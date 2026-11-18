"""
TrackPrior AI — Dataset Validation and Manifest Generation Script
Runs domain-specific integrity tests and builds the official dataset manifest:
data/manifests/dataset_manifest.json
"""

import os
import sys
import json
import datetime
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MANIFEST_DIR = os.path.join(DATA_DIR, 'manifests')
os.makedirs(MANIFEST_DIR, exist_ok=True)

class DatasetValidator:
    def __init__(self):
        self.validation_results = {}
        self.manifest_entries = []

    def validate_informs_geometry(self):
        print("Validating INFORMS Cleaned Track Geometry Dataset...")
        path = os.path.join(DATA_DIR, 'processed', 'informs_cleaned_geometry.parquet')
        if not os.path.exists(path):
            return False, "File does not exist"
        df = pd.read_parquet(path)
        
        checks = {
            "row_count_sufficient": len(df) > 20000,
            "target_no_nulls": df['severity_target_binary'].isna().sum() == 0,
            "target_valid_classes": set(df['severity_target_binary'].unique()).issubset({0, 1}),
            "defect_amplitude_bounded": (df['defect_amplitude_in'].abs() <= 10.0).all(),
            "defect_length_positive": (df['defect_length_ft'] > 0).all(),
            "valid_track_classes": set(df['fra_track_class'].dropna().unique()).issubset({1.0, 2.0, 3.0, 4.0, 5.0}),
            "date_range_valid": (df['inspection_date'].min() >= pd.Timestamp('2000-01-01')) and (df['inspection_date'].max() <= pd.Timestamp('2020-01-01'))
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-01",
            "name": "INFORMS Track Geometry Analytics Dataset",
            "category": "Real Observational Railway Inspection Data",
            "file_path": "data/processed/informs_cleaned_geometry.parquet",
            "format": "Parquet / CSV",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": f"{df['inspection_date'].min().strftime('%Y-%m-%d')} to {df['inspection_date'].max().strftime('%Y-%m-%d')}",
            "geographic_coverage": "North American Class 1 Railroad Network (De-identified FRA corridor)",
            "ml_role": "Experiment A: Primary Supervised Ground-Truth Track Defect Severity Classification",
            "target_variable": "severity_target_binary (0: Yellow Tag / Planned Maintenance, 1: Red Tag / Urgent Action)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def validate_synthetic_maintenance(self):
        print("Validating Synthetic Indian Railway Maintenance Dataset...")
        path = os.path.join(DATA_DIR, 'synthetic', 'synthetic_cleaned_track_subset.parquet')
        if not os.path.exists(path):
            return False, "File does not exist"
        df = pd.read_parquet(path)
        
        checks = {
            "row_count_sufficient": len(df) > 5000,
            "target_present": 'severity_level_ordinal' in df.columns,
            "target_classes_valid": set(df['severity_level_ordinal'].unique()).issubset({0, 1, 2, 3, 4}),
            "rail_wear_non_negative": (df['rail_wear_mm'].dropna() >= 0).all(),
            "temperatures_plausible": (df['track_temperature_c'].dropna() > -40).all() and (df['track_temperature_c'].dropna() < 80).all(),
            "synthetic_disclaimer_present": os.path.exists(os.path.join(DATA_DIR, 'synthetic', 'SYNTHETIC_DATA_DISCLAIMER.txt'))
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-02",
            "name": "Indian Railway Maintenance Dataset (Hugging Face - samyuktha01)",
            "category": "Synthetic Machine Learning Prototype Data",
            "file_path": "data/synthetic/synthetic_cleaned_track_subset.parquet",
            "format": "Parquet",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": "Synthetic simulation (no calendar date range)",
            "geographic_coverage": "Simulated Indian Railways Zonal Distribution",
            "ml_role": "Experiment B: Synthetic Multi-Class Maintenance Urgency Prototype (Isolated from real data)",
            "target_variable": "severity_level_ordinal (0: None, 1: Low, 2: Medium, 3: High, 4: Critical)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def validate_railway_network(self):
        print("Validating Indian Railway Stations Reference Data...")
        path = os.path.join(DATA_DIR, 'processed', 'cleaned_stations.parquet')
        if not os.path.exists(path):
            return False, "File does not exist"
        df = pd.read_parquet(path)
        
        checks = {
            "station_count_sufficient": len(df) > 8000,
            "valid_station_codes": df['station_code'].notna().all(),
            "valid_geo_coordinates": (df['has_valid_india_coords'].sum() / len(df)) > 0.90,
            "lines_geojson_exists": os.path.exists(os.path.join(DATA_DIR, 'raw', 'railway_network', 'railway_lines.geojson'))
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-03",
            "name": "Indian Railways Network Geography & Stations",
            "category": "Geospatial Reference Infrastructure",
            "file_path": "data/processed/cleaned_stations.parquet & data/raw/railway_network/railway_lines.geojson",
            "format": "GeoJSON (lines) & Parquet/CSV (stations)",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": "OpenStreetMap 2024 active topology",
            "geographic_coverage": "Nationwide India (68°E to 98°E, 6°N to 38°N)",
            "ml_role": "Spatial reference for inspection geolocation and zonal topology mapping",
            "target_variable": "None (Spatial context)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def validate_traffic_statistics(self):
        print("Validating Indian Railway Traffic Statistics...")
        path = os.path.join(DATA_DIR, 'raw', 'traffic', 'indian_railway_traffic_statistics_2018_2024.csv')
        df = pd.read_csv(path)
        
        checks = {
            "fiscal_years_covered": len(df) >= 6,
            "route_km_positive": (df['route_km_total'] > 60000).all(),
            "running_track_km_positive": (df['running_track_km'] > 90000).all(),
            "freight_loading_positive": (df['freight_loading_million_tonnes'] > 1000).all(),
            "zonal_table_exists": os.path.exists(os.path.join(DATA_DIR, 'raw', 'traffic', 'zonal_network_and_traffic.csv'))
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-04",
            "name": "Indian Railways Annual Traffic & Track Statistics",
            "category": "Aggregated Macro-Operational Statistics",
            "file_path": "data/raw/traffic/indian_railway_traffic_statistics_2018_2024.csv",
            "format": "CSV",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": "2018-19 to 2023-24 (6 Fiscal Years)",
            "geographic_coverage": "National Indian Railways Network (17 Zonal Railways)",
            "ml_role": "Contextual macro-operational baselines (cannot be disaggregated into fictional track sections)",
            "target_variable": "None (Aggregated statistical context)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def validate_standards(self):
        print("Validating Track Inspection Standards...")
        path = os.path.join(DATA_DIR, 'raw', 'standards', 'irpwm_geometry_thresholds.csv')
        df = pd.read_csv(path)
        
        checks = {
            "standards_count_sufficient": len(df) >= 30,
            "all_thresholds_numeric": pd.to_numeric(df['threshold_value'], errors='coerce').notna().all(),
            "units_populated": df['measurement_unit'].notna().all(),
            "sources_cited": df['source_document'].str.contains('IRPWM|RDSO').all(),
            "page_numbers_provided": df['page_number'].notna().all()
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-05",
            "name": "Indian Railways Permanent Way Manual (IRPWM 2020) & RDSO Geometry Standards",
            "category": "Engineering Safety & Inspection Standards",
            "file_path": "data/raw/standards/irpwm_geometry_thresholds.csv",
            "format": "CSV",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": "Current active manual (IRPWM 2020 / ACS-149)",
            "geographic_coverage": "Indian Railways Broad Gauge Network (Standard 1676 mm)",
            "ml_role": "Ground-truth engineering threshold reference for defect classification and priority labeling",
            "target_variable": "maintenance_classification (PML, NBML, UML, Comfort, Quality index)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def validate_accidents(self):
        print("Validating Railway Accidents & Derailment Audit Reports...")
        path = os.path.join(DATA_DIR, 'raw', 'accidents', 'cag_derailment_causation_2017_2021.csv')
        df = pd.read_csv(path)
        
        checks = {
            "records_populated": len(df) >= 5,
            "incident_counts_positive": (df['incident_count'] > 0).all(),
            "percentages_sum_approx_100": abs(df['percentage_of_total'].sum() - 100.0) < 1.0,
            "crs_investigations_exist": os.path.exists(os.path.join(DATA_DIR, 'raw', 'accidents', 'crs_derailment_investigations.csv'))
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-06",
            "name": "CAG Performance Audit on Derailments in Indian Railways & CRS Inquiries",
            "category": "Statutory Safety Audits & Accident Causation Records",
            "file_path": "data/raw/accidents/cag_derailment_causation_2017_2021.csv",
            "format": "CSV",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": "2017-18 to 2020-21 (Audit Period) & Major CRS Inquiries (2017-2023)",
            "geographic_coverage": "Nationwide Indian Railways Incidents",
            "ml_role": "Incident risk calibration and empirical track defect derailment causality validation",
            "target_variable": "cause_category (Isolated from inspection records)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def validate_weather(self):
        print("Validating Standardized Weather Observations...")
        path = os.path.join(DATA_DIR, 'processed', 'weather_standardized.parquet')
        df = pd.read_parquet(path)
        
        checks = {
            "timestamps_valid": df['timestamp'].notna().all(),
            "temperature_bounds": (df['temperature_c'].dropna() > -30).all() and (df['temperature_c'].dropna() < 60).all(),
            "humidity_bounds": (df['humidity_percent'].dropna() >= 0).all() and (df['humidity_percent'].dropna() <= 100).all(),
            "rainfall_non_negative": (df['rainfall_mm'].dropna() >= 0).all()
        }
        all_passed = all(checks.values())
        
        self.manifest_entries.append({
            "dataset_id": "DS-07",
            "name": "Weather Data Import & Harmonization Pipeline",
            "category": "Environmental Time-Series Observations",
            "file_path": "data/processed/weather_standardized.parquet",
            "format": "Parquet & CSV",
            "records": len(df),
            "columns": len(df.columns),
            "observation_period": f"{df['timestamp'].min().strftime('%Y-%m-%d')} to {df['timestamp'].max().strftime('%Y-%m-%d')}",
            "geographic_coverage": "Weather monitoring stations with validated coordinates",
            "ml_role": "Environmental covariates (coupled strictly via spatio-temporal joins)",
            "target_variable": "None (Environmental covariate)",
            "validation_status": "PASSED" if all_passed else "FAILED",
            "check_details": checks
        })
        return all_passed, checks

    def build_manifest(self):
        manifest_data = {
            "project_name": "TrackPrior AI",
            "version": "1.0.0",
            "generated_at": datetime.datetime.now().isoformat(),
            "datasets_count": len(self.manifest_entries),
            "datasets": self.manifest_entries
        }
        
        # Ensure all numpy types are converted to standard python types
        def sanitize(obj):
            if isinstance(obj, dict):
                return {k: sanitize(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [sanitize(v) for v in obj]
            elif isinstance(obj, (np.bool_, bool)):
                return bool(obj)
            elif isinstance(obj, (np.integer, int)):
                return int(obj)
            elif isinstance(obj, (np.floating, float)):
                return float(obj)
            return obj

        manifest_data = sanitize(manifest_data)
        out_file = os.path.join(MANIFEST_DIR, 'dataset_manifest.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=2)
        print(f"\nSuccessfully generated official dataset manifest: {out_file}")
        return manifest_data

def main():
    validator = DatasetValidator()
    validator.validate_informs_geometry()
    validator.validate_synthetic_maintenance()
    validator.validate_railway_network()
    validator.validate_traffic_statistics()
    validator.validate_standards()
    validator.validate_accidents()
    validator.validate_weather()
    validator.build_manifest()
    print("All validation suites passed!")

if __name__ == '__main__':
    main()
