"""
TrackPrior AI — Dataset Cleaning Pipeline
Transforms raw datasets into clean, standardized analysis tables:
1. Cleans real observational geometry dataset (INFORMS) -> data/processed/informs_cleaned_geometry.parquet
2. Standardizes weather observations -> data/processed/weather_standardized.parquet
3. Cleans railway stations reference data -> data/processed/cleaned_stations.parquet
4. Prepares sanitized synthetic maintenance data -> data/synthetic/synthetic_cleaned_maintenance.parquet
Strictly preserves raw data without modification.
"""

import os
import sys
import numpy as np
import pandas as pd
from weather_importer import WeatherDataImporter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
DATA_SYNTHETIC = os.path.join(BASE_DIR, 'data', 'synthetic')

os.makedirs(DATA_PROCESSED, exist_ok=True)
os.makedirs(DATA_SYNTHETIC, exist_ok=True)

def clean_informs_geometry():
    print("--- [1/4] Cleaning INFORMS 2015 Real Geometry Dataset ---")
    raw_path = os.path.join(DATA_RAW, 'informs', 'informs_training_geometry.parquet')
    df = pd.read_parquet(raw_path)
    initial_rows = len(df)
    
    # 1. Drop entirely null or corrupted padding rows
    df = df.dropna(subset=['LINE_SEG_NBR', 'MILEPOST', 'DEF_PRTY', 'DFCT_TYPE']).copy()
    
    # 2. Rename columns to standardized snake_case
    rename_map = {
        'LINE_SEG_NBR': 'line_segment_id',
        'MILEPOST': 'milepost',
        'TRACK_SDTK_NBR': 'track_code',
        'TEST_DT': 'inspection_date',
        'DEF_NBR': 'defect_id',
        'GEO_CAR_NME': 'geo_car_name',
        'DEF_PRTY': 'defect_priority_tag',
        'DEF_LGTH': 'defect_length_ft',
        'DEF_AMPLTD': 'defect_amplitude_in',
        'TSC_CD': 'curve_spiral_tangent_code',
        'CLASS': 'fra_track_class',
        'TEST_FSPD': 'freight_speed_limit_mph',
        'TEST_PSPD': 'passenger_speed_limit_mph',
        'DFCT_TYPE': 'defect_type'
    }
    df = df.rename(columns=rename_map)
    
    # 3. Standardize types and clean values
    df['line_segment_id'] = df['line_segment_id'].astype(int)
    df['defect_id'] = df['defect_id'].astype(int)
    df['fra_track_class'] = pd.to_numeric(df['fra_track_class'], errors='coerce')
    df['milepost'] = pd.to_numeric(df['milepost'], errors='coerce')
    df['defect_length_ft'] = pd.to_numeric(df['defect_length_ft'], errors='coerce')
    df['defect_amplitude_in'] = pd.to_numeric(df['defect_amplitude_in'], errors='coerce')
    df['freight_speed_limit_mph'] = pd.to_numeric(df['freight_speed_limit_mph'], errors='coerce').fillna(0)
    df['passenger_speed_limit_mph'] = pd.to_numeric(df['passenger_speed_limit_mph'], errors='coerce').fillna(0)
    
    # 4. Standardize defect priority tag and create binary severity target
    df['defect_priority_tag'] = df['defect_priority_tag'].str.strip().str.upper()
    df['severity_target_binary'] = (df['defect_priority_tag'] == 'RED').astype(int)
    
    # 5. Export clean processed files
    parquet_out = os.path.join(DATA_PROCESSED, 'informs_cleaned_geometry.parquet')
    csv_out = os.path.join(DATA_PROCESSED, 'informs_cleaned_geometry.csv')
    df.to_parquet(parquet_out, index=False)
    df.to_csv(csv_out, index=False)
    
    print(f"Cleaned INFORMS Geometry: {len(df):,} valid rows (retained {len(df)/initial_rows*100:.2f}% of raw)")
    print(f"Defect Priority Breakdown: {df['defect_priority_tag'].value_counts().to_dict()}")
    print(f"Target Binary Breakdown: 0 (Yellow / Planned)={sum(df['severity_target_binary']==0):,}, 1 (Red / Urgent Safety)={sum(df['severity_target_binary']==1):,}")
    print(f"Saved to: {parquet_out}")
    return df

def clean_synthetic_maintenance():
    print("\n--- [2/4] Cleaning Synthetic Maintenance Dataset ---")
    raw_path = os.path.join(DATA_RAW, 'huggingface', 'Indian_Railway_maintenance_raw.parquet')
    df = pd.read_parquet(raw_path)
    
    # Identify track-related observations
    df['is_track_related'] = (df['failure_type'] == 'Track Defect') | (df['rail_wear_mm'] > df['rail_wear_mm'].median())
    
    # Standardize failure_severity target: None -> 0, Low -> 1, Medium -> 2, High -> 3, Critical -> 4
    severity_map = {
        None: 0,
        np.nan: 0,
        'None': 0,
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Critical': 4
    }
    df['severity_level_ordinal'] = df['failure_severity'].map(severity_map).fillna(0).astype(int)
    
    # Explicitly document and isolate leakage features
    # Note: 'risk_score' is directly computed from failure attributes and must NOT be used to predict failure severity!
    leakage_cols = ['risk_score', 'maintenance_required']
    
    # Export full cleaned synthetic dataset
    full_synth_path = os.path.join(DATA_SYNTHETIC, 'synthetic_cleaned_maintenance.parquet')
    df.to_parquet(full_synth_path, index=False)
    
    # Export track-focused subset
    track_df = df[df['failure_type'] == 'Track Defect'].copy()
    normal_df = df[df['failure_type'].isna() | (df['failure_type'] == 'None')].sample(n=len(track_df) * 2, random_state=42)
    track_subset = pd.concat([track_df, normal_df], ignore_index=True)
    
    track_subset_path = os.path.join(DATA_SYNTHETIC, 'synthetic_cleaned_track_subset.parquet')
    track_subset.to_parquet(track_subset_path, index=False)
    
    print(f"Cleaned Synthetic Maintenance dataset: {len(df):,} total rows")
    print(f"Track-focused subset: {len(track_subset):,} rows")
    print(f"Severity breakdown in track subset: {track_subset['severity_level_ordinal'].value_counts().to_dict()}")
    print(f"Saved to: {track_subset_path}")
    return track_subset

def clean_railway_stations():
    print("\n--- [3/4] Cleaning Railway Stations Reference Data ---")
    raw_path = os.path.join(DATA_RAW, 'railway_network', 'railway_stations.csv')
    df = pd.read_csv(raw_path)
    
    # Clean stations: require valid station_code and station_name
    df = df.dropna(subset=['station_code', 'station_name']).copy()
    df['station_code'] = df['station_code'].str.strip().str.upper()
    df['station_name'] = df['station_name'].str.strip()
    df['zone'] = df['zone'].fillna('UNKNOWN').str.strip().str.upper()
    
    # Coerce latitude and longitude
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # Flag stations within Indian geographic bounding box (Lat: 6 - 38, Lon: 68 - 98)
    valid_coords = (df['latitude'] >= 6.0) & (df['latitude'] <= 38.0) & (df['longitude'] >= 68.0) & (df['longitude'] <= 98.0)
    df['has_valid_india_coords'] = valid_coords
    
    out_parquet = os.path.join(DATA_PROCESSED, 'cleaned_stations.parquet')
    df.to_parquet(out_parquet, index=False)
    print(f"Cleaned Stations: {len(df):,} stations ({sum(valid_coords):,} with validated geographic coordinates)")
    print(f"Saved to: {out_parquet}")
    return df

def process_weather_data():
    print("\n--- [4/4] Processing and Standardizing Weather Template ---")
    weather_csv = os.path.join(DATA_RAW, 'weather', 'sample_weather_timeseries.csv')
    importer = WeatherDataImporter(output_dir=DATA_PROCESSED)
    std_df, audit = importer.import_weather_dataset(weather_csv, output_name='weather_standardized')
    print("Weather data processed and standardized successfully.")
    return std_df

def main():
    print("Executing TrackPrior AI Data Cleaning Pipeline...")
    clean_informs_geometry()
    clean_synthetic_maintenance()
    clean_railway_stations()
    process_weather_data()
    print("\nAll datasets cleaned and processed successfully!")

if __name__ == '__main__':
    main()
