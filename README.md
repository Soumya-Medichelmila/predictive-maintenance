# Predictive Maintenance & Remaining Useful Life (RUL) Prediction System

> An end-to-end Machine Learning Engineering project that predicts the Remaining Useful Life of industrial turbofan engines using real sensor data, served via a production-ready REST API backed by PostgreSQL.

---

## Table of Contents

- [Overview](#overview)
- [Key Highlights](#key-highlights)
- [Problem Statement](#problem-statement)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Dataset](#dataset)
- [Model Performance](#model-performance)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Example Usage](#example-usage)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

---

## Overview

Traditional maintenance strategies — reactive repairs and fixed-interval preventive schedules — are costly and unreliable. This project implements **Predictive Maintenance (PdM)**: an ML-driven approach that monitors real sensor readings and estimates exactly how many operational cycles remain before a machine is likely to fail.

By predicting the **Remaining Useful Life (RUL)** of equipment, organizations can:

- Intervene *before* failures occur, not after
- Avoid unnecessary component replacements
- Significantly reduce unplanned downtime and maintenance costs

The system is trained on NASA's widely used CMAPSS turbofan engine degradation dataset, with XGBoost as the prediction engine and FastAPI exposing a clean REST interface backed by PostgreSQL for persistent prediction history.

---

## Key Highlights

- Built an end-to-end Machine Learning pipeline using NASA CMAPSS turbofan engine data
- Trained an XGBoost regression model achieving **MAE of 8.92 cycles**
- Developed REST APIs using FastAPI for real-time RUL prediction
- Integrated PostgreSQL and SQLAlchemy for persistent prediction history
- Documented APIs using Swagger UI (OpenAPI 3.1)
- Version controlled and managed using Git and GitHub

---

## Problem Statement

| Strategy | Description | Drawbacks |
|---|---|---|
| **Reactive** | Fix after failure | Unplanned downtime, high emergency costs |
| **Preventive** | Maintain on fixed schedule | Unnecessary replacement, wasted resources |
| **Predictive** | Predict failure before it happens | ✅ Data-driven, cost-effective, proactive |

This project implements the predictive strategy by learning degradation patterns from historical sensor data and estimating remaining cycles for any given engine state.

---

## Architecture

```
NASA CMAPSS Dataset
        │
        ▼
Data Preprocessing & Cleaning
        │
        ▼
Feature Engineering (sensor statistics, operational settings)
        │
        ▼
RUL Label Calculation  ──  RUL = Max Cycle − Current Cycle
        │
        ▼
XGBoost Regression Model Training
        │
        ▼
Model Serialization  →  saved_models/rul_model.pkl  (Joblib)
        │
        ▼
FastAPI REST API
    ┌───┴────────────┐
    ▼                ▼
POST /predict    GET /history
    │                │
    ▼                ▼
Prediction       Retrieve stored
 returned        predictions
    │
    ▼
PostgreSQL  ←  SQLAlchemy ORM
(Prediction History)
```

---

## Features

### Machine Learning
- Regression-based RUL prediction using **XGBoost**
- Feature engineering from 21 raw sensor channels and 3 operational settings
- Model persistence via **Joblib** for zero-retraining on server restarts

### API & Backend
- **FastAPI** REST API
- Auto-generated **Swagger UI** and **ReDoc** documentation at `/docs` and `/redoc`
- Input validation and schema enforcement via **Pydantic**
- Structured JSON responses with error handling

### Database
- **PostgreSQL** for persistent prediction history
- **SQLAlchemy** ORM for clean, Pythonic database access
- Database schema initialization using **SQLAlchemy**
- Full prediction retrieval via the `/history` endpoint

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.10+ | Core runtime |
| Machine Learning | XGBoost | RUL regression |
| Data Processing | Pandas, NumPy | Feature engineering, preprocessing |
| API Framework | FastAPI | REST API server |
| Validation | Pydantic | Request/response schemas |
| Database | PostgreSQL | Prediction history storage |
| ORM | SQLAlchemy | Database interaction |
| Model Serialization | Joblib | Model save/load |
| API Docs | Swagger UI / ReDoc | Interactive documentation |
| Version Control | Git & GitHub | Source control |

---

## Dataset

**NASA CMAPSS — Turbofan Engine Degradation Simulation Dataset**

The dataset simulates the operational lifecycle of turbofan engines under varying conditions until failure. It contains:

- **Engine operational settings** (3 continuous variables)
- **Sensor measurements** (21 channels: temperature, pressure, speed, etc.)
- **Run-to-failure trajectories** across hundreds of engines

**RUL Target Calculation:**

```
RUL = Maximum Cycle for that Engine − Current Cycle
```

Source: [NASA Prognostics Data Repository](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository)
> Direct link: https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository

---

## Model Performance

| Metric | Value |
|---|---|
| **Model** | XGBoost Regressor |
| **Evaluation Metric** | Mean Absolute Error (MAE) |
| **Result** | **MAE = 8.92 cycles** |

The model predicts the remaining useful life of an engine with an average error of under 9 cycles — meaning maintenance windows can be scheduled with high confidence well before actual failure.

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (running locally or via Docker)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Soumya-Medichelmila/predictive-maintenance.git
cd predictive-maintenance

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/rul_db
```

### Train the Model

```bash
python app/ml/train.py
```

This reads the CMAPSS dataset, runs feature engineering, trains the XGBoost model, and saves it as `saved_models/rul_model.pkl`.

### Start the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API is live at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

---

## API Reference

### `POST /predict`

Submit engine sensor readings to receive a predicted RUL.

**Request Body**

```json
{
  "engine_id": 1,
  "cycle": 50,
  "op_setting_1": -0.0007,
  "op_setting_2": -0.0004,
  "op_setting_3": 100.0
}
```

**Response**

```json
{
  "predicted_rul": 145.21
}
```

**Status Codes**

| Code | Meaning |
|---|---|
| `200 OK` | Prediction successful |
| `422 Unprocessable Entity` | Invalid or missing input fields |
| `500 Internal Server Error` | Model or database error |

---

### `GET /history`

Retrieve all stored predictions from the database.

**Response**

```json
[
  {
    "id": 1,
    "engine_id": 1,
    "predicted_rul": 145.21,
    "created_at": "2026-06-11T16:02:23"
  },
  {
    "id": 2,
    "engine_id": 3,
    "predicted_rul": 72.05,
    "created_at": "2026-06-11T16:15:47"
  }
]
```

**Status Codes**

| Code | Meaning |
|---|---|
| `200 OK` | Records returned (empty array if none exist) |
| `500 Internal Server Error` | Database connection error |

---

## Example Usage

Using `curl`:

```bash
# Submit a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "engine_id": 1,
    "cycle": 50,
    "op_setting_1": -0.0007,
    "op_setting_2": -0.0004,
    "op_setting_3": 100
  }'

# Retrieve prediction history
curl http://localhost:8000/history
```

Using Python:

```python
import requests

payload = {
    "engine_id": 1,
    "cycle": 50,
    "op_setting_1": -0.0007,
    "op_setting_2": -0.0004,
    "op_setting_3": 100
}

response = requests.post("http://localhost:8000/predict", json=payload)
print(response.json())
# {'predicted_rul': 145.21}
```

---

## Screenshots

### Swagger UI — API Documentation

![Swagger UI](screenshots/swagger.png)

### Prediction History — GET /history

![History Endpoint](screenshots/history.png)

> To add these screenshots: create a `screenshots/` folder in the repo root, take screenshots from `http://localhost:8000/docs`, and save them as `swagger.png` and `history.png`.

---

## Future Enhancements

- [ ] **Docker & Docker Compose** — containerize the API, model, and database for one-command deployment
- [ ] **Cloud Deployment** — deploy to AWS/GCP/Azure with managed PostgreSQL
- [ ] **Authentication & Authorization** — API key or OAuth2-based access control
- [ ] **Model Explainability** — SHAP values to explain individual RUL predictions
- [ ] **Real-Time Sensor Streaming** — Kafka or MQTT integration for live sensor ingestion
- [ ] **Automated Retraining Pipeline** — trigger retraining when model drift is detected
- [ ] **Monitoring & Alerting** — Prometheus + Grafana dashboard for prediction drift and API health
- [ ] **Multi-Dataset Support** — extend beyond FD001 to all four CMAPSS subsets

---

## Project Structure

```
predictive-maintenance/
├── app/
│   ├── database/         # Database connection and session setup
│   ├── routes/           # FastAPI route definitions
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Business logic layer
│   ├── ml/
│   │   └── train.py      # Model training script
│   └── main.py           # FastAPI application entry point
├── data/
│   └── raw/
│       └── train_FD001.txt   # NASA CMAPSS dataset
├── saved_models/
│   └── rul_model.pkl     # Serialized XGBoost model (generated)
├── create_tables.py      # Database schema initialization
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── README.md
```

---

## Author

Developed as a full-stack Machine Learning Engineering project, demonstrating end-to-end proficiency across:

- **ML Engineering** — data preprocessing, feature engineering, model training & evaluation
- **MLOps Fundamentals** — model serialization, versioning, and serving
- **Backend Development** — RESTful API design with FastAPI
- **Database Integration** — PostgreSQL with SQLAlchemy ORM
- **Software Engineering** — clean project structure, validation, error handling

---

*Dataset credit: [NASA Prognostics Center of Excellence](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository)*
