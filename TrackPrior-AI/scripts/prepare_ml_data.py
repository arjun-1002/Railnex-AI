"""
TrackPrior AI — Machine Learning Data Preparation Pipeline
Prepares reproducible, leak-free training and testing splits for:
Experiment A: Real Track Geometry Defect Severity Classification (INFORMS)
Experiment B: Synthetic Maintenance Urgency Prototype (Hugging Face)
Builds feature dictionaries, encodes categorical variables, and fits preprocessors inside training folds.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
DATA_SYNTHETIC = os.path.join(BASE_DIR, 'data', 'synthetic')
DATA_MANIFESTS = os.path.join(BASE_DIR, 'data', 'manifests')

os.makedirs(DATA_PROCESSED, exist_ok=True)
os.makedirs(DATA_SYNTHETIC, exist_ok=True)
os.makedirs(DATA_MANIFESTS, exist_ok=True)

# ==============================================================================
# EXPERIMENT A: REAL OBSERVATIONAL TRACK GEOMETRY INSPECTION DATA
# ==============================================================================
def prepare_experiment_a():
    print("=" * 80)
    print("EXPERIMENT A — REAL OBSERVATIONAL TRACK GEOMETRY INSPECTION DATA (INFORMS)")
    print("=" * 80)
    
    informs_file = os.path.join(DATA_PROCESSED, 'informs_cleaned_geometry.parquet')
    df = pd.read_parquet(informs_file)
    
    # Feature Engineering
    df['defect_volume_proxy'] = df['defect_length_ft'] * df['defect_amplitude_in'].abs()
    df['speed_ratio'] = df['freight_speed_limit_mph'] / (df['passenger_speed_limit_mph'] + 1e-4)
    df['inspection_year'] = df['inspection_date'].dt.year
    df['inspection_month'] = df['inspection_date'].dt.month
    
    # Target definition
    # 0 = Yellow tag (Defect requiring scheduled maintenance)
    # 1 = Red tag (FRA track safety standard violation requiring immediate urgent intervention)
    target_col = 'severity_target_binary'
    
    # Predictive features
    num_features = [
        'defect_length_ft',
        'defect_amplitude_in',
        'defect_volume_proxy',
        'fra_track_class',
        'freight_speed_limit_mph',
        'passenger_speed_limit_mph',
        'speed_ratio',
        'inspection_month'
    ]
    cat_features = [
        'defect_type',
        'curve_spiral_tangent_code',
        'track_code'
    ]
    
    # Leakage-prone / identifier columns strictly excluded from model input
    leakage_and_metadata = [
        'line_segment_id',
        'milepost',
        'defect_id',
        'geo_car_name',
        'defect_priority_tag',
        'inspection_date'
    ]
    
    # Chronological Split (Train: 2007 - 2011, Test: 2012 - 2013)
    split_date = pd.Timestamp('2012-01-01')
    train_mask = df['inspection_date'] < split_date
    test_mask = df['inspection_date'] >= split_date
    
    df_train = df[train_mask].copy()
    df_test = df[test_mask].copy()
    
    print(f"Chronological Split Threshold: {split_date.strftime('%Y-%m-%d')}")
    print(f"  Training set: {len(df_train):,} rows ({df_train['inspection_date'].min().strftime('%Y-%m-%d')} to {df_train['inspection_date'].max().strftime('%Y-%m-%d')})")
    print(f"  Testing set:  {len(df_test):,} rows ({df_test['inspection_date'].min().strftime('%Y-%m-%d')} to {df_test['inspection_date'].max().strftime('%Y-%m-%d')})")
    print(f"  Train Target distribution: {df_train[target_col].value_counts().to_dict()}")
    print(f"  Test Target distribution:  {df_test[target_col].value_counts().to_dict()}")
    
    # Fit preprocessor strictly on training data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )
    
    X_train = df_train[num_features + cat_features]
    y_train = df_train[target_col]
    X_test = df_test[num_features + cat_features]
    y_test = df_test[target_col]
    
    preprocessor.fit(X_train)
    joblib.dump(preprocessor, os.path.join(DATA_PROCESSED, 'exp_a_preprocessor.joblib'))
    
    # Save splits
    train_out = os.path.join(DATA_PROCESSED, 'exp_a_real_train.parquet')
    test_out = os.path.join(DATA_PROCESSED, 'exp_a_real_test.parquet')
    df_train.to_parquet(train_out, index=False)
    df_test.to_parquet(test_out, index=False)
    
    # Feature dictionary
    feature_dict_a = {
        "experiment": "Experiment A — Real Track Geometry Defect Severity Classification",
        "dataset_source": "INFORMS 2015 Railway Applications Section Track Geometry Analytics",
        "data_nature": "Real Observational Railway Track Geometry Car Measurements",
        "target_variable": {
            "name": target_col,
            "type": "Binary Classification (Integer 0 or 1)",
            "encoding": {"0": "Yellow Tag (Pre-defect / Planned Maintenance)", "1": "Red Tag (FRA Exceedance / Urgent Action)"},
            "class_distribution_train": {int(k): int(v) for k, v in df_train[target_col].value_counts().items()},
            "class_distribution_test": {int(k): int(v) for k, v in df_test[target_col].value_counts().items()}
        },
        "split_strategy": "Chronological Split at 2012-01-01 (prevents future-to-past temporal leakage)",
        "features": {
            "numerical_features": num_features,
            "categorical_features": cat_features,
            "engineered_features": ["defect_volume_proxy", "speed_ratio", "inspection_month"]
        },
        "excluded_features": {
            "line_segment_id": "Group identifier (spatial clustering)",
            "milepost": "Spatial coordinate (prevent overfitting to exact coordinate)",
            "defect_id": "Defect transaction sequence index",
            "geo_car_name": "Inspection vehicle hardware label",
            "defect_priority_tag": "Direct string representation of target",
            "inspection_date": "Timestamp (used strictly for chronological partitioning)"
        },
        "assumptions": [
            "Dataset represents real track geometry car inspections from North American Class 1 railroad operating under FRA track safety standards 49 CFR Part 213.",
            "Yellow tags indicate geometry anomalies nearing safety thresholds but still legally permissible for scheduled maintenance.",
            "Red tags require immediate speed reduction or urgent physical track correction.",
            "Chronological splitting prevents lookahead bias and mimics real-world predictive deployment."
        ]
    }
    
    dict_a_path = os.path.join(DATA_MANIFESTS, 'feature_dictionary_experiment_a.json')
    with open(dict_a_path, 'w', encoding='utf-8') as f:
        json.dump(feature_dict_a, f, indent=2)
    print(f"Saved Feature Dictionary A: {dict_a_path}")
    return df_train, df_test

# ==============================================================================
# EXPERIMENT B: SYNTHETIC RAILWAY MAINTENANCE PROTOTYPE DATA
# ==============================================================================
def prepare_experiment_b():
    print("\n" + "=" * 80)
    print("EXPERIMENT B — SYNTHETIC RAILWAY MAINTENANCE PROTOTYPE (HUGGING FACE)")
    print("=" * 80)
    
    synth_file = os.path.join(DATA_SYNTHETIC, 'synthetic_cleaned_track_subset.parquet')
    df = pd.read_parquet(synth_file)
    
    target_col = 'severity_level_ordinal'
    
    # Predictive features (operational & track sensors)
    num_features = [
        'track_temperature_c',
        'rail_wear_mm',
        'track_vibration_level',
        'track_curvature_degree',
        'ambient_temperature_c',
        'humidity_percent',
        'rainfall_mm',
        'wind_speed_kmph',
        'train_age_years',
        'average_speed_kmph',
        'distance_travelled_km',
        'daily_trips',
        'load_factor_percent',
        'power_consumption_kw'
    ]
    
    cat_features = [
        'ballast_condition',
        'region',
        'season',
        'train_type'
    ]
    
    # Critical Leakage Columns strictly excluded!
    leakage_and_metadata = [
        'risk_score',             # LEAKAGE: Direct deterministic continuous proxy of severity
        'maintenance_required',  # LEAKAGE: Direct binary proxy of failure
        'failure_type',          # LEAKAGE: Target causality indicator
        'inspection_score',      # Post-inspection score
        'delay_minutes',         # Consequence of failure, not precursor
        'train_id',              # Identifier
        'failure_severity'       # Raw string target
    ]
    
    # Stratified Train/Test Split (80% Train, 20% Test)
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df[target_col]
    )
    
    print(f"Stratified Split (80/20):")
    print(f"  Training set: {len(train_df):,} rows")
    print(f"  Testing set:  {len(test_df):,} rows")
    print(f"  Train Target distribution: {train_df[target_col].value_counts().to_dict()}")
    print(f"  Test Target distribution:  {test_df[target_col].value_counts().to_dict()}")
    
    # Fit preprocessor on training data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )
    
    X_train = train_df[num_features + cat_features]
    preprocessor.fit(X_train)
    joblib.dump(preprocessor, os.path.join(DATA_SYNTHETIC, 'exp_b_preprocessor.joblib'))
    
    # Save splits
    train_out = os.path.join(DATA_SYNTHETIC, 'exp_b_synthetic_train.parquet')
    test_out = os.path.join(DATA_SYNTHETIC, 'exp_b_synthetic_test.parquet')
    train_df.to_parquet(train_out, index=False)
    test_df.to_parquet(test_out, index=False)
    
    # Feature dictionary
    feature_dict_b = {
        "experiment": "Experiment B — Synthetic Multi-Class Track Maintenance Urgency Prototype",
        "dataset_source": "Hugging Face (samyuktha01/Indian_Railway_maintance)",
        "data_nature": "SYNTHETIC SIMULATED DATASET — NOT OFFICIAL INDIAN RAILWAYS RECORDS",
        "disclaimer": "This experiment is strictly an algorithmic prototype and pipeline benchmark. Results must never be claimed to validate actual Indian Railways track performance.",
        "target_variable": {
            "name": target_col,
            "type": "Ordinal Multi-Class (Integer 0 to 4)",
            "encoding": {"0": "None", "1": "Low", "2": "Medium", "3": "High", "4": "Critical"},
            "class_distribution_train": {int(k): int(v) for k, v in train_df[target_col].value_counts().items()},
            "class_distribution_test": {int(k): int(v) for k, v in test_df[target_col].value_counts().items()}
        },
        "split_strategy": "Stratified Random Split (80% train, 20% test, random_state=42)",
        "features": {
            "numerical_features": num_features,
            "categorical_features": cat_features
        },
        "excluded_leakage_features": {
            "risk_score": "CRITICAL TARGET LEAKAGE: Continuous variable computed directly from failure state (r > 0.88 with severity)",
            "maintenance_required": "CRITICAL TARGET LEAKAGE: Direct binary flag indicating maintenance requirement",
            "failure_type": "TARGET LEAKAGE: Categorical failure taxonomy",
            "inspection_score": "Post-hoc evaluator score reflecting known defects",
            "delay_minutes": "Operational consequence of defect occurrence rather than predictive precursor",
            "train_id": "Row sequence identifier"
        },
        "assumptions": [
            "Dataset is purely synthetic, created for data science prototyping and code testing.",
            "Features reflect simulated physics and environment (wear, temperature, humidity).",
            "Leakage-prone columns must be rigorously omitted to avoid inflated synthetic accuracy."
        ]
    }
    
    dict_b_path = os.path.join(DATA_MANIFESTS, 'feature_dictionary_experiment_b.json')
    with open(dict_b_path, 'w', encoding='utf-8') as f:
        json.dump(feature_dict_b, f, indent=2)
    print(f"Saved Feature Dictionary B: {dict_b_path}")
    return train_df, test_df

def main():
    print("Preparing ML Datasets for TrackPrior AI Experiments...")
    prepare_experiment_a()
    prepare_experiment_b()
    print("\nPhase 4 ML Data Preparation completed successfully!")

if __name__ == '__main__':
    main()
