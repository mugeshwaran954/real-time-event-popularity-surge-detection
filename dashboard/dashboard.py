import streamlit as st
import pandas as pd
import glob
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Real-Time Popularity Surge Detection", layout="wide")

st_autorefresh(interval=5000)

st.title("📊 Real-Time Popularity Surge Detection Dashboard")

DATA_PATH = "../storage/results/*.csv"

files = glob.glob(DATA_PATH)

columns = ["window_start","window_end","hashtag","tweet_count"]

dfs = []

for f in files:
    try:
        temp = pd.read_csv(f, header=None)
        if len(temp.columns) == 4:
            temp.columns = columns
            dfs.append(temp)
    except:
        pass

if len(dfs) == 0:
    st.warning("Waiting for streaming data...")
    st.stop()

df = pd.concat(dfs)

# -------- PREPROCESS --------
df["window_start"] = pd.to_datetime(df["window_start"])
df = df[df["hashtag"] != "#worldcup2022"]

df = df.sort_values(by=["hashtag", "window_start"])

# -------- SURGE LOGIC --------
df["prev_count"] = df.groupby("hashtag")["tweet_count"].shift(1)
df["prev_count"] = df["prev_count"].fillna(0)

df["surge_score"] = (df["tweet_count"] - df["prev_count"]) / (df["prev_count"] + 1)

def classify(x):
    if x > 2:
        return "High Surge"
    elif x > 1:
        return "Moderate Surge"
    else:
        return "Low/Stable"

df["surge_level"] = df["surge_score"].apply(classify)

# -------- KPI SECTION --------
st.subheader("📌 Real-Time Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tweets Processed", int(df["tweet_count"].sum()))
col2.metric("Unique Hashtags Detected", df["hashtag"].nunique())
col3.metric("Active Surge Events", (df["surge_level"] == "High Surge").sum())
col4.metric("Avg Surge Score", round(df["surge_score"].mean(), 2))

st.divider()

# -------- TOP SURGE --------
st.subheader("🔥 Top Emerging Hashtag Trends (Real-Time Surge)")

latest_time = df["window_start"].max()
latest_df = df[df["window_start"] == latest_time]

top = latest_df.sort_values(by="surge_score", ascending=False).head(10)

fig = px.bar(
    top,
    x="hashtag",
    y="surge_score",
    text="surge_score",
    title="Top Emerging Hashtags Based on Current Surge"
)

st.plotly_chart(fig, use_container_width=True)

# -------- TIME SERIES (FIXED + PROFESSIONAL) --------
st.subheader("📈 Hashtag Trend Analysis (Enhanced View)")

top_tags = top["hashtag"].head(5).values  # ✅ FIXED

sample = df[df["hashtag"].isin(top_tags)].copy()

# -------- LIMIT TIME WINDOW --------
latest_time = sample["window_start"].max()
sample = sample[
    sample["window_start"] > latest_time - pd.Timedelta(minutes=5)
]

# -------- RESAMPLE SAFELY --------
resampled_list = []

for tag in sample["hashtag"].unique():
    temp = sample[sample["hashtag"] == tag].copy()
    
    temp = temp.set_index("window_start")
    
    temp = temp["tweet_count"].resample("1min").sum().reset_index()
    
    temp["hashtag"] = tag  # IMPORTANT
    
    resampled_list.append(temp)

sample = pd.concat(resampled_list)

sample["tweet_count"] = sample["tweet_count"].fillna(0)

# -------- SMOOTH --------
sample = sample.sort_values(by=["hashtag", "window_start"])

sample["smoothed"] = sample.groupby("hashtag")["tweet_count"] \
    .rolling(window=2, min_periods=1).mean().reset_index(0, drop=True)

# -------- PLOT --------
fig = px.area(
    sample,
    x="window_start",
    y="smoothed",
    color="hashtag",
    title="Hashtag Popularity Trends Over Time",
    labels={"smoothed": "Tweet Volume"}
)

st.plotly_chart(fig, use_container_width=True)

# -------- SURGE DISTRIBUTION --------
st.subheader("📊 Surge Level Distribution")

fig3 = px.pie(
    df,
    names="surge_level",
    title="Distribution of Surge Categories"
)

st.plotly_chart(fig3, use_container_width=True)

# -------- ALERT SYSTEM --------
st.subheader("🚨 Real-Time Surge Alerts")

alerts = df[df["surge_level"] == "High Surge"]

if len(alerts) > 0:
    st.error("High Surge Detected in Hashtag Trends!")
    st.dataframe(alerts.sort_values("surge_score", ascending=False))
else:
    st.success("No critical surge events detected")

# -------- INSIGHTS (CONSISTENT WITH ALERTS) --------
st.subheader("🧠 Analytical Insights")

# -------- REAL-TIME INSIGHT --------
latest_time = df["window_start"].max()
latest_df = df[df["window_start"] == latest_time]

if len(latest_df) > 0:
    current_top = latest_df.sort_values(by="surge_score", ascending=False).iloc[0]
    
    st.write(f"🔥 Current top emerging hashtag: **{current_top['hashtag']}**")
    st.write(f"⚡ Current surge score: **{round(current_top['surge_score'],2)}**")

# -------- GLOBAL INSIGHT --------
# -------- GLOBAL INSIGHT --------
valid_df = df[df["surge_score"].notna()]

if len(valid_df) > 0:

    top_row = valid_df.sort_values(by="surge_score", ascending=False).iloc[0]

    max_hashtag = top_row["hashtag"]
    max_score = top_row["surge_score"]

    st.write(f"📊 Highest observed surge (overall): **{max_hashtag}**")
    st.write(f"🚀 Peak surge score recorded: **{round(max_score, 2)}**")

else:
    st.write("No sufficient surge data available for global insights")

# -------- RAW STREAM --------
st.subheader("📡 Live Streaming Data Snapshot")

st.dataframe(df.tail(20))
