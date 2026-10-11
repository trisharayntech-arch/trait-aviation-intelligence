"""
TRAIT Aviation Analytics - Machine Learning Anomaly Detection Service
Powered by Scikit-Learn IsolationForest.
Detects operational bottlenecks across turnaround times, delays, and baggage reclaim.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, List
from app.database import get_db_connection

def detect_operational_anomalies() -> Dict[str, Any]:
    conn = get_db_connection()
    df_flights = pd.read_sql_query("SELECT * FROM flights", conn)
    df_bag = pd.read_sql_query("SELECT * FROM baggage_operations", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operational_anomalies ORDER BY id DESC")
    logged_anomalies = [dict(row) for row in cursor.fetchall()]
    conn.close()

    anomalies_list: List[Dict[str, Any]] = []

    # 1. Isolation Forest on Flight Operations (Turnaround & Delay)
    if len(df_flights) >= 10:
        features = df_flights[["turnaround_time_mins", "delay_minutes", "passengers_booked"]].copy()
        
        # Fit Isolation Forest
        iso_forest = IsolationForest(contamination=0.06, random_state=42)
        predictions = iso_forest.fit_predict(features)
        scores = iso_forest.decision_function(features)

        # Flag outliers (predictions == -1)
        outlier_indices = np.where(predictions == -1)[0]
        mean_turnaround = df_flights["turnaround_time_mins"].mean()
        std_turnaround = df_flights["turnaround_time_mins"].std()

        for idx in outlier_indices:
            row = df_flights.iloc[idx]
            turnaround = float(row["turnaround_time_mins"])
            delay = float(row["delay_minutes"])
            score = round(float(scores[idx]), 3)

            # Determine severity
            if turnaround > mean_turnaround + 2.0 * std_turnaround or delay > 75:
                severity = "HIGH"
            else:
                severity = "MEDIUM"

            anomalies_list.append({
                "id": len(anomalies_list) + 1,
                "timestamp": row["scheduled_time"],
                "incident_type": "Flight Turnaround Anomaly",
                "flight_number": row["flight_number"],
                "airline": row["airline"],
                "location": f"{row['terminal']} ({row['gate']})",
                "metric_name": "Turnaround Duration",
                "observed_value": turnaround,
                "expected_range": f"{round(mean_turnaround - std_turnaround, 0)} - {round(mean_turnaround + std_turnaround, 0)} mins",
                "anomaly_score": score,
                "severity": severity,
                "description": f"Flight {row['flight_number']} experienced turnaround of {turnaround:.0f} mins with {delay:.0f} min delay. ML Model flagged deviation from normal operational envelope.",
                "status": "ACTIVE" if severity == "HIGH" else "RESOLVING"
            })

    # 2. Isolation Forest on Baggage Operations
    if len(df_bag) >= 10:
        bag_features = df_bag[["first_bag_mins", "last_bag_mins", "dwell_time_mins", "total_bags"]].copy()
        iso_bag = IsolationForest(contamination=0.08, random_state=42)
        bag_preds = iso_bag.fit_predict(bag_features)
        bag_scores = iso_bag.decision_function(bag_features)

        bag_outliers = np.where(bag_preds == -1)[0]
        mean_last_bag = df_bag["last_bag_mins"].mean()

        for idx in bag_outliers:
            row = df_bag.iloc[idx]
            last_bag = float(row["last_bag_mins"])
            score = round(float(bag_scores[idx]), 3)

            if last_bag > 60:
                severity = "HIGH"
            else:
                severity = "MEDIUM"

            anomalies_list.append({
                "id": len(anomalies_list) + 1,
                "timestamp": "Real-time Belt Monitor",
                "incident_type": "Baggage Dwell Anomaly",
                "flight_number": row["flight_number"],
                "airline": "Arrival Operations",
                "location": f"{row['terminal']} ({row['carousel_id']})",
                "metric_name": "Last Bag Delivery Time",
                "observed_value": last_bag,
                "expected_range": "20 - 45 mins",
                "anomaly_score": score,
                "severity": severity,
                "description": f"Baggage discharge at {row['carousel_id']} completed in {last_bag:.0f} mins. Exceeded airport target SLA by {max(0, last_bag - 45):.0f} mins.",
                "status": "ACTIVE" if severity == "HIGH" else "MONITORING"
            })

    # Sort by severity (HIGH first) then anomaly score
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    anomalies_list.sort(key=lambda x: (severity_order.get(x["severity"], 3), x["anomaly_score"]))

    # Scatter plot data points for visualization: Normal vs Anomaly
    scatter_points = []
    if len(df_flights) >= 10:
        for i, row in df_flights.head(40).iterrows():
            is_anomaly = any(a.get("flight_number") == row["flight_number"] for a in anomalies_list)
            scatter_points.append({
                "flight_number": row["flight_number"],
                "turnaround_mins": int(row["turnaround_time_mins"]),
                "delay_mins": int(row["delay_minutes"]),
                "passengers": int(row["passengers_booked"]),
                "is_anomaly": is_anomaly,
                "severity": "HIGH" if (row["turnaround_time_mins"] > 100 or row["delay_minutes"] > 80) else ("MEDIUM" if is_anomaly else "NORMAL")
            })

    return {
        "active_anomalies_count": len([a for a in anomalies_list if a["severity"] in ["HIGH", "MEDIUM"]]),
        "total_anomalies_detected": len(anomalies_list),
        "anomalies": anomalies_list[:12],  # Top anomalies
        "scatter_points": scatter_points,
        "logged_incidents": logged_anomalies,
        "model_metadata": {
            "algorithm": "Scikit-Learn IsolationForest (Tree-based ensemble)",
            "features_used": ["turnaround_time_mins", "delay_minutes", "passengers_booked", "baggage_dwell"],
            "contamination_rate": 0.06
        },
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }
