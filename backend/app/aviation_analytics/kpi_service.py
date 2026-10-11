"""
TRAIT Aviation Analytics - Operational KPI Service
Calculates real-time executive KPI metrics across airport operations.
"""

import pandas as pd
from typing import Dict, Any
from app.database import get_db_connection
from app.models import KPISummary

def get_kpi_summary() -> KPISummary:
    conn = get_db_connection()
    df_flights = pd.read_sql_query("SELECT * FROM flights", conn)
    df_bag = pd.read_sql_query("SELECT * FROM baggage_operations", conn)
    df_pax = pd.read_sql_query("SELECT * FROM passenger_hourly_flow", conn)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM operational_anomalies WHERE status = 'ACTIVE'")
    active_anomalies = cursor.fetchone()[0]
    conn.close()

    total_flights = len(df_flights)
    if total_flights > 0:
        delayed_count = int((df_flights["delay_minutes"] > 15).sum())
        otp = round(((total_flights - delayed_count) / total_flights) * 100, 1)
        avg_delay = round(df_flights["delay_minutes"].mean(), 1)
        avg_turnaround = round(df_flights["turnaround_time_mins"].mean(), 1)
    else:
        otp, avg_delay, avg_turnaround = 100.0, 0.0, 45.0

    if not df_pax.empty:
        avg_sec_wait = round(df_pax["security_wait_mins"].mean(), 1)
    else:
        avg_sec_wait = 8.5

    if not df_bag.empty:
        avg_first_bag = round(df_bag["first_bag_mins"].mean(), 1)
        total_bags = int(df_bag["total_bags"].sum())
        mishandled = int(df_bag["mishandled_bags"].sum())
        mishandled_rate = round((mishandled / max(1, total_bags)) * 1000, 2)
    else:
        avg_first_bag, mishandled_rate = 14.2, 0.45

    return KPISummary(
        otp_percentage=otp,
        avg_delay_mins=avg_delay,
        avg_turnaround_mins=avg_turnaround,
        avg_security_wait_mins=avg_sec_wait,
        first_bag_avg_mins=avg_first_bag,
        mishandled_bag_rate_per_1000=mishandled_rate,
        active_anomalies_count=active_anomalies,
        total_flights_monitored=total_flights,
        synthetic_disclaimer="SYNTHETIC DEMONSTRATION DATA"
    )
