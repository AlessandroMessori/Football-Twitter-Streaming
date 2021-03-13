from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json,json_tuple
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType

if __name__ == "__main__":
    spark = SparkSession.builder.appName("wordCounter").getOrCreate()

    # Defines schema of Twitter Post
    tweetSchema = StructType() \
            .add("payload", StringType())

    payloadSchema = StructType() \
            .add("Text", StringType())
                
    # Reads the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "testing2") \
        .option("startingOffsets", "earliest") \
        .load()
    
    messages = df \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", tweetSchema).alias("data")) \
        .select(from_json("data.payload", payloadSchema).alias("payload")) \
        .select("payload.*")


    query = messages \
        .writeStream \
        .format("console") \
        .start()

    import time
    time.sleep(10)  # sleep 10 seconds
    query.stop()