import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from io import StringIO
import os

st.set_page_config(page_title="Log Anomaly Detector", layout="wide")
st.title("🔍 Log Anomaly Detection App")

# Path to your datasets
DATASET_DIR = "sample_datasets"

# Preloaded datasets
built_in_datasets = {
    "Web Logs": os.path.join(DATASET_DIR, "web_logs.csv"),
    #"DB Logs": os.path.join(DATASET_DIR, "db_logs.csv"),
    #"File Logs": os.path.join(DATASET_DIR, "file_logs.csv")
}

# Sidebar - Choose dataset
st.sidebar.header("📁 Input Options")
dataset_option = st.sidebar.selectbox("Choose a demo dataset:", ["None"] + list(built_in_datasets.keys()))
uploaded_file = st.sidebar.file_uploader("Or upload your own CSV file", type=["csv"])
st.sidebar.write("""
Billa venu gopal reddy : 21BCS5361 \n
Sejal : 21BCS5517
""")

# Load dataset
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=["timestamp"])
    st.success("✅ Uploaded custom dataset!")
elif dataset_option != "None":
    dataset_path = built_in_datasets[dataset_option]
    df = pd.read_csv(dataset_path, parse_dates=["timestamp"])
    st.success(f"✅ Loaded built-in dataset: {dataset_option}")

if df is not None:
    st.subheader("📋 Sample of Log Data")
    st.dataframe(df.head())

    # Feature engineering
    df['hour'] = df['timestamp'].dt.hour
    df['action_code'] = df['action'].astype('category').cat.codes
    df['user_code'] = df['user_id'].astype('category').cat.codes
    df['ip_code'] = df['ip_address'].astype('category').cat.codes

    features = df[['hour', 'action_code', 'user_code', 'ip_code']]

    # Isolation Forest
    model = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly'] = model.fit_predict(features)

    # Show anomalies
    anomalies = df[df['anomaly'] == -1]
    st.subheader(f"🚨 Detected Anomalies: {len(anomalies)}")
    st.dataframe(anomalies)

    # Download
    csv = anomalies.to_csv(index=False)
    st.download_button("Download Anomaly Results", csv, file_name="anomalies.csv", mime="text/csv")

else:
    st.info("Please select or upload a dataset to get started.")
