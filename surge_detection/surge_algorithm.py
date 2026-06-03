from pyspark.sql.functions import (
    window, col, count, explode, split, lower
)

def detect_surge(df):

    # -------- Extract hashtags --------
    tweets = df.withColumn(
        "hashtags",
        split(lower(col("tweet")), " ")
    )

    tweets = tweets.withColumn(
        "hashtag",
        explode("hashtags")
    ).filter(col("hashtag").startswith("#"))

    # Remove dominant hashtag
    tweets = tweets.filter(col("hashtag") != "#worldcup2022")

    # -------- Window aggregation --------
    tweet_counts = tweets.groupBy(
        window(col("timestamp"), "1 minute", "10 seconds"),
        col("hashtag")
    ).agg(
        count("*").alias("tweet_count")
    )

    # Flatten window
    result = tweet_counts.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("hashtag"),
        col("tweet_count")
    )

    return result
