import csv
from datetime import datetime

def save_log_to_csv(filename, logs):
    """logs là danh sách các dict, ví dụ:
       [{"time": "2025-10-07 08:30", "event": "Start Retraining", "status": "OK"}, ...]
    """
    fieldnames = ["time", "event", "status"]

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)

# Ví dụ sử dụng:
logs = [
    {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": "Retraining", "status": "Start"},
    {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": "Retraining", "status": "Done"},
]

save_log_to_csv("log_retraining.csv", logs)
print("✅ Log đã lưu vào log_retraining.csv")
