# 🚀 Real-Time Online Event Popularity Surge Detection Using Streaming Big Data Analytics

## 📌 Project Overview

Social media platforms generate massive amounts of real-time data that reflect public attention toward events, topics, and trends. Detecting sudden increases in popularity is important for trend monitoring, event awareness, and decision-making.

This project implements a real-time popularity surge detection system using Apache Kafka and Apache Spark Structured Streaming. The system continuously processes streaming tweet data, identifies emerging hashtag trends, computes surge intensity, and visualizes results through an interactive dashboard.

---

## 🎯 Objectives

- Develop a real-time streaming analytics pipeline.
- Detect emerging online events using hashtag analysis.
- Quantify popularity surge intensity using a surge score.
- Process streaming data using sliding window analytics.
- Visualize trends, alerts, and insights through a dashboard.

---

## 🏗️ System Architecture

```text
Tweet Dataset
      │
      ▼
Kafka Producer
      │
      ▼
Apache Kafka Topic
      │
      ▼
Spark Structured Streaming
      │
      ▼
Hashtag Extraction
      │
      ▼
Sliding Window Analytics
      │
      ▼
CSV Storage
      │
      ▼
Streamlit Dashboard
      │
      ▼
Surge Alerts & Insights
```

---

## ⚙️ Technologies Used

- Apache Kafka
- Apache Spark Structured Streaming
- Python
- Pandas
- Streamlit
- Plotly

---

## 📊 Methodology

### 1. Data Streaming
Tweets from the FIFA World Cup dataset are streamed through Apache Kafka to simulate real-time social media activity.

### 2. Real-Time Processing
Apache Spark Structured Streaming consumes data from Kafka and performs continuous processing.

### 3. Hashtag Extraction
Hashtags are extracted from tweet text and treated as representations of online events and trends.

### 4. Sliding Window Analytics
A sliding window of 1 minute with a 10-second slide interval is used to calculate hashtag frequencies.

### 5. Surge Detection
Popularity surge is computed using:

```text
Surge Score = (Current Count - Previous Count) / (Previous Count + 1)
```

Higher scores indicate rapidly emerging trends.

### 6. Visualization
A Streamlit dashboard displays:

- Real-time metrics
- Trending hashtags
- Trend analysis
- Surge alerts
- Analytical insights

---

## 📂 Project Structure

```text
real-time-popularity-surge-detection/
│
├── kafka_producer/
│   └── producer.py
│
├── spark_processing/
│   └── spark_stream.py
│
├── surge_detection/
│   └── surge_algorithm.py
│
├── dashboard/
│   └── dashboard.py
│
├── storage/
│   ├── results/
│   └── checkpoints/
│
├── README.md
└── requirements.txt
```

---

## 📈 Features

✅ Real-time tweet streaming

✅ Distributed stream processing

✅ Hashtag extraction

✅ Sliding window analytics

✅ Popularity surge detection

✅ Real-time dashboard

✅ Surge alerts

✅ Trend visualization

✅ Analytical insights

---

## 📊 Dashboard Outputs

The dashboard provides:

- Total Tweets Processed
- Unique Hashtags Detected
- Active Surge Events
- Average Surge Score
- Top Emerging Hashtags
- Trend Analysis Graphs
- Surge Distribution
- Real-Time Alerts
- Analytical Insights

---
<img width="975" height="521" alt="image" src="https://github.com/user-attachments/assets/ba50c100-454a-41a5-9669-994533c598fc" />

<img width="975" height="293" alt="image" src="https://github.com/user-attachments/assets/7cf6f32e-62ad-476e-8af6-3ac731d9fd77" />

<img width="975" height="288" alt="image" src="https://github.com/user-attachments/assets/e0dce536-8b60-4296-9363-ab95b2601fb1" />

<img width="975" height="404" alt="image" src="https://github.com/user-attachments/assets/06942938-8e9e-47f1-9ada-e79eb4416071" />

<img width="975" height="312" alt="image" src="https://github.com/user-attachments/assets/23f2af84-2b37-43a5-a1fe-22411d85931e" />

## 📁 Dataset

**Dataset:** FIFA World Cup 2022 Tweets Dataset

**Attributes:**

| Attribute | Description |
|------------|------------|
| timestamp | Tweet timestamp |
| tweet_text | Tweet content |
| likes | Number of likes |
| sentiment | Sentiment label |

---

## 🚀 How to Run

### Step 1: Start Kafka

```bash
zookeeper-server-start.sh config/zookeeper.properties

kafka-server-start.sh config/server.properties
```

### Step 2: Run Spark Streaming

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 spark_processing/spark_stream.py
```

### Step 3: Start Kafka Producer

```bash
python kafka_producer/producer.py
```

### Step 4: Launch Dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

## 📊 Performance Metrics

- Processing Latency: ~1–3 seconds
- Throughput: Continuous tweet stream processing
- Surge Detection Responsiveness: ~10 seconds
- Dashboard Refresh Interval: 5 seconds

---

## 🎓 Academic Contribution

This project demonstrates how streaming big data technologies can be used to identify and quantify popularity surges in real time. The system combines distributed data processing, sliding window analytics, and interactive visualization to provide actionable insights from social media streams.

---
