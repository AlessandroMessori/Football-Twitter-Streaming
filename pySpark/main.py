from pyspark.sql.session import SparkSession
from pyspark.sql.functions import lit, explode, split, col, from_json, to_json, json_tuple, window, struct, udf
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
        .withWatermark("timestamp", "10 seconds") \
        .withColumn('word', explode(split(col(colName), ' '))) \
        .groupBy(window(col("timestamp"), "10 seconds", "5 seconds"),
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


def getLastName(full_name):
    return full_name.split(" ")[-1:][0]


if __name__ == "__main__":
    spark = SparkSession.builder.appName("wordCounter").getOrCreate()

    # Defines schema of Twitter Post
    tweetSchema = StructType() \
        .add("payload", StringType())

    payloadSchema = StructType() \
        .add("Text", StringType()) \
        .add("Lang", StringType())

    players = spark.read \
        .option("header", "true") \
        .option("mode", "DROPMALFORMED") \
        .csv("work/players_21.csv")

    lastNameUDF = udf(getLastName, StringType())

    player_names = players \
        .withColumn(
            "word", lastNameUDF("short_name")) \
        .withColumn("category", lit("Player")) \
        .select("word", "category") \
        .limit(500) \

    teams = players \
        .select("club_name") \
        .withColumn("category", lit("Team")) \
        .limit(500) \
        .dropDuplicates() \

    topics = player_names.union(teams)

    # Reads the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "broker:9092") \
        .option("failOnDataLoss", "false") \
        .option("subscribe", "tweets") \
        .option("startingOffsets", "earliest") \
        .load()

    messages = extractTweetPayload(df, tweetSchema, payloadSchema)

    wordCount = wordCountQuery(messages, "Text") \
        .join(topics, "word") \
        .select("word", "count","category", to_json(struct("word", "count","category")).alias("value"))

    langCount = langCountQuery(messages, "Lang")

    query = wordCount \
        .writeStream \
        .format("kafka") \
        .option("checkpointLocation", "./checkpoints") \
        .option("kafka.bootstrap.servers", "broker:9092") \
        .option("topic", "countByName") \
        .start()

    query.awaitTermination()
