"""
TRAIT AirportAI - Flight Guidance & Turn-by-Turn Navigation Assistant
Provides automated step-by-step navigation, gate guidance, check-in instructions, and carousel details.
"""

import re
from typing import Optional, Dict, Any, List
from app.database import get_db_connection
from app.models import FlightGuidance, NavigationStep

# Airline code: 2 uppercase chars/digits (e.g. AI, 6E, UK, BA, EK, QR) or 3 letters (e.g. AIC, BAW)
FLIGHT_PATTERN = re.compile(r"\b([A-Z]{2}|[A-Z][0-9]|[0-9][A-Z]|[A-Z]{3})\s*[- ]?\s*(\d{2,4})\b", re.IGNORECASE)


def extract_flight_number(text: str) -> Optional[str]:
    """Extracts flight number like 'AI-204', '6E 531', 'ba142', 'EK501' from text."""
    if not text:
        return None
    match = FLIGHT_PATTERN.search(text)
    if match:
        carrier = match.group(1).upper()
        digits = match.group(2)
        return f"{carrier}-{digits}"
    return None

def get_flight_record(flight_number: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    # Normalize flight number
    clean_num = flight_number.upper().replace(" ", "-")
    cursor.execute("""
        SELECT * FROM flights 
        WHERE UPPER(REPLACE(flight_number, ' ', '-')) = ?
           OR UPPER(flight_number) = ?
        LIMIT 1
    """, (clean_num, clean_num.replace("-", "")))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def generate_flight_guidance(flight_record: Dict[str, Any], lang: str = "en") -> FlightGuidance:
    f_num = flight_record["flight_number"]
    airline = flight_record["airline"]
    term = flight_record["terminal"]
    gate = flight_record["gate"]
    status = flight_record["status"]
    checkin = flight_record["checkin_desks"]
    carousel = flight_record["baggage_carousel"]
    sched = flight_record["scheduled_time"]
    est = flight_record["estimated_time"]
    delay_m = flight_record["delay_minutes"]
    delay_r = flight_record["delay_reason"]
    f_type = flight_record["flight_type"]

    steps: List[NavigationStep] = []
    tips: List[str] = []

    if f_type == "Departure":
        steps.append(NavigationStep(
            step_number=1,
            instruction=f"Arrive at {term} Departures Forecourt. Enter through Departure Gate 2 or 3.",
            distance_meters=50,
            estimated_minutes=2,
            landmark="Curbside drop-off zone"
        ))
        steps.append(NavigationStep(
            step_number=2,
            instruction=f"Locate airline counters at {checkin}. Print boarding pass or drop baggage.",
            distance_meters=80,
            estimated_minutes=4,
            landmark=f"{airline} check-in overhead display"
        ))
        steps.append(NavigationStep(
            step_number=3,
            instruction=f"Pass through {term} Central Security Screening. Empty pockets and remove laptops for X-ray.",
            distance_meters=120,
            estimated_minutes=6,
            landmark="Security checkpoint archways"
        ))
        steps.append(NavigationStep(
            step_number=4,
            instruction=f"Follow overhead directional signage towards {gate}. Use moving walkways on the main pier.",
            distance_meters=220,
            estimated_minutes=7,
            landmark="Central Duty Free / Food Court concourse"
        ))
        steps.append(NavigationStep(
            step_number=5,
            instruction=f"Arrive at {gate}. Verify your boarding zone and prepare your passport/boarding card.",
            distance_meters=60,
            estimated_minutes=2,
            landmark=f"Boarding podium at {gate}"
        ))

        tips.append(f"Boarding gates close strictly 25 minutes prior to estimated departure ({est}).")
        tips.append("DigiYatra e-gates provide automated facial-recognition entry for faster clearance.")
        if delay_m > 0:
            tips.append(f"Flight delayed by {delay_m} mins due to {delay_r}. Refreshment vouchers available at airline service desk.")
        else:
            tips.append(f"Flight operating on-time. Relax at {term} departure lounges or coffee shops.")
    else:
        # Arrival flight navigation
        steps.append(NavigationStep(
            step_number=1,
            instruction=f"Disembark aircraft at {gate} and follow the yellow 'Arrivals / Baggage Reclaim' indicators.",
            distance_meters=140,
            estimated_minutes=4,
            landmark=f"Aerobridge exit {gate}"
        ))
        steps.append(NavigationStep(
            step_number=2,
            instruction=f"Proceed through Immigration / Health clearance (if arriving from international destination).",
            distance_meters=180,
            estimated_minutes=6,
            landmark="Arrivals Concourse Level 1"
        ))
        steps.append(NavigationStep(
            step_number=3,
            instruction=f"Descend to Ground Floor Baggage Reclaim Hall. Proceed directly to {carousel}.",
            distance_meters=110,
            estimated_minutes=3,
            landmark=f"Overhead digital screen above {carousel}"
        ))
        steps.append(NavigationStep(
            step_number=4,
            instruction="Collect all checked-in bags and check tags. Proceed through Customs and exit.",
            distance_meters=70,
            estimated_minutes=2,
            landmark="Green Customs exit channel & Curbside taxi pickup"
        ))

        tips.append(f"First bag arrival estimated 15 mins after touchdown onto {carousel}.")
        tips.append("Free trolleys and porter services are available right beside the carousel.")

    return FlightGuidance(
        flight_number=f_num,
        airline=airline,
        status=status,
        terminal=term,
        gate=gate,
        checkin_desks=checkin,
        baggage_carousel=carousel,
        scheduled_time=sched,
        estimated_time=est,
        delay_minutes=delay_m,
        delay_reason=delay_r,
        navigation_steps=steps,
        quick_tips=tips
    )
