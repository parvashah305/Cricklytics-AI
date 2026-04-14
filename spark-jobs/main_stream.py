from datetime import datetime, timezone
import os

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from redis import Redis
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    BooleanType,
    FloatType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

from analytics.pressure_index import compute_pressure_index


def invalidate_redis_cache(match_ids: list[str]) -> None:
    if not match_ids:
        return

    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

    keys_to_delete: list[str] = []
    for match_id in match_ids:
        keys_to_delete.extend(
            [
                f"analytics:{match_id}",
                f"scorecard:{match_id}",
                f"match:{match_id}:analytics",
                f"match:{match_id}:scorecard",
            ]
        )

    if keys_to_delete:
        redis_client.delete(*keys_to_delete)
    redis_client.close()


def build_ball_schema() -> StructType:
    return StructType(
        [
            StructField("event_id", StringType(), False),
            StructField("match_id", StringType(), False),
            StructField("innings", IntegerType(), False),
            StructField("over", FloatType(), False),
            StructField("ball", IntegerType(), False),
            StructField("batsman", StringType(), False),
            StructField("bowler", StringType(), False),
            StructField("runs", IntegerType(), False),
            StructField("is_wicket", BooleanType(), False),
            StructField("is_boundary", BooleanType(), False),
            StructField("is_dot", BooleanType(), False),
            StructField("delivery_type", StringType(), False),
            StructField("timestamp", LongType(), False),
        ]
    )


def write_ball_events_to_mongo(batch_df: DataFrame, _batch_id: int) -> None:
    if batch_df.rdd.isEmpty():
        return

    records = []
    for row in batch_df.collect():
        ts_ms = int(row["timestamp"])
        records.append(
            {
                "event_id": row["event_id"],
                "match_id": row["match_id"],
                "innings": int(row["innings"]),
                "over": float(row["over"]),
                "ball": int(row["ball"]),
                "batsman": row["batsman"],
                "bowler": row["bowler"],
                "runs": int(row["runs"]),
                "is_wicket": bool(row["is_wicket"]),
                "is_boundary": bool(row["is_boundary"]),
                "is_dot": bool(row["is_dot"]),
                "delivery_type": row["delivery_type"],
                "timestamp": datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc),
            }
        )

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/cricklytics")
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client.get_default_database() or mongo_client["cricklytics"]
    collection = db["ball_events"]
    collection.create_index([("match_id", 1), ("innings", 1), ("over", 1), ("ball", 1)])
    collection.create_index("event_id", unique=True)
    try:
        collection.insert_many(records, ordered=False)
    except BulkWriteError:
        # Duplicate event_id records are expected during retries/replays.
        pass

    analytics_collection = db["analytics"]
    analytics_collection.create_index("match_id", unique=True)

    by_match: dict[str, list[dict]] = {}
    for record in records:
        by_match.setdefault(record["match_id"], []).append(record)

    for match_id, match_records in by_match.items():
        total_runs = sum(int(item["runs"]) for item in match_records)
        total_wickets = sum(1 for item in match_records if item["is_wicket"])
        total_dots = sum(1 for item in match_records if item["is_dot"])
        total_boundaries = sum(1 for item in match_records if item["is_boundary"])
        total_balls = max(len(match_records), 1)
        overs = total_balls / 6.0
        current_run_rate = round((total_runs / overs) if overs > 0 else 0.0, 2)

        innings_target = float(os.getenv("SIM_DEFAULT_TARGET", "180"))
        innings_overs = float(os.getenv("SIM_DEFAULT_OVERS", "20"))
        remaining_balls = max(int(innings_overs * 6) - total_balls, 1)
        required_runs = max(int(innings_target) - total_runs, 0)
        required_run_rate = round((required_runs * 6) / remaining_balls, 2)
        dot_ball_percentage = (total_dots / total_balls) * 100.0

        pressure_index = compute_pressure_index(
            required_run_rate=required_run_rate,
            current_run_rate=current_run_rate,
            dot_ball_percentage=dot_ball_percentage,
            wickets_fallen=total_wickets,
        )
        win_probability_home = round(max(0.0, min(1.0, 1.0 - pressure_index / 100.0)), 4)
        win_probability_away = round(1.0 - win_probability_home, 4)
        projected_score = round(current_run_rate * innings_overs, 1)

        momentum_state = "stable"
        if total_boundaries >= 3:
            momentum_state = "rising"
        if total_wickets >= 2:
            momentum_state = "falling"
        if total_boundaries >= 3 and total_wickets >= 2:
            momentum_state = "shift"

        analytics_collection.update_one(
            {"match_id": match_id},
            {
                "$set": {
                    "match_id": match_id,
                    "pressure_index": pressure_index,
                    "win_probability": {
                        "home": win_probability_home,
                        "away": win_probability_away,
                    },
                    "current_run_rate": current_run_rate,
                    "required_run_rate": required_run_rate,
                    "momentum_state": momentum_state,
                    "projected_score": projected_score,
                    "commentary": (
                        f"Over momentum: {momentum_state}. "
                        f"Runs: {total_runs}/{total_wickets}."
                    ),
                    "last_updated": datetime.now(timezone.utc),
                }
            },
            upsert=True,
        )

    invalidate_redis_cache(list(by_match.keys()))
    mongo_client.close()


def main() -> None:
    spark = (
        SparkSession.builder.appName(os.getenv("SPARK_APP_NAME", "CricklyticsStream"))
        .master(os.getenv("SPARK_MASTER", "local[*]"))
        .getOrCreate()
    )
    schema = build_ball_schema()

    stream_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", os.getenv("KAFKA_BROKER", "localhost:9092"))
        .option(
            "subscribe", os.getenv("KAFKA_TOPIC_BALL_EVENTS", "cricket.ball.events")
        )
        .option("startingOffsets", "latest")
        .load()
    )

    parsed_df = stream_df.select(
        from_json(col("value").cast("string"), schema).alias("event")
    ).select("event.*")

    query = (
        parsed_df.writeStream.foreachBatch(write_ball_events_to_mongo)
        .outputMode("append")
        .option("checkpointLocation", "./spark-checkpoints/ball-events")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
