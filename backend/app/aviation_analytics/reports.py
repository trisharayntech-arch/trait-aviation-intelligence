"""
TRAIT Aviation Analytics - Downloadable Reports Generator
Produces CSV datasets, JSON audits, and formatted operational summaries.
DISCLAIMER: ALL EXPORTED REPORTS ARE STRICTLY SYNTHETIC DEMONSTRATION DATA.
"""

import io
import json
import pandas as pd
from datetime import datetime
from typing import Tuple
from app.database import get_db_connection
from app.aviation_analytics.kpi_service import get_kpi_summary
from app.aviation_analytics.delay_analysis import get_delay_analysis
from app.aviation_analytics.anomaly_detection import detect_operational_anomalies

def generate_flights_csv() -> Tuple[str, str]:
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM flights ORDER BY scheduled_time ASC", conn)
    conn.close()

    output = io.StringIO()
    output.write("# TRAIT AVIATION INTELLIGENCE - OPERATIONAL FLIGHTS REPORT\n")
    output.write(f"# GENERATED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("# DISCLAIMER: SYNTHETIC DEMONSTRATION DATA FOR DEMO PURPOSES ONLY\n")
    df.to_csv(output, index=False)
    
    filename = f"trait_aviation_flights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return output.getvalue(), filename

def generate_baggage_csv() -> Tuple[str, str]:
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM baggage_operations ORDER BY id ASC", conn)
    conn.close()

    output = io.StringIO()
    output.write("# TRAIT AVIATION INTELLIGENCE - BAGGAGE OPERATIONS REPORT\n")
    output.write(f"# GENERATED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("# DISCLAIMER: SYNTHETIC DEMONSTRATION DATA FOR DEMO PURPOSES ONLY\n")
    df.to_csv(output, index=False)
    
    filename = f"trait_aviation_baggage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return output.getvalue(), filename

def generate_executive_digest_markdown() -> Tuple[str, str]:
    kpis = get_kpi_summary()
    delays = get_delay_analysis()
    anomalies = detect_operational_anomalies()

    gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report_lines = [
        "=" * 78,
        "TRAIT INNOVATION - AVIATION INTELLIGENCE EXECUTIVE SUMMARY",
        "=" * 78,
        f"Generated At: {gen_time}",
        "Data Classification: SYNTHETIC DEMONSTRATION DATA (FOR TESTING & DEMO ONLY)",
        "",
        "1. EXECUTIVE OPERATIONAL KPIs",
        "-" * 40,
        f"• On-Time Performance (OTP): {kpis.otp_percentage}% (Target: >85.0%)",
        f"• Average Flight Delay: {kpis.avg_delay_mins} minutes",
        f"• Average Aircraft Turnaround Time: {kpis.avg_turnaround_mins} minutes",
        f"• Average Security Checkpoint Wait Time: {kpis.avg_security_wait_mins} minutes",
        f"• Baggage First-Bag Delivery Time: {kpis.first_bag_avg_mins} minutes",
        f"• Mishandled Baggage Rate: {kpis.mishandled_bag_rate_per_1000} per 1,000 bags",
        f"• Active Operational Anomalies: {kpis.active_anomalies_count}",
        f"• Total Scheduled Movements Monitored: {kpis.total_flights_monitored}",
        "",
        "2. DELAY CAUSALITY BREAKDOWN",
        "-" * 40
    ]

    for cause in delays.get("causality_breakdown", []):
        report_lines.append(f"• {cause['cause']}: {cause['percentage']}% ({cause['flight_count']} flights)")

    report_lines.extend([
        "",
        "3. MACHINE LEARNING ANOMALY DETECTION (ISOLATION FOREST)",
        "-" * 40,
        f"Total Flagged Outliers: {anomalies['total_anomalies_detected']}"
    ])

    for a in anomalies.get("anomalies", [])[:5]:
        report_lines.append(f"• [{a['severity']}] {a['incident_type']} - {a['location']}: {a['description']}")

    report_lines.extend([
        "",
        "4. OPERATIONAL RECOMMENDATIONS",
        "-" * 40,
        "• Turnaround Management: Implement rapid-deployment fueling crews for international widebody departures.",
        "• Baggage Operations: Accelerate conveyor belt preventative servicing on Carousel 15 to eliminate baggage dwell spikes.",
        "• Terminal Balancing: Redirect passenger check-in overflow from Terminal 1 during morning peak hours (06:00-09:00).",
        "",
        "=" * 78,
        "END OF REPORT - TRAIT AVIATION INTELLIGENCE",
        "=" * 78
    ])

    filename = f"trait_aviation_executive_digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return "\n".join(report_lines), filename
