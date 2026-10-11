"""
TRAIT Aviation Analytics - Flight Delay Analysis Service
Analyzes delay causality, airline performance, terminal metrics, and distribution.
"""

import pandas as pd
from typing import Dict, Any, List
from app.database import get_db_connection

def get_delay_analysis() -> Dict[str, Any]:
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM flights", conn)
    conn.close()

    if df.empty:
        return {}

    total_flights = len(df)
    delayed_df = df[df["delay_minutes"] > 15]
    total_delayed = len(delayed_df)
    otp_pct = round(((total_flights - total_delayed) / total_flights) * 100, 1)

    # 1. Delay Causality Breakdown
    cause_counts = delayed_df["delay_reason"].value_counts().to_dict()
    causes_breakdown = []
    for cause in ["Carrier", "Weather", "NAS/ATC", "Late Aircraft", "Security"]:
        count = cause_counts.get(cause, 0)
        pct = round((count / max(1, total_delayed)) * 100, 1)
        causes_breakdown.append({
            "cause": cause,
            "flight_count": count,
            "percentage": pct
        })

    # 2. Airline Performance Breakdown
    airline_stats = []
    for airline, group in df.groupby("airline"):
        grp_delayed = group[group["delay_minutes"] > 15]
        grp_total = len(group)
        grp_otp = round(((grp_total - len(grp_delayed)) / grp_total) * 100, 1)
        avg_delay = round(group["delay_minutes"].mean(), 1)
        max_delay = int(group["delay_minutes"].max())
        airline_stats.append({
            "airline": airline,
            "total_flights": grp_total,
            "delayed_flights": len(grp_delayed),
            "otp_percentage": grp_otp,
            "avg_delay_mins": avg_delay,
            "max_delay_mins": max_delay
        })
    airline_stats.sort(key=lambda x: x["otp_percentage"], reverse=True)

    # 3. Terminal Delay Distribution
    terminal_stats = []
    for term, group in df.groupby("terminal"):
        grp_delayed = group[group["delay_minutes"] > 15]
        terminal_stats.append({
            "terminal": term,
            "total_flights": len(group),
            "delayed_flights": len(grp_delayed),
            "avg_delay_mins": round(group["delay_minutes"].mean(), 1),
            "otp_percentage": round(((len(group) - len(grp_delayed)) / len(group)) * 100, 1)
        })

    # 4. Delay Duration Histogram Bins
    delay_bins = [
        {"range": "0-15m (On-Time)", "count": int((df["delay_minutes"] <= 15).sum())},
        {"range": "16-30m (Minor)", "count": int(((df["delay_minutes"] > 15) & (df["delay_minutes"] <= 30)).sum())},
        {"range": "31-60m (Moderate)", "count": int(((df["delay_minutes"] > 30) & (df["delay_minutes"] <= 60)).sum())},
        {"range": "61-90m (Significant)", "count": int(((df["delay_minutes"] > 60) & (df["delay_minutes"] <= 90)).sum())},
        {"range": "90m+ (Severe)", "count": int((df["delay_minutes"] > 90).sum())}
    ]

    return {
        "summary": {
            "total_flights": total_flights,
            "delayed_flights": total_delayed,
            "on_time_performance_pct": otp_pct,
            "avg_delay_all_flights": round(df["delay_minutes"].mean(), 1),
            "avg_delay_delayed_only": round(delayed_df["delay_minutes"].mean(), 1) if not delayed_df.empty else 0.0
        },
        "causality_breakdown": causes_breakdown,
        "airline_performance": airline_stats,
        "terminal_performance": terminal_stats,
        "duration_distribution": delay_bins,
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }
