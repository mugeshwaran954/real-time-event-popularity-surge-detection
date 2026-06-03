import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from surge_detection.surge_algorithm import detect_surge

spark = SparkSession.builder \
    .appName("TweetSurgeDetectionFinal") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# -------- Read Kafka --------
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers","localhost:9092") \
    .option("subscribe","tweets_stream") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

tweets = df.selectExpr(
    "CAST(value AS STRING) as tweet",
    "timestamp"
)

# -------- Timestamp + Watermark --------
tweets = tweets.withColumn("timestamp", to_timestamp(col("timestamp"))) \
               .withWatermark("timestamp", "2 minutes")

# -------- Apply Logic --------
result = detect_surge(tweets)

result = result.select(
    "window_start",
    "window_end",
    "hashtag",
    "tweet_count"
)

# -------- Console --------
console_query = result.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

# -------- CSV --------
file_query = result.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path","../storage/results") \
    .option("checkpointLocation","../storage/checkpoints") \
    .start()

spark.streams.awaitAnyTermination()
