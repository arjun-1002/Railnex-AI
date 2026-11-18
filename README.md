# RAILNEX AI
## AI-Powered Railway Track Defect Severity Classification & Maintenance Prioritization System

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38b2ac.svg)](https://tailwindcss.com/)
[![Tests Passing](https://img.shields.io/badge/tests-21%2F21%20passed-brightgreen.svg)]()
[![Model Champion](https://img.shields.io/badge/XGBoost%20Champion-99.1%25%20F1-success.svg)]()

> **Railnex AI** is an intelligent railway infrastructure monitoring and maintenance decision-support platform designed primarily for the Indian Railways ecosystem.
>
> It does not replace existing Indian Railways inspection systems (such as Track Recording Cars, TMS, or OMS-2000), but builds an **intelligent analytical decision-support layer** on top of their data.

---

## 1. System Architecture

```text
Railnex-AI/
├── backend/                          # High-Performance FastAPI Decision-Support API
│   ├── app/
│   │   ├── main.py                   # App entrypoint + static SPA serving
│   │   ├── config.py                 # Paths, environment, and metadata
│   │   ├── api/
│   │   │   └── endpoints.py          # REST endpoints for all 8 core features
│   │   ├── core/
│   │   │   ├── ml_service.py         # Calibrated ML inference & IRPWM standard checks
│   │   │   ├── data_service.py       # Prioritization ranking & longitudinal trends
│   │   │   └── ...
│   │   └── schemas/
│   │       └── models.py             # Pydantic validation schemas
│   └── tests/
│       └── test_api.py               # Integration test suite (11 API tests)
│
├── frontend/                         # Modern React 18 + TypeScript + Tailwind CSS SPA
│   ├── src/
│   │   ├── components/
│   │   │   └── Header.tsx            # Minimal horizontal navigation (No vertical sidebar)
│   │   ├── pages/
│   │   │   ├── OverviewPage.tsx      # Feature 1: Central Infrastructure Dashboard
│   │   │   ├── TrackAnalysisPage.tsx # Feature 4: Longitudinal Degradation Analysis
│   │   │   ├── SeverityPredictionPage.tsx # Feature 2: Interactive ML Severity Tool
│   │   │   ├── MaintenancePriorityPage.tsx# Feature 3: Ranked Maintenance Prioritization
│   │   │   ├── NetworkMapPage.tsx    # Feature 5: Indian Railway Geography & Stations
│   │   │   ├── DataExplorerPage.tsx  # Feature 8: Paginated Inspection Data Explorer
│   │   │   ├── ModelEvaluationPage.tsx # Feature 7: Model Comparison & Explainability
│   │   │   └── SettingsPage.tsx      # Feature 6/RTI: Pipeline Governance & Weather
│   │   ├── services/api.ts           # Type-safe API client
│   │   └── types/index.ts            # Domain data structures
│   └── dist/                         # Production-optimized build bundle
│
├── models/                           # Trained Model Artifacts & Evaluation Reports
│   ├── real_best_severity_model.joblib # Trained XGBoost Champion (Weighted F1: 99.1%)
│   ├── real_feature_preprocessor.joblib# Scikit-learn Pipeline
│   ├── experiment_a_evaluation.json  # Comprehensive Real Model Benchmark Report
│   └── experiment_b_evaluation.json  # Synthetic Prototype Benchmark Report
│
├── TrackPrior-AI/                    # Core Data Engineering & Scientific Modules
│   ├── data/
│   │   ├── raw/                      # Raw immutable downloads (INFORMS, OSM, Traffic, Standards, CAG)
│   │   ├── processed/                # Standardized Parquet & CSV inspection files
│   │   ├── synthetic/                # Quarantined synthetic prototype data & disclaimer
│   │   └── manifests/                # Verified dataset manifest & feature dictionaries
│   ├── scripts/                      # Data ingestion, cleaning, validation & ML preparation
│   ├── reports/                      # DATA_AVAILABILITY_REPORT.md & high-res figures
│   └── tests/                        # Validation, RTI pipeline, & weather importer unit tests
│
├── scripts/
│   └── train_models.py               # Reproducible ML training pipeline (LogReg, RF, XGB)
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 2. Core Application Features

### Feature 1: Railway Infrastructure Dashboard (`Overview`)
- Real-time KPI summaries: Total verified inspection records (23,847), monitored line segments, critical Red Tags (6,487), planned Yellow Tags (17,360), operational railway stations (8,989).
- Defect severity breakdown, geometry channel distribution (Crosslevel 49.9%, Surface Profile 31.8%, Dip 18.3%), quarterly inspection trends, and official CAG audit derailment causation evidence.

### Feature 2: Track Defect Severity Classification (`Severity Prediction`)
- Interactive engineer tool to enter track measurements (defect length, amplitude, FRA track class, freight/passenger speed limits, curve/tangent alignment).
- Real-time ML inference returning:
  - **Predicted Class**: `Red Tag (Urgent Action Required / UML)` vs `Yellow Tag (Planned Maintenance / NBML)`.
  - **Calibrated Probabilities**: Precise class confidence distribution.
  - **Explainable Factors**: Identification of high-risk amplitude exceedance, volume perturbation, or high-speed dynamic wheel unloading.
  - **IRPWM 2020 Benchmarking**: Automated conversion and verification against Indian Railways Permanent Way Manual Table 5.1 thresholds.
  - **Engineering Presets**: Pre-loaded typical scenarios (Curve Cross-Level Exceedance, Planned Surface Profile Wear, High-Speed Track Dip).

### Feature 3: Maintenance Prioritization (`Maintenance Priority`)
- Multi-criteria ranked list of track observations requiring review:
  $$\text{Priority Score} = 0.40 \cdot P(\text{Red Tag}) + 0.35 \cdot \frac{|\text{Amplitude}|}{\text{Threshold}} + 0.15 \cdot \text{Length Extent} + 0.10 \cdot \text{Speed Exposure}$$
- Categorized into actionable urgency tiers: `CRITICAL_REVIEW`, `HIGH_PRIORITY`, and `SCHEDULED_MONITORING`.
- Filterable by urgency tier and defect type; includes **One-Click CSV Export** for field engineers.

### Feature 4: Track Deterioration Analysis (`Track Analysis`)
- Analyzes 79,069 repeated inspection runs on track line segments across 2007–2013.
- Identifies recurring defect clusters, geometry deviation growth over time, and post-tamping recovery.
- Classifies line segments by degradation pattern (`ACCELERATING DETERIORATION`, `MODERATE DEGRADATION`, `STABLE MAINTENANCE`).

### Feature 5: Railway Network Visualization (`Network Map`)
- Interactive geographic map rendering 8,989 verified Indian Railways stations across all 17 Zonal Railways (NR, WR, CR, SR, SCR, ER, ECoR, etc.).
- Station inspector with official station codes, zones, states, and WGS-84 coordinates.
- **Strict Data Verification**: Defect locations are plotted only when verified GPS tags are present.

### Feature 6: Weather Analysis & Environmental Coupling
- Standardizes weather observations (rainfall, temperature, humidity).
- **Strict Decoupling Rule**: Weather is merged with track inspections only when spatial proximity ($\le$ 25 km) and temporal window ($\pm$ 6 hours) are satisfied.

### Feature 7: Model Evaluation & Transparent AI Governance (`Model Evaluation`)
- Side-by-side benchmark comparison of **Logistic Regression**, **Random Forest**, and **XGBoost** on out-of-time test partitions.
- Confusion matrix inspection with focus on **Critical Severity Recall (Red Tag Recall)**.
- Feature importance attribution highlighting defect amplitude, defect volume, and track curvature.

### Feature 8: Data Management (`Data Explorer & Settings`)
- Paginated table of 23,847 records with instant multi-column filtering and CSV export.
- Access to the official dataset manifest, scientific data provenance, and IRPWM 2020 threshold tables.

---

## 3. Machine Learning Benchmark Results

Evaluated on out-of-time test split (6,564 records from 2012–2013; models trained on 17,283 records from 2007–2011):

| Model Algorithm | Accuracy | Precision (Red Tag) | Recall (Red Tag) | Critical Recall | Macro-F1 | Weighted-F1 | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Classifier** | **99.13%** | **97.35%** | **99.72%** | **99.72%** | **98.92%** | **99.14%** | **CHAMPION** |
| **Random Forest** | 98.83% | 96.54% | 99.28% | 99.28% | 98.54% | 98.83% | Strong Ensemble |
| **Logistic Regression** | 87.80% | 80.25% | 75.21% | 75.21% | 84.42% | 87.70% | Linear Baseline |

*Safety Takeaway: XGBoost achieved **99.72% Critical Red Tag Recall**, missing only 5 out of 1,799 severe safety exceedance defects in the test partition.*

---

## 4. Indian Railways RTI Integration Protocol

A formal application under the Right to Information (RTI) Act has been submitted requesting anonymized Track Management System (TMS) inspection and Track Recording Car (TRC) logs covering 2020–2025 across Zonal Railways.

The backend includes a dedicated ingestion engine (`TrackPrior-AI/scripts/rti_pipeline.py`) that:
- Ingests `.csv`, `.xlsx`, `.xls`, and `.parquet` files.
- Automatically handles heterogeneous column naming conventions across all 17 Zonal Railways and 68 Divisions.
- Cross-references raw measurements against the 40 verified threshold rules in **IRPWM 2020 Table 5.1** (`irpwm_geometry_thresholds.csv`).

---

## 5. Quickstart & How to Run

### 5.1 Prerequisites
- Python 3.11+
- Node.js 18+ and npm (optional for frontend development; production bundle is pre-built)

### 5.2 Option A: Launch Full-Stack Application (Zero-Config Single Command)
The FastAPI backend serves both the REST API and the pre-built React frontend:

```powershell
# 1. Install python dependencies
pip install -r requirements.txt

# 2. Start Railnex AI Server
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Open your browser to:
- **Web Application Interface:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 5.3 Option B: Development Mode (Vite Hot-Reload)
```powershell
# Terminal 1: Backend
python -m uvicorn backend.app.main:app --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm.cmd run dev
```
Open [http://localhost:3000/](http://localhost:3000/)

### 5.4 Run Complete Test Suite
```powershell
python -m pytest backend/tests/ TrackPrior-AI/tests/ -v
```

---

## 6. Statutory Limitations & Governance

- **Academic Prototype:** Railnex AI is developed as an academic machine learning research and decision-support prototype.
- **No Replacement for Field Inspection:** It must not replace official Indian Railways inspection protocols, statutory Commissioner of Railway Safety (CRS) inquiries, or permanent way rules laid down in the IRPWM.
- **Traceability:** Every prediction displays calibrated confidence, contributing factors, applicable IRPWM standards, and data origin disclaimers.
