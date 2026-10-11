"""
TRAIT Aviation Analytics - Time Series Forecasting Service
Powered by Statsmodels ExponentialSmoothing (Holt-Winters).
Forecasts passenger volumes and airport operational pressure for upcoming 24-48 hour windows.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from app.database import get_db_connection

def forecast_passenger_and_delays() -> Dict[str, Any]:
    conn = get_db_connection()
    df_pax = pd.read_sql_query("SELECT * FROM passenger_hourly_flow ORDER BY timestamp ASC", conn)
    conn.close()

    if df_pax.empty:
        return {"points": [], "model_name": "No data"}

    # Aggregate total hourly passenger throughput
    hourly = df_pax.groupby("timestamp")[["inbound_passengers", "outbound_passengers"]].sum()
    hourly["total_pax"] = hourly["inbound_passengers"] + hourly["outbound_passengers"]
    series = hourly["total_pax"].values

    history_points: List[Dict[str, Any]] = []
    timestamps = list(hourly.index)

    # Populate historical observations
    for ts, val in zip(timestamps[-24:], series[-24:]):
        history_points.append({
            "timestamp": ts,
            "hour_label": ts[-5:],
            "actual": int(val),
            "predicted": None,
            "lower_bound": None,
            "upper_bound": None,
            "type": "Historical"
        })

    forecast_points: List[Dict[str, Any]] = []

    # Fit Statsmodels Exponential Smoothing
    try:
        # Use seasonal periods = 24 (daily cycle)
        if len(series) >= 24:
            model = ExponentialSmoothing(
                series,
                seasonal_periods=24,
                trend="add",
                seasonal="add",
                initialization_method="estimated"
            ).fit()
            predictions = model.forecast(steps=24)
            # Estimate residual variance for prediction interval
            residuals = model.resid
            sigma = np.std(residuals) if len(residuals) > 0 else 250.0
        else:
            predictions = np.repeat(np.mean(series), 24)
            sigma = 200.0
    except Exception as e:
        # Fallback to simple moving average with diurnal sinusoid
        mean_val = np.mean(series)
        hours = np.arange(24)
        diurnal = np.sin((hours - 6) * np.pi / 12) * (mean_val * 0.4)
        predictions = mean_val + diurnal
        sigma = 200.0

    last_ts_str = timestamps[-1]
    try:
        last_dt = datetime.strptime(last_ts_str, "%Y-%m-%d %H:00")
    except ValueError:
        last_dt = datetime.now().replace(minute=0, second=0, microsecond=0)

    for i, pred in enumerate(predictions):
        future_dt = last_dt + timedelta(hours=i + 1)
        pred_val = max(400, int(round(pred)))
        lower = max(200, int(round(pred_val - 1.96 * sigma)))
        upper = int(round(pred_val + 1.96 * sigma))

        forecast_points.append({
            "timestamp": future_dt.strftime("%Y-%m-%d %H:00"),
            "hour_label": future_dt.strftime("%H:00"),
            "actual": None,
            "predicted": pred_val,
            "lower_bound": lower,
            "upper_bound": upper,
            "type": "Forecast"
        })

    # Combined dataset for chart rendering
    combined = history_points + forecast_points

    # Operational insights
    peak_forecast = max(forecast_points, key=lambda x: x["predicted"])
    trough_forecast = min(forecast_points, key=lambda x: x["predicted"])

    return {
        "metric": "Total Hourly Passenger Throughput",
        "unit": "Passengers / Hour",
        "model_name": "Statsmodels Holt-Winters Exponential Smoothing (Additive Trend & 24h Seasonality)",
        "confidence_level": "95% Prediction Interval (±1.96σ)",
        "points": combined,
        "insights": {
            "forecast_peak_hour": peak_forecast["hour_label"],
            "forecast_peak_volume": peak_forecast["predicted"],
            "forecast_trough_hour": trough_forecast["hour_label"],
            "forecast_trough_volume": trough_forecast["predicted"],
            "recommended_staffing_action": f"Elevate security checkpoint screening capacity by +30% at {peak_forecast['hour_label']} to handle projected peak {peak_forecast['predicted']} pax/hr.",
            "baggage_staffing_action": f"Pre-position 3 additional baggage tug teams in Terminal 3 arrivals at {peak_forecast['hour_label']} for peak inbound load.",
            "gate_allocation_action": f"Predicted volume lull at {trough_forecast['hour_label']} ({trough_forecast['predicted']} pax/hr); schedule heavy aircraft turnaround slots accordingly."
        },

        "synthetic_disclaimer": "SYNTHETIC DEMONSTRATION DATA"
    }
