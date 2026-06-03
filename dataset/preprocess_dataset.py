import pandas as pd

# Load dataset
df = pd.read_csv("raw/fifa_world_cup_2022_tweets.csv")

# Select important columns
df = df[[
    "Date Created",
    "Tweet",
    "Number of Likes",
    "Sentiment"
]]

# Rename columns
df.columns = [
    "timestamp",
    "tweet_text",
    "likes",
    "sentiment"
]

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Save cleaned dataset
df.to_csv("processed/cleaned_tweets.csv", index=False)

print("Dataset cleaned successfully!")
print(df.head())
