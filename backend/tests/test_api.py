import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "TRAIT Aviation Intelligence" in data["system"]

def test_airport_ai_chat_endpoint():
    # Chat with flight query
    res = client.post("/api/airport-ai/chat", json={"query": "Gate for flight AI-204", "language": "en"})
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "FLIGHT_GUIDANCE"
    assert data["flight_guidance"] is not None
    assert data["flight_guidance"]["flight_number"] == "AI-204"

def test_flight_guidance_endpoint():
    res = client.get("/api/airport-ai/flight/6E-531")
    assert res.status_code == 200
    data = res.json()
    assert data["guidance"]["airline"] == "IndiGo"
    assert data["guidance"]["terminal"] == "T1"

def test_terminals_endpoint():
    res = client.get("/api/airport-ai/terminals")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] > 0

def test_faqs_endpoint():
    res = client.get("/api/airport-ai/faqs?lang=en")
    assert res.status_code == 200
    data = res.json()
    assert len(data["faqs"]) > 0

def test_analytics_kpis():
    res = client.get("/api/analytics/kpis")
    assert res.status_code == 200
    data = res.json()
    assert data["total_flights_monitored"] > 0
    assert 0 <= data["otp_percentage"] <= 100

def test_analytics_delays():
    res = client.get("/api/analytics/delays")
    assert res.status_code == 200
    data = res.json()
    assert len(data["causality_breakdown"]) == 5

def test_analytics_anomalies():
    res = client.get("/api/analytics/anomalies")
    assert res.status_code == 200
    data = res.json()
    assert "anomalies" in data

def test_analytics_forecast():
    res = client.get("/api/analytics/forecast")
    assert res.status_code == 200
    data = res.json()
    assert len(data["points"]) > 0

def test_export_reports():
    # CSV export
    res_csv = client.get("/api/analytics/export/flights")
    assert res_csv.status_code == 200
    assert "text/csv" in res_csv.headers["content-type"]
    assert "flight_number" in res_csv.text

    # Executive digest export
    res_digest = client.get("/api/analytics/export/digest")
    assert res_digest.status_code == 200
    assert "TRAIT INNOVATION" in res_digest.text
