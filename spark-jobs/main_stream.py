from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import BooleanType, FloatType, IntegerType, LongType, StringType, StructField, StructType


def build_ball_schema() -> StructType:
    return StructType(
        [
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


def main() -> None:
    spark = SparkSession.builder.appName("CricklyticsStream").getOrCreate()
    schema = build_ball_schema()

    stream_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "cricket.ball.events")
        .option("startingOffsets", "latest")
        .load()
    )

    parsed_df = stream_df.select(
        from_json(col("value").cast("string"), schema).alias("event")
    ).select("event.*")

    query = (
        parsed_df.writeStream.format("console")
        .outputMode("append")
        .option("truncate", False)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
