from datetime import datetime, timezone
import os

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
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
