from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    language: Optional[str] = "en"  # "en", "hi", "es", "fr", "de", "ar"
    flight_number: Optional[str] = None

class NavigationStep(BaseModel):
    step_number: int
    instruction: str
    distance_meters: int
    estimated_minutes: int
    landmark: Optional[str] = None

class FlightGuidance(BaseModel):
    flight_number: str
    airline: str
    status: str
    terminal: str
    gate: str
    checkin_desks: str
    baggage_carousel: str
    scheduled_time: str
    estimated_time: str
    delay_minutes: int
    delay_reason: str
    navigation_steps: List[NavigationStep] = []
    quick_tips: List[str] = []

class ChatResponse(BaseModel):
    answer: str
    detected_language: str
    intent: str
    confidence: float
    flight_guidance: Optional[FlightGuidance] = None
    facility_matches: List[Dict[str, Any]] = []
    suggested_prompts: List[str] = []
    synthetic_disclaimer: str = "SYNTHETIC DEMONSTRATION DATA - FOR TESTING & DEMO PURPOSES ONLY"

class KPISummary(BaseModel):
    otp_percentage: float
    avg_delay_mins: float
    avg_turnaround_mins: float
    avg_security_wait_mins: float
    first_bag_avg_mins: float
    mishandled_bag_rate_per_1000: float
    active_anomalies_count: int
    total_flights_monitored: int
    synthetic_disclaimer: str = "SYNTHETIC DEMONSTRATION DATA"

class DelayCausality(BaseModel):
    carrier_pct: float
    weather_pct: float
    nas_pct: float
    late_aircraft_pct: float
    security_pct: float
    total_delayed_flights: int

class AnomalyItem(BaseModel):
    id: int
    timestamp: str
    incident_type: str
    flight_number: Optional[str] = None
    location: str
    metric_name: str
    observed_value: float
    expected_range: str
    severity: str
    anomaly_score: float
    description: str
    status: str

class ForecastPoint(BaseModel):
    timestamp: str
    actual: Optional[float] = None
    predicted: Optional[float] = None
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

class ForecastResponse(BaseModel):
    metric: str
    unit: str
    points: List[ForecastPoint]
    model_name: str
    synthetic_disclaimer: str = "SYNTHETIC DEMONSTRATION DATA"
