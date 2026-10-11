import pytest
from app.aviation_analytics.kpi_service import get_kpi_summary
from app.aviation_analytics.delay_analysis import get_delay_analysis
from app.aviation_analytics.passenger_baggage import get_passenger_baggage_analytics
from app.aviation_analytics.anomaly_detection import detect_operational_anomalies
from app.aviation_analytics.forecasting import forecast_passenger_and_delays

def test_kpi_summary():
    kpi = get_kpi_summary()
    assert kpi.total_flights_monitored > 0
    assert 0 <= kpi.otp_percentage <= 100
    assert kpi.avg_turnaround_mins > 0
    assert kpi.synthetic_disclaimer == "SYNTHETIC DEMONSTRATION DATA"

def test_delay_analysis():
    delays = get_delay_analysis()
    assert "causality_breakdown" in delays
    assert len(delays["causality_breakdown"]) == 5
    assert len(delays["airline_performance"]) > 0
    assert len(delays["duration_distribution"]) == 5

def test_passenger_and_baggage_analytics():
    pax_bag = get_passenger_baggage_analytics()
    assert len(pax_bag["passenger_trend"]) > 0
    assert len(pax_bag["terminal_utilization"]) > 0
    assert "baggage_summary" in pax_bag
    assert pax_bag["baggage_summary"]["total_bags"] > 0

def test_ml_anomaly_detection():
    anomalies = detect_operational_anomalies()
    assert "anomalies" in anomalies
    assert len(anomalies["anomalies"]) > 0
    assert "IsolationForest" in anomalies["model_metadata"]["algorithm"]
    assert "scatter_points" in anomalies
    assert len(anomalies["scatter_points"]) > 0

def test_time_series_forecasting():
    forecast = forecast_passenger_and_delays()
    assert len(forecast["points"]) > 0
    assert "Exponential Smoothing" in forecast["model_name"] or "ExponentialSmoothing" in forecast["model_name"]
    # Check that predictions exist and have non-null bounds
    forecast_points = [p for p in forecast["points"] if p["type"] == "Forecast"]
    assert len(forecast_points) == 24
    assert forecast_points[0]["predicted"] is not None
    assert forecast_points[0]["lower_bound"] is not None
    assert forecast_points[0]["upper_bound"] is not None
