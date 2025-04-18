import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Helper function to generate random timestamps
def random_dates(start, end, n):
    delta = end - start
    return [start + timedelta(seconds=random.randint(0, int(delta.total_seconds()))) for _ in range(n)]

# Set parameters
num_rows = 10000
users = [f"user_{i}" for i in range(1, 101)]
ips = [f"192.168.1.{i}" for i in range(1, 51)]
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# Make sure the target directory exists
data_dir = "sample_datasets"
os.makedirs(data_dir, exist_ok=True)

# Dataset 1: Web application logs
actions = ["login", "logout", "read", "write", "delete", "update"]
web_logs = pd.DataFrame({
    "timestamp": random_dates(start_date, end_date, num_rows),
    "user_id": np.random.choice(users, num_rows),
    "action": np.random.choice(actions, num_rows),
    "ip_address": np.random.choice(ips, num_rows),
    "status": np.random.choice(["success", "failure"], num_rows, p=[0.95, 0.05])
})

# Dataset 2: Database access logs
db_logs = pd.DataFrame({
    "timestamp": random_dates(start_date, end_date, num_rows),
    "user_id": np.random.choice(users, num_rows),
    "query_type": np.random.choice(["SELECT", "INSERT", "UPDATE", "DELETE"], num_rows),
    "table": np.random.choice(["users", "orders", "products", "payments"], num_rows),
    "execution_time_ms": np.random.exponential(scale=100, size=num_rows).astype(int),
    "ip_address": np.random.choice(ips, num_rows)
})

# Dataset 3: File access logs
file_logs = pd.DataFrame({
    "timestamp": random_dates(start_date, end_date, num_rows),
    "user_id": np.random.choice(users, num_rows),
    "file_path": np.random.choice([
        "/home/docs/report.pdf", "/var/log/syslog", "/etc/passwd", "/data/backup.zip"
    ], num_rows),
    "access_type": np.random.choice(["read", "write", "execute"], num_rows),
    "status": np.random.choice(["granted", "denied"], num_rows, p=[0.9, 0.1])
})

# Save datasets to CSV
web_logs_path = os.path.join(data_dir, "web_logs.csv")
db_logs_path = os.path.join(data_dir, "db_logs.csv")
file_logs_path = os.path.join(data_dir, "file_logs.csv")

web_logs.to_csv(web_logs_path, index=False)
db_logs.to_csv(db_logs_path, index=False)
file_logs.to_csv(file_logs_path, index=False)

print("✅ Datasets saved successfully in the 'sample_datasets' folder.")
