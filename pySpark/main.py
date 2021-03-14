from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json, to_json, json_tuple, window, struct
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType


# extracts structured content from json tweet message
def extractTweetPayload(df, tweetSchema, payloadSchema):
    return df \
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "CAST(timestamp AS TIMESTAMP)", "offset") \
        .withColumn("data", from_json("value", tweetSchema)) \
        .withColumn("payload", from_json("data.payload", payloadSchema)) \
        .select("payload.*", "key", "timestamp")

# given a steam dataframe returns a df with an additional word count column


def wordCountQuery(df, colName):
    return df \
        .withWatermark("timestamp", "2 minutes") \
        .withColumn('word', explode(split(col(colName), ' '))) \
        .groupBy(window(col("timestamp"), "2 minutes", "1 minutes"),
                 col('word')
                 ).count() \
        .select("word", "count", to_json(struct("word", "count")).alias("value"))


def langCountQuery(df, colName):
    return df \
        .withWatermark("timestamp", "2 minutes") \
        .groupBy(
            window(col("timestamp"), "2 minutes", "1 minutes"),
            col(colName)
        ).count() \
        .select(colName, "count", to_json(struct(colName, "count")).alias("value"))


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
        .option("failOnDataLoss", "false") \
        .option("subscribe", "testing2") \
        .option("startingOffsets", "earliest") \
        .load()

    messages = extractTweetPayload(df, tweetSchema, payloadSchema)

    wordCount = wordCountQuery(messages, "Text")

    #langCount = langCountQuery(messages, "Lang")

    query = wordCount \
        .writeStream \
        .format("kafka") \
        .option("checkpointLocation", "/home/alessandro/Desktop/Repos/Football-Twitter-Streaming/checkpoints") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "words") \
        .start()

    '''query = wordCount \
        .writeStream \
        .format("console") \
        .start()'''

    query.awaitTermination()
