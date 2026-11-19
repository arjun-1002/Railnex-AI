# Railnex AI: Project Defense & Technical Presentation

**Title:** Railnex AI — Supervised Machine Learning for Track Defect Severity Classification, TreeSHAP Feature Attribution, and Maintenance Prioritization in High-Density Railway Networks  
**Target Audience:** Capstone Defense Panel, Academic Review Board, Railway Civil Engineering Practitioners, and Research Conferences  
**Repository:** [https://github.com/arjun-1002/Railnex-AI.git](https://github.com/arjun-1002/Railnex-AI.git)  
**System Status:** Production Release (v1.1.0) | 29/29 Passing Tests | Dockerized Multi-Stage Container  

---

## Slide 1: Title & Executive Summary

### Railnex AI
**AI-Powered Permanent Way Inspection & Decision-Support Platform for Indian Railways**

- **Core Problem:** 37.4% of investigated train derailments in Indian Railways (2017–2021) stemmed from civil engineering & track defects (CAG Report No. 22 of 2022). Fixed-threshold heuristics trigger "alarm fatigue" without quantifying multivariable compound risks.
- **Our Solution:** A production-grade decision-support system integrating:
  1. Supervised Machine Learning (XGBoost Champion with **99.72% safety-critical Red Tag recall**).
  2. Native TreeSHAP game-theoretic explainability.
  3. Prognostic Remaining Useful Life (RUL) degradation velocity modeling.
  4. Statutory compliance with **Indian Railways Permanent Way Manual (IRPWM 2020 Table 5.1)**.
  5. Automated RTI TMS & Weather CSV Ingestion pipelines.
  6. Interactive "What-If" Operational Sensitivity & Climate Resilience Simulator.

---

## Slide 2: Problem Statement & National Motivation

### Why Indian Railways Needs Intelligent Track Maintenance
- **Scale of Operation:**
  - 68,000+ route km | 108,000+ running track km | 1.59 Billion tonnes of freight | 7.3 Billion passengers.
- **CAG Report No. 22 of 2022 Key Audit Findings:**
  - 1,127 derailment incidents audited over 4 years.
  - **422 incidents (37.4%)** directly caused by track geometry flaws: gauge widening, crosslevel imbalance, profile dips, and rail joint failures.
  - Track maintenance backlog and insufficient "traffic blocks" (possession windows) require surgical precision in maintenance prioritization.
- **Current Limitation in P-Way Operations:**
  - Track Recording Cars (TRC) collect data at 0.25m intervals, generating millions of data points.
  - Section Engineers (PWI / SSE) face thousands of static threshold alerts without an objective risk-rank or remaining-life forecast.

---

## Slide 3: Critical Research Finding — Target Leakage Audit

### The Pitfall of Synthetic Railway Datasets
- **The Benchmark Dilemma:**
  - Widely cited synthetic railway maintenance datasets (e.g., Hugging Face 100k defect sets) boast "100% classification accuracy."
- **Our Empirical Discovery:**
  - Rigorous cross-correlation auditing revealed extreme **target leakage** in synthetic datasets:
    $$\text{Correlation between } \texttt{risk\_score} \text{ and } \texttt{failure\_severity} = 0.887$$
  - The feature `risk_score` was computed post-hoc from the label `failure_severity`!
- **Empirical Demonstration:**
  - When leakage features (`risk_score`) are removed, synthetic classification accuracy plummets from **100% to 70.52%**.
- **Railnex AI Architectural Decision:**
  - Strict quarantine: Synthetic datasets are isolated in `data/synthetic/` solely as UI prototyping mocks.
  - **Zero leakage allowed into production models.** Champion models are trained strictly on real observational TRC telemetry.

---

## Slide 4: Data Engineering & Provenance (7 Datasets)

| Dataset ID | Dataset Name | Records / Scale | Source & Provenance | Role in Railnex AI |
|:---|:---|:---:|:---|:---|
| **DS-01** | INFORMS Real Geometry Car Archive | 23,847 records | North American Heavy-Haul Corridor (2007–2013) | **Production ML Training & Testing** |
| **DS-02** | Synthetic Defect Dataset (Quarantined) | 11,904 defects | Hugging Face synthetic benchmark | Quarantined prototype / Leakage audit study |
| **DS-03** | Indian Railway Network Geography | 8,989 stations, 5,208 routes | Open data & IR network geometries | Interactive GIS Map & Nationwide Station Search |
| **DS-04** | National Traffic & Track Statistics | 6 FY (2018–2024), 17 Zones | Railway Ministry statistical summaries | Macro network context & zonal traffic dashboards |
| **DS-05** | IRPWM 2020 Statutory Standards | 40 speed-band limits | Ministry of Railways Table 5.1 | Statutory Maintenance Advisory & Threshold Rules |
| **DS-06** | CAG Derailment Audit Database | 1,127 audit records, 5 CRS cases | CAG Report No. 22 / CRS Investigations | Historical causation benchmarking & safety validation |
| **DS-07** | Standardized Weather Time-Series | Multi-station hourly feeds | CPCB / IMD weather templates | Climate degradation & rail buckling analysis |

---

## Slide 5: Methodology — Strict Chronological Train/Test Partitioning

### Eliminating Temporal Lookahead Leakage
Standard random train/test splits (e.g., random 80/20 `train_test_split`) are fundamentally flawed in time-series and spatial degradation data because track defects at the same milepost appear in both training and test sets.

```
Time Horizon: 2007 --------------------- 2011 | 2012 -------------- 2013
               [  TRAIN SET: 17,283 records  ] | [ TEST SET: 6,564 records ]
               (5 Fiscal Years)               | (2 Fiscal Years - Out of Time)
                                              ^
                                       Split Boundary: 2012-01-01
```

- **Training Partition ($T < 2012-01-01$):** 17,283 records (72.47%)
- **Test Partition ($T \ge 2012-01-01$):** 6,564 records (27.53%)
- **Outcome:** Guarantees true out-of-time generalizability without temporal lookahead bias.

---

## Slide 6: Model Evaluation & Results

### Supervised Classification Benchmark (Out-of-Time Test Set)

| Model Architecture | Overall Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | **Critical Red Tag Recall (UML)** |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Logistic Regression (Baseline)** | 93.68% | 93.74% | 93.68% | 93.44% | 88.55% |
| **Random Forest (100 Trees)** | 98.92% | 98.93% | 98.92% | 98.92% | 99.44% |
| **XGBoost (Champion Model)** | **99.13%** | **99.14%** | **99.13%** | **99.14%** | **99.72%** |

### Safety Invariance: Critical Defect Performance
- Out of 1,799 safety-critical Red Tag (Urgent Maintenance Limit) defects in the 2-year test set:
  - **XGBoost correctly identified 1,794 defects**, missing only 5 ($Recall = 99.72\%$).
  - Zero critical defects were classified as minor.
  - The model delivers the high sensitivity required for zero-derailment tolerance.

---

## Slide 7: Explainable AI — Native TreeSHAP Game-Theoretic Attributions

### Opening the "Black Box" for Railway Permanent Way Engineers
Field engineers cannot trust an opaque probability score without engineering justification.

- **Game-Theoretic Implementation:**
  - Implemented directly via `xgboost.Booster.predict(pred_contribs=True)` for sub-millisecond overhead.
  - Computes exact marginal Shapley values satisfying efficiency, symmetry, and additivity axioms:
    $$\text{Severity Score} = \phi_0 + \sum_{i=1}^{M} \phi_i(x)$$
- **Key Empirical Attribution Findings:**
  1. **Crosslevel (XLEVEL):** Primary driver of critical derailment risk on transitions and curves.
  2. **Defect Amplitude $\times$ Track Curvature:** Non-linear interaction triggering accelerated flange climb.
  3. **Track Joint Foundation Dip (DIP):** Dominant contributor to dynamic impact loads at fishplated joints.
- **Frontend Visualization:** Live bidirectional horizontal divergence bars (Blue = stabilizing, Red = escalating risk).

---

## Slide 8: Prognostic RUL & IRPWM 2020 Statutory Compliance

### From Diagnostics to Prognostics
1. **Remaining Useful Life (RUL) Velocity Formulation:**
   $$\text{Degradation Rate } v = \frac{\Delta \delta}{\Delta t} \times \left(1 + \frac{\text{Speed}}{100}\right) \times \left(1 + \frac{\text{Curvature}}{5}\right)$$
   $$\text{Days to Critical Exceedance (RUL)} = \max\left(1, \left\lfloor \frac{\text{Threshold}_{\text{UML}} - \delta_{\text{current}}}{v} \right\rfloor\right)$$

2. **Statutory Standards Grounding (IRPWM 2020 Table 5.1):**
   - Speed Band Group A: $V \ge 130 \text{ km/h}$ (NDLS–HWH / NDLS–MMCT Rajdhani corridors).
   - Speed Band Group B: $110 \le V < 130 \text{ km/h}$.
   - Speed Band Group C: Suburban routes.
   - Speed Band Group D/E: Freight and branch lines ($V < 100 \text{ km/h}$).
   - **Automated Advisory Output:** Official Maintenance Advisory Sheet generated with Section PWI signatures, statutory urgency codes, and exact IRPWM paragraph citations.

---

## Slide 9: System Architecture & Technology Stack

### End-to-End Enterprise Full-Stack Blueprint

```
+-----------------------------------------------------------------------------------------+
|                                    REACT 18 SPA (Vite)                                   |
|   Tailwind CSS  *  Lucide Icons  *  Recharts  *  TypeScript  *  Horizontal Navbar       |
|                                                                                         |
|  [Overview]  [Track Analysis]  [Severity Prediction]  [Priority]  [Map]  [Explorer]      |
+-----------------------------------------------------------------------------------------+
                                           | HTTP / REST (Axios)
                                           v
+-----------------------------------------------------------------------------------------+
|                                  FASTAPI APPLICATION CORE                                |
|   15+ REST Endpoints  *  Pydantic Schemas  *  CORS Middleware  *  Static File Serving    |
+-----------------------------------------------------------------------------------------+
         |                                 |                                 |
         v                                 v                                 v
+------------------+             +------------------+             +----------------------+
| ML Service       |             | Data Service     |             | RTI / Weather Ingest |
| - XGBoost (Joblib)|            | - Informs CSV/Pq |             | - Multi-format Parse |
| - Native TreeSHAP|             | - 8,989 Stations |             | - Schema Validator   |
| - Prognostic RUL |             | - What-If Engine |             | - Audit Log Exporter |
+------------------+             +------------------+             +----------------------+
```

- **Frontend:** React 18, TypeScript, Tailwind CSS, Recharts, Vite (Build time: 3.3s, 689 KB gzip).
- **Backend:** FastAPI, Python 3.11, Uvicorn, Pandas, NumPy, Scikit-Learn, XGBoost, Joblib.
- **Deployment:** Multi-stage Docker container (`node:20-alpine` + `python:3.11-slim`), Render Blueprint (`render.yaml`).

---

## Slide 10: Operational Innovations & Value-Add Features

1. **RTI TMS Inspection Ingestion Engine:**
   - Pre-configured ingestion pipeline for official CRIS / Track Management System (TMS) inspection logs requested under the Right to Information (RTI) Act.
   - Robust schema normalizer converting legacy CSV/Excel columns into canonical geometry telemetry.
2. **Interactive "What-If" Operational Sensitivity Sandbox:**
   - Real-time simulation of compound operational stress:
     - Axle Load multipliers ($1.0\times$ to $1.6\times$ for Dedicated Freight Corridors).
     - Operating Train Speed adjustments ($60 \text{ km/h}$ to $160 \text{ km/h}$ for Vande Bharat corridors).
     - Monsoon Rainfall & Summer Heat ambient thermal stress coefficients.
   - Visual 12-month projected deterioration curve comparing baseline vs accelerated degradation.
3. **Nationwide Station Search & Geographic Explorer:**
   - Instant query across **8,989 Indian railway stations** and 5,208 route LineStrings.

---

## Slide 11: Robustness, Verification & Testing

### Complete Test Coverage Across All Subsystems
- **Automated Test Suite:**
  - `python -m pytest backend/tests/ TrackPrior-AI/tests/ -v`
  - **29 Passed out of 29 Tests (100% Pass Rate in 2.13s)**
- **Test Coverage Breakdown:**
  - REST API Endpoints: Health, Overview, Severity Prediction, SHAP, Prioritization, RUL Deterioration, Advisory Sheet, Search.
  - Data Validation: Dataset manifest verification, Chronological train/test split verification, Quarantined synthetic test splits.
  - Ingestion Engine: RTI TMS parsing, schema mapping, severity standardization, Weather time-series standardization, Out-of-bounds clipping, Audit logging.
  - Simulation Engine: What-If parameter sensitivity and trajectory monotonicity.
- **Enterprise Resilience:** Graceful fallbacks for Windows Application Control policies (Parquet $\rightarrow$ CSV) and strict JSON NaN sanitation.

---

## Slide 12: Conclusion & Future Outlook

### Summary of Achievements
- Successfully constructed **Railnex AI**, a mathematically sound, empirical track inspection decision-support platform.
- Uncovered and documented target leakage in widely cited public railway benchmarks ($r=0.887$).
- Delivered an out-of-time **99.72% Red Tag recall** XGBoost Champion model.
- Bridged research and field operations with IRPWM 2020 compliance, TreeSHAP explainability, and printable P-Way Maintenance Advisory generation.

### Future Roadmap
1. **RTI Data Integration:** Incorporate official CRIS/TMS field datasets upon completion of the pending RTI application.
2. **Deep Sequence Modeling:** Train Transformer / Temporal Fusion architectures on multi-year longitudinal TRC runs.
3. **Mobile P-Way Inspection PWA:** Offline-first Progressive Web App for Track Maintainers (Gangmen) and Junior Engineers in remote railway sections.

---

*Thank you! Questions and Defense Inquiries are welcome.*
