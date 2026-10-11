# TRAIT Aviation Intelligence (v2.0)
### Next-Generation Airport Passenger Assistance & Operational Analytics Platform
**Developed for TRAIT Innovation**

> **DATA CLASSIFICATION NOTICE**:  
> **SYNTHETIC DEMONSTRATION DATA** — All flight schedules, passenger numbers, baggage turnaround metrics, and incident records contained in this application are strictly synthetic data generated for testing, prototype demonstration, and evaluation purposes only.

---

## 🛫 Executive Overview

**TRAIT Aviation Intelligence** is an enterprise-grade, integrated airport operations and passenger concierge platform engineered by **TRAIT Innovation**. It resolves key airport challenges by combining real-time passenger navigation with operational intelligence across two unified modules:

1. **TRAIT AirportAI (Passenger Assistance)**:
   - **Offline AI Passenger Concierge**: Local TF-IDF semantic vectorizer & cosine similarity knowledge retrieval over local airport knowledge base (Zero paid API cost).
   - **Turn-by-Turn Gate & Facility Guidance**: Real-time directional steps, estimated walking minutes, distances, and landmarks to gates, security, check-in rows, and baggage carousels.
   - **Flight Status & Tracker**: Instant operational lookup for flights (e.g. `AI-204`, `6E-531`, `BA-142`, `EK-501`, `UK-817`, `LH-760`).
   - **Terminal & Facility Directory**: Searchable matrix of Terminals 1, 2, and 3 covering lounges, medical centers, prayer rooms, restaurants, and inter-terminal shuttles.
   - **Multilingual Support**: Real-time language detection and localized responses in **English, Hindi (हिन्दी), Spanish (Español), French (Français), German (Deutsch), and Arabic (العربية)**.

2. **TRAIT Aviation Analytics (Operations Intelligence)**:
   - **Operational KPI Dashboard**: Live tracking of fleet On-Time Performance (OTP %), average flight delay, aircraft turnaround minutes, security wait times, and baggage delivery SLA.
   - **Flight Delay Analysis**: Breakdown by delay causality (*Carrier, Weather, NAS/ATC, Late Aircraft, Security*), delay duration histogram, and airline OTP benchmark rankings.
   - **Passenger & Baggage Throughput**: 24-hour diurnal bank flow curves (inbound vs outbound vs design capacity) and real-time reclaim carousel status monitors.
   - **Machine Learning Anomaly Detection**: Powered by **Scikit-Learn IsolationForest**, detecting turnaround bottlenecks and baggage belt dwell anomalies in real-time with severity scoring.
   - **Predictive Time Series Forecasting**: Powered by **Statsmodels Holt-Winters Exponential Smoothing (Additive Trend & 24h Seasonality)** with 95% confidence intervals (upper/lower bounds) and automated staffing recommendations.
   - **Downloadable Reports**: One-click instant exports of Flights CSV, Baggage Operations CSV, Executive Digest (.txt/.md), and Full JSON Audit State.

---

## 💻 Tech Stack & Zero-Cost Constraints

- **Budget**: **₹0** (100% open-source, offline local execution, zero paid cloud or third-party AI APIs).
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, Lucide React, Recharts.
- **Backend**: Python 3.11, FastAPI, Uvicorn, SQLite3 (WAL mode).
- **Data Science & ML**: Pandas, NumPy, Scikit-Learn (`TfidfVectorizer`, `IsolationForest`), Statsmodels (`ExponentialSmoothing`).
- **Platform**: Native Windows 10/11, Docker, Linux compatible.

---

## ⚡ Quick Start: Running Locally on Windows

### Option 1: One-Click Launch (Recommended)
Simply double-click:
```bat
run_local.bat
```
*(Or run `./start.ps1` in PowerShell)*

This automatically seeds the SQLite database and launches the unified server on `http://127.0.0.1:8000`.

### Option 2: Manual Terminal Execution

#### 1. Start the Unified Backend & Frontend:
```powershell
cd backend
python -m app.seed_data
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open your browser to: **http://127.0.0.1:8000**

#### 2. (Optional) Run Frontend in Vite Development Mode:
```powershell
cd frontend
npm run dev
```
Open your browser to: **http://localhost:5173** (API proxy automatically routes to port 8000).

---

## 🧪 Automated Test Suite Validation

The test suite validates both AirportAI NLP matching and Aviation Analytics ML models:
```powershell
cd backend
python run_tests.py
```

### Verified Test Results:
- `test_flight_extraction`: **PASSED** (IATA/ICAO regex flight number extraction)
- `test_flight_guidance`: **PASSED** (Turn-by-turn navigation steps & landmarks)
- `test_knowledge_engine`: **PASSED** (TF-IDF semantic retrieval & FAQ matching)
- `test_multilingual_detection`: **PASSED** (EN, HI, ES, FR, DE, AR script & keyword parser)
- `test_delay_analysis`: **PASSED** (Causality breakdown & airline OTP rankings)
- `test_forecasting`: **PASSED** (Statsmodels Holt-Winters 24h predictions with 95% CI bounds)
- `test_kpis`: **PASSED** (Real-time operational KPI aggregation)
- `test_ml_anomaly_detection`: **PASSED** (Scikit-Learn IsolationForest outlier detection)
- `test_passenger_baggage`: **PASSED** (Throughput aggregation & baggage dwell metrics)
- `test_api_endpoints`: **PASSED** (FastAPI REST endpoints & CSV/digest exports)

**Result**: `14 passed in 1.792s (100% SUCCESS)`

---

## ☁️ Zero-Cost Cloud Deployment Blueprints

### Free Option 1: Render Free Tier
1. Connect your GitHub repository to [Render.com](https://render.com).
2. Render detects `render.yaml` or create a new Web Service using the included `Dockerfile`.
3. Set environment variable: `PORT=8000`.
4. Deploy on Render's Free instance plan ($0/month).

### Free Option 2: Hugging Face Spaces (Docker SDK)
1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces) with **Docker SDK**.
2. Push this repository.
3. Hugging Face builds and hosts the full-stack container for free on port 7860/8000.

### Free Option 3: Docker Compose (Local / VPS)
```bash
docker compose up --build -d
```
Access at `http://localhost:8000`.

---

## 📁 Repository Directory Structure

```text
trait-aviation-intelligence/
├── backend/
│   ├── app/
│   │   ├── airport_ai/
│   │   │   ├── flight_assistant.py      # Turn-by-turn gate & flight navigator
│   │   │   ├── knowledge_engine.py      # Local TF-IDF & cosine similarity engine
│   │   │   └── multilingual.py          # Multilingual parser & localized templates
│   │   ├── aviation_analytics/
│   │   │   ├── anomaly_detection.py     # Scikit-Learn IsolationForest anomaly detector
│   │   │   ├── delay_analysis.py        # Flight delay causality & OTP service
│   │   │   ├── forecasting.py           # Statsmodels Holt-Winters time-series forecaster
│   │   │   ├── kpi_service.py           # Executive KPI aggregator
│   │   │   ├── passenger_baggage.py     # Passenger flow & baggage dwell analytics
│   │   │   └── reports.py               # CSV and executive digest export generator
│   │   ├── database.py                  # SQLite schema initialization
│   │   ├── main.py                      # FastAPI application & static server
│   │   ├── models.py                    # Pydantic schemas
│   │   └── seed_data.py                 # Synthetic demonstration data generator
│   ├── tests/                           # Unit & integration tests
│   ├── run_tests.py                     # Automated test runner
│   ├── trait_aviation.db                # SQLite database (generated)
│   └── requirements.txt                 # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── airport-ai/              # Module 1 UI components
│   │   │   ├── analytics/               # Module 2 UI components
│   │   │   └── Header.tsx               # Global navigation bar & controls
│   │   ├── services/api.ts              # Typed API client
│   │   ├── types.ts                     # TypeScript definitions
│   │   ├── App.tsx                      # Root application router
│   │   └── main.tsx                     # React entrypoint
│   ├── dist/                            # Production build assets
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── Dockerfile                           # Production multi-stage Docker build
├── docker-compose.yml                   # Docker orchestrator
├── render.yaml                          # Render zero-cost cloud blueprint
├── run_local.bat                        # Windows 1-click batch launcher
├── start.ps1                            # Windows PowerShell launcher
└── README.md                            # Documentation
```
