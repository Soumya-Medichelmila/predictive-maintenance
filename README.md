# Predictive Maintenance & Remaining Useful Life (RUL) Prediction System

> An end-to-end ML Engineering project that predicts the Remaining Useful Life of industrial turbofan engines using real sensor data — containerized with Docker, deployed on Render, and backed by a cloud PostgreSQL database.

[![Live API](https://img.shields.io/badge/Live%20API-Render-46E3B7?style=flat-square)](https://predictive-maintenance-3i1r.onrender.com)
[![Swagger Docs](https://img.shields.io/badge/Docs-Swagger%20UI-85EA2D?style=flat-square)](https://predictive-maintenance-3i1r.onrender.com/docs)
---

## Live Demo

| Resource | URL |
|---|---|
| **API** | https://predictive-maintenance-3i1r.onrender.com |
| **Swagger UI** | https://predictive-maintenance-3i1r.onrender.com/docs |
| **ReDoc** | https://predictive-maintenance-3i1r.onrender.com/redoc |
| **Database** | Render managed PostgreSQL |

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
- [Docker Setup](#docker-setup)
- [API Reference](#api-reference)
- [Example Usage](#example-usage)
- [Project Structure](#project-structure)
- [Author](#author)

---

## Overview

Traditional maintenance strategies — reactive repairs and fixed-interval preventive schedules — are costly and unreliable. This project implements **Predictive Maintenance (PdM)**: an ML-driven approach that monitors real sensor readings and estimates exactly how many operational cycles remain before a machine is likely to fail.

By predicting the **Remaining Useful Life (RUL)** of equipment, organizations can:

- Intervene *before* failures occur, not after
- Avoid unnecessary component replacements
- Significantly reduce unplanned downtime and maintenance costs

The system is trained on NASA's widely used CMAPSS turbofan engine degradation dataset, with XGBoost as the prediction engine. The application is containerized with Docker, deployed on Render with a cloud PostgreSQL database, and exposes a clean REST API via FastAPI.

---

## Key Highlights

- Built an end-to-end ML Engineering pipeline using NASA CMAPSS turbofan engine data
- Trained an XGBoost regression model achieving **MAE of 8.92 cycles**
- **Deployed on Render** with a cloud PostgreSQL database — live and publicly accessible
- **Fully containerized** with Docker and docker-compose for one-command local setup
- REST APIs built with FastAPI for real-time RUL prediction
- Integrated PostgreSQL and SQLAlchemy for persistent prediction history
- Interactive API docs via Swagger UI (OpenAPI 3.1) at `/docs` and `/redoc`
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
FastAPI REST API  ←  Docker Container
    ┌───┴────────────┐
    ▼                ▼
POST /predict    GET /history
    │                │
    ▼                ▼
Prediction       Retrieve stored
 returned        predictions
    │
    ▼
Cloud PostgreSQL  ←  SQLAlchemy ORM
(Render Managed DB)
```

---

## Features

### Machine Learning
- Regression-based RUL prediction using **XGBoost**
- Feature engineering from 21 raw sensor channels and 3 operational settings
- Model persistence via **Joblib** for zero-retraining on server restarts

### API & Backend
- **FastAPI** REST API with structured JSON responses and error handling
- Auto-generated **Swagger UI** and **ReDoc** at `/docs` and `/redoc`
- Input validation and schema enforcement via **Pydantic**

### Infrastructure & Deployment
- **Docker** containerization for consistent, reproducible environments
- **docker-compose** for one-command local setup (API + PostgreSQL together)
- **Deployed on Render** — live and publicly accessible
- **Cloud PostgreSQL** managed database on Render for persistent prediction history

### Database
- **PostgreSQL** for persistent prediction history
- **SQLAlchemy** ORM for clean, Pythonic database access
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
| Containerization | Docker + docker-compose | Reproducible environment |
| Deployment | Render | Cloud hosting |
| API Docs | Swagger UI / ReDoc | Interactive documentation |
| Version Control | Git & GitHub | Source control |

---

## Dataset

**NASA CMAPSS — Turbofan Engine Degradation Simulation Dataset**

The dataset simulates the operational lifecycle of turbofan engines under varying conditions until failure:

- **Engine operational settings** — 3 continuous variables
- **Sensor measurements** — 21 channels: temperature, pressure, speed, etc.
- **Run-to-failure trajectories** — across hundreds of engines

**RUL Target Calculation:**

```
RUL = Maximum Cycle for that Engine − Current Cycle
```

Source: [NASA Prognostics Data Repository](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository)

---

## Model Performance

| Metric | Value |
|---|---|
| **Model** | XGBoost Regressor |
| **Evaluation Metric** | Mean Absolute Error (MAE) |
| **Result** | **MAE = 8.92 cycles** |

The model predicts remaining useful life with an average error under 9 cycles — maintenance windows can be scheduled with high confidence well before actual failure.

---

## Getting Started

### Prerequisites

- Docker & docker-compose — **recommended, no other setup needed**
- OR Python 3.10+ with PostgreSQL for manual setup

### Option 1 — Docker (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Soumya-Medichelmila/predictive-maintenance.git
cd predictive-maintenance

# 2. Start API + PostgreSQL with one command
docker-compose up --build
```

API live at `http://localhost:8000`  
Swagger UI at `http://localhost:8000/docs`

### Option 2 — Manual Setup

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

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/rul_db
```

Train the model:

```bash
python app/ml/train.py
```

Start the API server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Run in detached (background) mode
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (resets the database)
docker-compose down -v
```

`docker-compose.yml` orchestrates two services: the FastAPI `api` container and a `db` PostgreSQL container with a persistent volume. No separate database installation required.

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

**Using `curl` against the live API:**

```bash
# Submit a prediction
curl -X POST https://predictive-maintenance-3i1r.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "engine_id": 1,
    "cycle": 50,
    "op_setting_1": -0.0007,
    "op_setting_2": -0.0004,
    "op_setting_3": 100.0
  }'

# Retrieve prediction history
curl https://predictive-maintenance-3i1r.onrender.com/history
```

**Using Python:**

```python
import requests

payload = {
    "engine_id": 1,
    "cycle": 50,
    "op_setting_1": -0.0007,
    "op_setting_2": -0.0004,
    "op_setting_3": 100.0
}

response = requests.post(
    "https://predictive-maintenance-3i1r.onrender.com/predict",
    json=payload
)
print(response.json())
# {'predicted_rul': 145.21}
```

---

## Project Structure

```
predictive-maintenance/
├── app/
│   ├── database/             # Database connection and session setup
│   ├── routes/               # FastAPI route definitions
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Business logic layer
│   ├── ml/
│   │   └── train.py          # Model training script
│   └── main.py               # FastAPI application entry point
├── data/
│   └── raw/
│       └── train_FD001.txt   # NASA CMAPSS dataset
├── saved_models/
│   └── rul_model.pkl         # Serialized XGBoost model (generated)
├── Dockerfile                # Container image definition
├── docker-compose.yml        # Multi-service orchestration
├── create_tables.py          # Database schema initialization
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
└── README.md
```

---

## Author

Developed as a full-stack ML Engineering project, demonstrating end-to-end proficiency across:

- **ML Engineering** — data preprocessing, feature engineering, model training & evaluation
- **MLOps** — model serialization, Docker containerization, cloud deployment on Render
- **Backend Development** — RESTful API design with FastAPI
- **Database Integration** — cloud PostgreSQL with SQLAlchemy ORM
- **Software Engineering** — clean project structure, input validation, error handling, API documentation

---

*Dataset credit: [NASA Prognostics Center of Excellence](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository)*
