"""
TRAIT Aviation Intelligence - Automated Test Runner
Runs comprehensive test suites across AirportAI and Aviation Analytics using Python's standard library unittest.
"""

import unittest
import sys
import os
import io


# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app
from app.airport_ai.multilingual import detect_language, SUPPORTED_LANGUAGES
from app.airport_ai.flight_assistant import extract_flight_number, get_flight_record, generate_flight_guidance
from app.airport_ai.knowledge_engine import KnowledgeEngine
from app.aviation_analytics.kpi_service import get_kpi_summary
from app.aviation_analytics.delay_analysis import get_delay_analysis
from app.aviation_analytics.passenger_baggage import get_passenger_baggage_analytics
from app.aviation_analytics.anomaly_detection import detect_operational_anomalies
from app.aviation_analytics.forecasting import forecast_passenger_and_delays

class TestAirportAI(unittest.TestCase):
    def test_multilingual_detection(self):
        self.assertEqual(detect_language("उड़ान AI-204 की स्थिति क्या है?"), "hi")
        self.assertEqual(detect_language("dónde está la puerta de embarque"), "es")
        self.assertEqual(detect_language("où sont mes bagages"), "fr")
        self.assertEqual(detect_language("wo ist das flugsteig"), "de")
        self.assertEqual(detect_language("أين بوابة الصعود للرحلة"), "ar")
        self.assertEqual(detect_language("Where is Gate 24B?"), "en")

    def test_flight_extraction(self):
        self.assertEqual(extract_flight_number("Status for AI-204 please"), "AI-204")
        self.assertEqual(extract_flight_number("Where is flight 6E 531?"), "6E-531")
        self.assertEqual(extract_flight_number("Flight BA142 delay"), "BA-142")
        self.assertIsNone(extract_flight_number("Hello there"))

    def test_flight_guidance(self):
        record = get_flight_record("AI-204")
        self.assertIsNotNone(record)
        self.assertEqual(record["flight_number"], "AI-204")
        self.assertEqual(record["terminal"], "T3")

        guidance = generate_flight_guidance(record, lang="en")
        self.assertTrue(len(guidance.navigation_steps) > 0)
        self.assertEqual(guidance.flight_number, "AI-204")
        self.assertIn("Gate", guidance.gate)

    def test_knowledge_engine(self):
        engine = KnowledgeEngine()
        res_flight = engine.process_query("What is the gate for flight AI-204?", user_lang="en")
        self.assertEqual(res_flight.intent, "FLIGHT_GUIDANCE")
        self.assertIsNotNone(res_flight.flight_guidance)

        res_bag = engine.process_query("What is the baggage weight allowance for domestic flights?", user_lang="en")
        self.assertTrue("Baggage" in res_bag.intent or res_bag.confidence > 0.15)
        self.assertTrue("7kg" in res_bag.answer or "15kg" in res_bag.answer)

class TestAviationAnalytics(unittest.TestCase):
    def test_kpis(self):
        kpi = get_kpi_summary()
        self.assertGreater(kpi.total_flights_monitored, 0)
        self.assertTrue(0 <= kpi.otp_percentage <= 100)
        self.assertGreater(kpi.avg_turnaround_mins, 0)

    def test_delay_analysis(self):
        delays = get_delay_analysis()
        self.assertIn("causality_breakdown", delays)
        self.assertEqual(len(delays["causality_breakdown"]), 5)
        self.assertGreater(len(delays["airline_performance"]), 0)

    def test_passenger_baggage(self):
        pax_bag = get_passenger_baggage_analytics()
        self.assertGreater(len(pax_bag["passenger_trend"]), 0)
        self.assertGreater(len(pax_bag["terminal_utilization"]), 0)
        self.assertGreater(pax_bag["baggage_summary"]["total_bags"], 0)

    def test_ml_anomaly_detection(self):
        anomalies = detect_operational_anomalies()
        self.assertIn("anomalies", anomalies)
        self.assertGreater(len(anomalies["anomalies"]), 0)
        self.assertIn("IsolationForest", anomalies["model_metadata"]["algorithm"])
        self.assertGreater(len(anomalies["scatter_points"]), 0)

    def test_forecasting(self):
        forecast = forecast_passenger_and_delays()
        self.assertGreater(len(forecast["points"]), 0)
        self.assertIn("Exponential Smoothing", forecast["model_name"])
        forecast_pts = [p for p in forecast["points"] if p["type"] == "Forecast"]
        self.assertEqual(len(forecast_pts), 24)
        self.assertIsNotNone(forecast_pts[0]["predicted"])


class TestFastAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "healthy")

    def test_airport_ai_chat(self):
        res = self.client.post("/api/airport-ai/chat", json={"query": "Gate for flight AI-204", "language": "en"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["intent"], "FLIGHT_GUIDANCE")

    def test_flight_guidance(self):
        res = self.client.get("/api/airport-ai/flight/6E-531")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["guidance"]["airline"], "IndiGo")

    def test_analytics_endpoints(self):
        res_kpi = self.client.get("/api/analytics/kpis")
        self.assertEqual(res_kpi.status_code, 200)
        
        res_delays = self.client.get("/api/analytics/delays")
        self.assertEqual(res_delays.status_code, 200)

        res_anom = self.client.get("/api/analytics/anomalies")
        self.assertEqual(res_anom.status_code, 200)

        res_fore = self.client.get("/api/analytics/forecast")
        self.assertEqual(res_fore.status_code, 200)

    def test_exports(self):
        res_csv = self.client.get("/api/analytics/export/flights")
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn("text/csv", res_csv.headers["content-type"])

        res_digest = self.client.get("/api/analytics/export/digest")
        self.assertEqual(res_digest.status_code, 200)
        self.assertIn("TRAIT INNOVATION", res_digest.text)

    def test_multilingual_semantic_faq(self):
        # Test Hindi semantic matching with Unicode tokenization
        res = self.client.post("/api/airport-ai/chat", json={"query": "सामान की सीमा क्या है?", "language": "hi"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["detected_language"], "hi")
        self.assertEqual(res.json()["intent"], "FAQ_BAGGAGE")
        self.assertTrue(res.json()["confidence"] >= 0.15)

    def test_empty_query_handling(self):
        res = self.client.post("/api/airport-ai/chat", json={"query": "   ", "language": "en"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["intent"], "GREETING")

    def test_csv_upload_valid(self):
        csv_content = (
            "flight_number,airline,origin,destination,flight_type,scheduled_time,estimated_time,status,terminal,gate,checkin_desks,baggage_carousel,delay_minutes,delay_reason,aircraft_type,passengers_booked,turnaround_time_mins\n"
            "AI-999,Air India,Delhi (DEL),London (LHR),Departure,2026-10-15 14:00,2026-10-15 14:00,On-Time,T3,Gate 48,Row E (Counters 41-45),Carousel 9,0,None,Boeing 787-9,240,55\n"
        )
        files = {"file": ("test_schedule.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
        res = self.client.post("/api/analytics/upload/flights-csv", files=files)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")
        self.assertEqual(res.json()["rows_imported"], 1)

        # Verify immediate database persistence and lookup
        flight_res = self.client.get("/api/airport-ai/flight/AI-999")
        self.assertEqual(flight_res.status_code, 200)
        self.assertEqual(flight_res.json()["guidance"]["flight_number"], "AI-999")
        self.assertEqual(flight_res.json()["guidance"]["terminal"], "T3")

    def test_csv_upload_invalid(self):
        # Missing required columns
        invalid_csv = "bad_col_1,bad_col_2\nval1,val2\n"
        files = {"file": ("invalid.csv", io.BytesIO(invalid_csv.encode("utf-8")), "text/csv")}
        res = self.client.post("/api/analytics/upload/flights-csv", files=files)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Missing required columns", res.json()["detail"])

        # Invalid file extension
        files_txt = {"file": ("invalid.txt", io.BytesIO(b"hello"), "text/plain")}
        res_txt = self.client.post("/api/analytics/upload/flights-csv", files=files_txt)
        self.assertEqual(res_txt.status_code, 400)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
