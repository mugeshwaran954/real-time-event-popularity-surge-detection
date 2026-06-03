import json
import time
import random
import pandas as pd
from kafka import KafkaProducer
from config import KAFKA_SERVER, TOPIC_NAME

# -------- LOAD DATASET --------
df = pd.read_csv("../dataset/processed/cleaned_tweets.csv")

# -------- CREATE PRODUCER --------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 Starting tweet stream...\n")

# -------- STREAM DATA --------
for _, row in df.iterrows():

    tweet_data = {
        "timestamp": str(row["timestamp"]),
        "tweet": row["tweet_text"],
        "likes": int(row["likes"]),
        "sentiment": row["sentiment"]
    }

    producer.send(TOPIC_NAME, value=tweet_data)
    print("Sent:", tweet_data)

    time.sleep(random.uniform(0.2, 1.5))

producer.flush()
