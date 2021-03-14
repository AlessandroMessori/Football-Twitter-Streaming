from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json, json_tuple, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType

if __name__ == "__main__":
    spark = SparkSession.builder.appName("wordCounter").getOrCreate()

    # Defines schema of Twitter Post
    tweetSchema = StructType() \
        .add("payload", StringType())

    payloadSchema = StructType() \
        .add("Text", StringType()) \
        .add("Lang", StringType())

    # Reads the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "testing2") \
        .option("startingOffsets", "earliest") \
        .load()

    messages = df \
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "CAST(timestamp AS TIMESTAMP)", "offset") \
        .withColumn("data", from_json("value", tweetSchema)) \
        .withColumn("payload", from_json("data.payload", payloadSchema)) \
        .select("payload.*", "key", "timestamp")

    langCount = messages \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window(col("timestamp"), "10 minutes", "5 minutes"),
            col("Lang")
        ).count()

    query = langCount \
        .writeStream \
        .format("console") \
        .start()

    query.awaitTermination()
