"""
TRAIT Aviation Intelligence - Main FastAPI Application
Integrates TRAIT AirportAI and TRAIT Aviation Analytics.
DISCLAIMER: ALL OPERATIONAL DATA IN THIS APPLICATION IS STRICTLY SYNTHETIC DEMONSTRATION DATA.
"""

import os
import io
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, JSONResponse


from app.database import init_db, get_db_connection
from app.seed_data import generate_synthetic_data
from app.models import ChatRequest, ChatResponse, KPISummary
from app.airport_ai.knowledge_engine import get_knowledge_engine
from app.airport_ai.flight_assistant import get_flight_record, generate_flight_guidance
from app.airport_ai.multilingual import SUPPORTED_LANGUAGES
from app.aviation_analytics.kpi_service import get_kpi_summary
from app.aviation_analytics.delay_analysis import get_delay_analysis
from app.aviation_analytics.passenger_baggage import get_passenger_baggage_analytics
from app.aviation_analytics.anomaly_detection import detect_operational_anomalies
from app.aviation_analytics.forecasting import forecast_passenger_and_delays
from app.aviation_analytics.reports import (
    generate_flights_csv, generate_baggage_csv, generate_executive_digest_markdown
)

# Initialize Database on startup
init_db()

app = FastAPI(
    title="TRAIT Aviation Intelligence",
    description="Integrated AirportAI Passenger Assistance & Aviation Operational Analytics Platform by TRAIT Innovation. Synthetic demonstration data only.",
    version="2.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- SYSTEM & CORE ENDPOINTS -----------------

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "system": "TRAIT Aviation Intelligence",
        "version": "2.0.0",
        "modules": ["TRAIT AirportAI", "TRAIT Aviation Analytics"],
        "disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }

@app.post("/api/reseed")
def reseed_database():
    """Reseeds the SQLite database with fresh synthetic demonstration data."""
    generate_synthetic_data()
    # Refresh TF-IDF knowledge index
    get_knowledge_engine().refresh_index()
    return {"message": "Database reseeded successfully with synthetic demonstration data."}

# ----------------- MODULE 1: TRAIT AIRPORT AI -----------------

@app.post("/api/airport-ai/chat", response_model=ChatResponse)
def airport_ai_chat(payload: ChatRequest):
    """Processes passenger questions using offline TF-IDF similarity, multilingual engine, and flight tracker."""
    engine = get_knowledge_engine()
    return engine.process_query(payload.query, user_lang=payload.language)

@app.get("/api/airport-ai/flight/{flight_number}")
def get_flight_guidance_endpoint(flight_number: str, lang: str = "en"):
    """Fetches real-time synthetic status and turn-by-turn guidance for a specific flight."""
    record = get_flight_record(flight_number)
    if not record:
        raise HTTPException(status_code=404, detail=f"Flight '{flight_number}' not found in active schedule.")
    guidance = generate_flight_guidance(record, lang=lang)
    return {
        "guidance": guidance,
        "raw_record": record,
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }

@app.get("/api/airport-ai/terminals")
def list_facilities(terminal: str = None, category: str = None):
    """Returns terminal directories, facilities, gates, check-in desks, and baggage reclaim belts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM terminals_facilities WHERE 1=1"
    params = []
    if terminal:
        query += " AND terminal = ?"
        params.append(terminal.upper())
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY terminal, category, name"
    cursor.execute(query, params)
    facilities = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {
        "facilities": facilities,
        "count": len(facilities),
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }

@app.get("/api/airport-ai/faqs")
def list_faqs(lang: str = "en"):
    """Returns all airport FAQs localized in the requested language."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faqs_knowledge ORDER BY category, topic")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    result = []
    for r in rows:
        q_field = f"question_{lang}" if f"question_{lang}" in r else "question_en"
        a_field = f"answer_{lang}" if f"answer_{lang}" in r else "answer_en"
        result.append({
            "id": r["id"],
            "topic": r["topic"],
            "category": r["category"],
            "question": r[q_field],
            "answer": r[a_field],
            "keywords": r["keywords"]
        })

    return {
        "language": lang,
        "faqs": result,
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }

@app.get("/api/airport-ai/languages")
def get_supported_languages():
    return {"languages": SUPPORTED_LANGUAGES}

# ----------------- MODULE 2: TRAIT AVIATION ANALYTICS -----------------

@app.get("/api/analytics/kpis", response_model=KPISummary)
def get_operational_kpis():
    """Fetches real-time operational executive KPIs: OTP %, turnaround, security wait, baggage time."""
    return get_kpi_summary()

@app.get("/api/analytics/delays")
def get_flight_delay_metrics():
    """Returns delay breakdown by causality (Carrier, Weather, ATC, Late Aircraft, Security) and airlines."""
    return get_delay_analysis()

@app.get("/api/analytics/passenger-baggage")
def get_passenger_and_baggage_metrics():
    """Returns hourly passenger throughput across terminals and baggage carousel dwell metrics."""
    return get_passenger_baggage_analytics()

@app.get("/api/analytics/anomalies")
def get_ml_anomalies():
    """Runs Scikit-Learn IsolationForest to detect operational anomalies in flight turnarounds and baggage dwell."""
    return detect_operational_anomalies()

@app.get("/api/analytics/forecast")
def get_predictive_forecast():
    """Runs Statsmodels ExponentialSmoothing to predict upcoming 24-48h passenger throughput and operational load."""
    return forecast_passenger_and_delays()

# ----------------- DOWNLOADABLE REPORTS -----------------

@app.get("/api/analytics/export/flights")
def export_flights_csv():
    csv_data, filename = generate_flights_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/analytics/export/baggage")
def export_baggage_csv():
    csv_data, filename = generate_baggage_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/analytics/export/digest")
def export_digest():
    text_data, filename = generate_executive_digest_markdown()
    return Response(
        content=text_data,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/analytics/export/json")
def export_full_json():
    kpis = get_kpi_summary().dict()
    delays = get_delay_analysis()
    pax_bag = get_passenger_baggage_analytics()
    anomalies = detect_operational_anomalies()
    forecast = forecast_passenger_and_delays()
    return {
        "kpis": kpis,
        "delay_analysis": delays,
        "passenger_and_baggage": pax_bag,
        "anomalies": anomalies,
        "forecast": forecast,
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA - STRICTLY FOR TESTING AND DEMO PURPOSES ONLY"
    }

# ----------------- CSV UPLOAD & DATA INGESTION -----------------

@app.post("/api/analytics/upload/flights-csv")
async def upload_flights_csv(file: UploadFile = File(...)):
    """Ingests and validates uploaded flight schedules from a CSV file into the SQLite database."""
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files (.csv) are accepted.")
    
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content), comment="#")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")

    required_cols = {"flight_number", "airline", "origin", "destination", "scheduled_time", "terminal", "gate"}
    missing = required_cols - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns in CSV: {', '.join(sorted(missing))}")

    conn = get_db_connection()
    cursor = conn.cursor()
    inserted_count = 0

    for _, row in df.iterrows():
        f_num = str(row["flight_number"]).strip().upper()
        airline = str(row.get("airline", "Unknown")).strip()
        origin = str(row.get("origin", "Delhi (DEL)")).strip()
        dest = str(row.get("destination", "Mumbai (BOM)")).strip()
        f_type = str(row.get("flight_type", "Departure")).strip()
        sched = str(row.get("scheduled_time", "")).strip()
        est = str(row.get("estimated_time", sched)).strip()
        status = str(row.get("status", "On-Time")).strip()
        term = str(row.get("terminal", "T3")).strip()
        gate = str(row.get("gate", "Gate 40")).strip()
        checkin = str(row.get("checkin_desks", "Counters 1-10")).strip()
        carousel = str(row.get("baggage_carousel", "Carousel 1")).strip()
        delay_m = int(row.get("delay_minutes", 0)) if pd.notnull(row.get("delay_minutes")) else 0
        delay_r = str(row.get("delay_reason", "None")).strip()
        aircraft = str(row.get("aircraft_type", "Airbus A320neo")).strip()
        pax = int(row.get("passengers_booked", 150)) if pd.notnull(row.get("passengers_booked")) else 150
        turnaround = int(row.get("turnaround_time_mins", 45)) if pd.notnull(row.get("turnaround_time_mins")) else 45

        cursor.execute("""
            INSERT OR REPLACE INTO flights 
            (flight_number, airline, origin, destination, flight_type, scheduled_time, estimated_time, actual_time,
             status, terminal, gate, checkin_desks, baggage_carousel, delay_minutes, delay_reason, aircraft_type,
             passengers_booked, turnaround_time_mins)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (f_num, airline, origin, dest, f_type, sched, est, est if status in ["Departed", "Landed"] else None,
              status, term, gate, checkin, carousel, delay_m, delay_r, aircraft, pax, turnaround))
        inserted_count += 1

    conn.commit()
    conn.close()

    # Refresh TF-IDF Knowledge index so newly imported flights or gates are searchable immediately
    get_knowledge_engine().refresh_index()

    return {
        "status": "success",
        "rows_imported": inserted_count,
        "filename": file.filename,
        "message": f"Successfully ingested {inserted_count} flight records into the operational database.",
        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }

# Serve frontend build if present (for single-container free deployment)

frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend_dist")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
