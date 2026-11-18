# TrackPrior AI — Railway Track Defect Severity Classification and Maintenance Prioritization System

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-10%2F10%20passed-brightgreen.svg)]()
[![Data Integrity](https://img.shields.io/badge/manifest-validated-success.svg)]()

> **TrackPrior AI** is an academic research engineering framework designed to predict railway track geometry defect severity and prioritize maintenance inspections using machine learning.

---

## 1. Directory Structure

```text
TrackPrior-AI/
├── data/
│   ├── raw/
│   │   ├── informs/                  # INFORMS 2015 Track Geometry archive & PDFs (Real data)
│   │   ├── huggingface/              # Hugging Face maintenance dataset (Raw synthetic)
│   │   ├── railway_network/          # OpenStreetMap railway lines GeoJSON & stations CSV
│   │   ├── traffic/                  # MoR / MoSPI national railway statistics (2018–2024)
│   │   ├── standards/                # IRPWM 2020 / RDSO verified geometry thresholds
│   │   ├── accidents/                # CAG Report 22 of 2022 derailment audit & CRS inquiries
│   │   └── weather/                  # Weather timeseries import templates
│   ├── processed/
│   │   ├── informs_cleaned_geometry.parquet # Clean real geometry observations
│   │   ├── exp_a_real_train.parquet         # Chronological train split (2007–2011)
│   │   ├── exp_a_real_test.parquet          # Chronological test split (2012–2013)
│   │   ├── cleaned_stations.parquet         # Harmonized Indian Railway stations
│   │   └── weather_standardized.parquet     # Audited weather observations
│   ├── synthetic/
│   │   ├── SYNTHETIC_DATA_DISCLAIMER.txt    # Strict disclaimer & usage rules
│   │   ├── synthetic_cleaned_track_subset.parquet # Quarantined track-defect subset
│   │   ├── exp_b_synthetic_train.parquet    # Stratified synthetic train split
│   │   └── exp_b_synthetic_test.parquet     # Stratified synthetic test split
│   └── manifests/
│       ├── dataset_manifest.json            # Machine-readable provenance & audit records
│       ├── feature_dictionary_experiment_a.json # Real experiment feature dictionary
│       └── feature_dictionary_experiment_b.json # Synthetic experiment feature dictionary
├── scripts/
│   ├── download_datasets.py          # Phase 1: Automated download & extraction
│   ├── inspect_datasets.py           # Phase 3: Data quality audit & figure generator
│   ├── clean_datasets.py             # Phase 3: Data standardization & cleaning
│   ├── validate_datasets.py          # Phase 3: Domain integrity tests & manifest builder
│   ├── prepare_ml_data.py            # Phase 4: Chronological/stratified ML partitioning
│   ├── weather_importer.py           # Phase 1/7: Modular weather import engine
│   └── rti_pipeline.py               # Phase 6: Indian Railways TMS RTI ingestion pipeline
├── reports/
│   ├── DATA_AVAILABILITY_REPORT.md   # Comprehensive dataset availability report
│   ├── DATA_QUALITY_AUDIT.json       # Numerical audit metrics for all datasets
│   └── figures/                      # High-resolution exploratory audit figures
│       ├── fig1_informs_defect_distributions.png
│       ├── fig2_synthetic_severity_and_leakage.png
│       └── fig3_zonal_network_and_derailment_causation.png
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb # Interactive walkthrough of data & thresholds
├── tests/
│   ├── test_weather_importer.py      # Unit tests for weather ingestion & validation
│   ├── test_rti_pipeline.py          # Unit tests for TMS column mapping & IRPWM limits
│   └── test_data_validation.py       # Unit tests for manifest & ML split integrity
├── requirements.txt                  # Python package dependencies
└── README.md                         # Project documentation
```

---

## 2. Dataset Provenance & Architectural Boundaries

| Dataset ID | Name | Source | Nature | Verified Records | Role in Project |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-01** | INFORMS 2015 Track Geometry | [INFORMS RAS Repository](https://connect.informs.org/railway-applications/new-item3/problem-repository16) | Real Observational Data | 23,847 rows | **Experiment A**: Primary ground-truth supervised defect severity classification (`severity_target_binary`: Yellow vs Red tag). |
| **DS-02** | Indian Railway Maintenance | [Hugging Face (`samyuktha01`)](https://huggingface.co/datasets/samyuktha01/Indian_Railway_maintance) | Synthetic Simulation | 11,904 track rows (100,300 total) | **Experiment B**: Algorithmic prototype for multi-sensor maintenance classification. Strictly quarantined. |
| **DS-03** | Indian Railway Network Geography | [DataMeet / OpenStreetMap](https://github.com/datameet/railways) | Geospatial Reference | 8,989 stations, 5,208 route lines | Spatial topology, routing, and zonal classification reference. |
| **DS-04** | Indian Railway Traffic Statistics | Ministry of Railways / MoSPI | Aggregated Statistics | 6 Fiscal Years, 17 Zones | Macro operational context (freight NTKM, passenger PKM, route km). |
| **DS-05** | Track Inspection Standards | [IRPWM 2020](https://indianrailways.gov.in/) / RDSO | Engineering Standards | 40 threshold rules | Verified engineering maintenance thresholds (PML, NBML, UML, TQI). |
| **DS-06** | Railway Accidents & Safety Audits | [CAG Report 22 of 2022](https://cag.gov.in/) / CRS | Audit / Inquiry Evidence | 1,127 derailment cases | Empirical derailment causation calibration and safety shortfall analysis. |
| **DS-07** | Weather Data Pipeline | Extensible interface | Environmental Time-Series | 240 hourly rows (template) | Modular ingestion for external weather files with spatio-temporal validation. |

---

## 3. Methodological Separation: Real vs. Synthetic Data

In accordance with machine learning best practices and engineering ethics:
1. **Never Pooled:** Synthetic data is **never** mixed into the training or validation partitions of the real geometry dataset.
2. **Experiment A (Real Observational Data):**
   - Uses real geometry car inspection recordings from INFORMS 2015.
   - Target: `severity_target_binary` (0: Yellow tag / Planned maintenance, 1: Red tag / FRA safety exceedance requiring urgent action).
   - Partitioning: **Chronological Split** at `2012-01-01`. 17,283 training rows (2007–2011) and 6,564 testing rows (2012–2013). Prevents lookahead temporal leakage.
3. **Experiment B (Synthetic Prototype):**
   - Uses Hugging Face maintenance dataset.
   - Target: `severity_level_ordinal` (0: None, 1: Low, 2: Medium, 3: High, 4: Critical).
   - Leakage Exclusion: Column `risk_score` (computed directly from failure severity with $r > 0.88$) and `maintenance_required` are strictly stripped from predictive inputs.
   - Partitioning: Stratified 80/20 train/test split (9,523 train, 2,381 test).

---

## 4. Indian Railways RTI Data Integration Protocol

The project includes an extensible TMS ingestion engine (`scripts/rti_pipeline.py`) designed to ingest future official inspection records released under the pending Right to Information (RTI) application:
- **Formats Supported:** CSV, Excel (`.xlsx`, `.xls`), and Apache Parquet.
- **Heterogeneous Schema Normalization:** Dynamic alias mapping handles varying column nomenclature across all 17 Zonal Railways and 68 Divisions.
- **Engineering Standardization:** Automatically categorizes defect measurements against the **IRPWM 2020 Table 5.1** thresholds for Broad Gauge (PML, NBML, UML).

---

## 5. Quickstart & Execution Instructions

### 5.1 Installation

Clone the repository and install dependencies in Python 3.11+:

```powershell
# Clone repository
git clone https://github.com/arjun-1002/Railnex-AI.git
cd TrackPrior-AI

# Install required packages
pip install -r requirements.txt
```

### 5.2 Execute Complete Pipeline

Run each pipeline stage sequentially:

```powershell
# Step 1: Download, extract and preserve all raw datasets
python scripts/download_datasets.py

# Step 2: Run data quality audit and generate figures
python scripts/inspect_datasets.py

# Step 3: Clean and standardize observations
python scripts/clean_datasets.py

# Step 4: Validate domain schemas and build dataset manifest
python scripts/validate_datasets.py

# Step 5: Prepare leak-free ML train/test splits and feature dictionaries
python scripts/prepare_ml_data.py

# Step 6: Run full test suite
python -m pytest tests/ -v
```

### 5.3 Import Weather Data

To import your existing historical weather file:

```powershell
python scripts/weather_importer.py --file "path/to/your_weather.csv" --out-name "historical_weather_clean"
```

### 5.4 Ingest Future RTI TMS Records

When official TMS records are received:

```powershell
python scripts/rti_pipeline.py --file "path/to/tms_inspection_records.xlsx" --out-dir "data/processed"
```

---

## 6. Reports & Verification Deliverables

- Detailed availability report: [reports/DATA_AVAILABILITY_REPORT.md](reports/DATA_AVAILABILITY_REPORT.md)
- Machine-readable manifest: [data/manifests/dataset_manifest.json](data/manifests/dataset_manifest.json)
- Feature Dictionary A (Real): [data/manifests/feature_dictionary_experiment_a.json](data/manifests/feature_dictionary_experiment_a.json)
- Feature Dictionary B (Synthetic): [data/manifests/feature_dictionary_experiment_b.json](data/manifests/feature_dictionary_experiment_b.json)
- Quality figures: [reports/figures/](reports/figures/)
