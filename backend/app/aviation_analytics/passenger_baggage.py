"""
TRAIT Aviation Analytics - Passenger Flow & Baggage Operations Service
Computes passenger volume trends, terminal capacity pressure, and baggage belt dwell times.
"""

import pandas as pd
from typing import Dict, Any, List
from app.database import get_db_connection

def get_passenger_baggage_analytics() -> Dict[str, Any]:
    conn = get_db_connection()
    df_pax = pd.read_sql_query("SELECT * FROM passenger_hourly_flow ORDER BY timestamp ASC", conn)
    df_bag = pd.read_sql_query("SELECT * FROM baggage_operations", conn)
    conn.close()

    # 1. Passenger Throughput & Wait Time Trends (aggregated by timestamp)
    pax_trend = []
    if not df_pax.empty:
        for ts, group in df_pax.groupby("timestamp"):
            pax_trend.append({
                "timestamp": ts,
                "hour_label": ts[-5:],  # e.g., "14:00"
                "total_inbound": int(group["inbound_passengers"].sum()),
                "total_outbound": int(group["outbound_passengers"].sum()),
                "total_passengers": int(group["inbound_passengers"].sum() + group["outbound_passengers"].sum()),
                "avg_security_wait_mins": round(group["security_wait_mins"].mean(), 1),
                "avg_capacity_pct": round(group["capacity_pct"].mean(), 1)
            })

    # 2. Terminal Utilization Comparison
    terminal_pax = []
    if not df_pax.empty:
        for term, group in df_pax.groupby("terminal"):
            terminal_pax.append({
                "terminal": term,
                "avg_inbound_hourly": int(group["inbound_passengers"].mean()),
                "avg_outbound_hourly": int(group["outbound_passengers"].mean()),
                "avg_security_wait_mins": round(group["security_wait_mins"].mean(), 1),
                "peak_security_wait_mins": round(group["security_wait_mins"].max(), 1),
                "avg_capacity_pct": round(group["capacity_pct"].mean(), 1),
                "max_capacity_pct": round(group["capacity_pct"].max(), 1)
            })

    # 3. Baggage Operations Performance
    bag_summary = {}
    carousel_breakdown = []
    if not df_bag.empty:
        total_bags = int(df_bag["total_bags"].sum())
        processed_bags = int(df_bag["processed_bags"].sum())
        mishandled_bags = int(df_bag["mishandled_bags"].sum())
        avg_first_bag = round(df_bag["first_bag_mins"].mean(), 1)
        avg_last_bag = round(df_bag["last_bag_mins"].mean(), 1)
        avg_dwell = round(df_bag["dwell_time_mins"].mean(), 1)

        mishandled_rate = round((mishandled_bags / max(1, total_bags)) * 1000, 2)

        bag_summary = {
            "total_bags": total_bags,
            "processed_bags": processed_bags,
            "mishandled_bags": mishandled_bags,
            "mishandled_rate_per_1000": mishandled_rate,
            "avg_first_bag_mins": avg_first_bag,
            "avg_last_bag_mins": avg_last_bag,
            "avg_dwell_time_mins": avg_dwell,
            "sla_compliance_pct": round(((df_bag["last_bag_mins"] <= 45).sum() / len(df_bag)) * 100, 1)
        }

        for car, group in df_bag.groupby("carousel_id"):
            carousel_breakdown.append({
                "carousel_id": car,
                "terminal": group["terminal"].iloc[0],
                "flights_handled": len(group),
                "total_bags": int(group["total_bags"].sum()),
                "avg_last_bag_mins": round(group["last_bag_mins"].mean(), 1),
                "status": group["status"].iloc[-1]
            })
        carousel_breakdown.sort(key=lambda x: x["carousel_id"])

    return {
        "passenger_trend": pax_trend[-24:],  # Last 24 hours of flow
        "terminal_utilization": terminal_pax,
        "baggage_summary": bag_summary,
        "carousel_breakdown": carousel_breakdown,
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }
