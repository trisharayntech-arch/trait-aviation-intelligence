import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

load_dotenv()

router = APIRouter(prefix="/api/airport-ai/live-flights", tags=["Live Flights"])

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv(
    "RAPIDAPI_HOST",
    "aerodatabox.p.rapidapi.com",
)


@router.get("/{airport_code}")
async def get_live_flights(
    airport_code: str,
    flight_type: str = "arrivals",
    offset_minutes: int = 0,
    duration_minutes: int = 360,
) -> dict[str, Any]:
    """Fetch airport arrivals or departures from AeroDataBox."""

    airport_code = airport_code.upper().strip()
    flight_type = flight_type.lower().strip()

    if flight_type not in {"arrivals", "departures"}:
        raise HTTPException(
            status_code=400,
            detail="flight_type must be arrivals or departures.",
        )

    if not RAPIDAPI_KEY:
        raise HTTPException(
            status_code=503,
            detail="Flight API key is not configured on the server.",
        )

    if not 1 <= duration_minutes <= 1440:
        raise HTTPException(
            status_code=400,
            detail="duration_minutes must be between 1 and 1440.",
        )

    url = f"https://{RAPIDAPI_HOST}/flights/airports/iata/{airport_code}"

    params = {
    "offsetMinutes": offset_minutes,
    "durationMinutes": duration_minutes,
    "withLeg": "true",
    "direction": "Both",
    "withCancelled": "true",
    "withCodeshared": "true",
    "withCargo": "true",
    "withPrivate": "true",
    "withLocation": "false",
}

    headers = {
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "X-RapidAPI-Host": RAPIDAPI_HOST,
}
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code

        if status_code in {401, 403}:
            raise HTTPException(
                status_code=502,
                detail="The flight provider rejected the API credentials or access.",
            ) from exc

        if status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Flight API request limit reached. Try again later.",
            ) from exc

        raise HTTPException(
            status_code=502,
            detail=f"Flight provider returned HTTP {status_code}.",
        ) from exc

    except (httpx.RequestError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve flight data from the provider.",
        ) from exc
    
        print("AeroDataBox response type:", type(data).__name__)

    if isinstance(data, dict):
        arrivals = data.get("arrivals", [])
        departures = data.get("departures", [])

        if flight_type == "arrivals":
            flights = arrivals
        else:
            flights = departures

    elif isinstance(data, list):
        flights = data
    else:
        flights = []

    return {
        "airport": airport_code,
        "flight_type": flight_type,
        "count": len(flights),
        "flights": flights,
        "data_source": "AeroDataBox",
        "synthetic_disclaimer": (
            "Provider-supplied flight data. Availability and completeness "
            "depend on the provider."
        ),
    }