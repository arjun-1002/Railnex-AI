"""
Unit tests for Dataset Validation and ML Preparation outputs.
"""

import os
import sys
import json
import pytest
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
DATA_SYNTHETIC = os.path.join(BASE_DIR, 'data', 'synthetic')
DATA_MANIFESTS = os.path.join(BASE_DIR, 'data', 'manifests')

def test_dataset_manifest_exists():
    manifest_path = os.path.join(DATA_MANIFESTS, 'dataset_manifest.json')
    assert os.path.exists(manifest_path)
    with open(manifest_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data['datasets_count'] == 7
    for ds in data['datasets']:
        assert ds['validation_status'] == 'PASSED'

def test_experiment_a_data_splits():
    train_path = os.path.join(DATA_PROCESSED, 'exp_a_real_train.parquet')
    test_path = os.path.join(DATA_PROCESSED, 'exp_a_real_test.parquet')
    
    assert os.path.exists(train_path)
    assert os.path.exists(test_path)
    
    df_train = pd.read_parquet(train_path)
    df_test = pd.read_parquet(test_path)
    
    # Chronological separation check: max train date < min test date
    assert df_train['inspection_date'].max() < df_test['inspection_date'].min()
    assert len(df_train) > 15000
    assert len(df_test) > 5000
    assert set(df_train['severity_target_binary'].unique()) == {0, 1}

def test_experiment_b_synthetic_data_splits():
    train_path = os.path.join(DATA_SYNTHETIC, 'exp_b_synthetic_train.parquet')
    test_path = os.path.join(DATA_SYNTHETIC, 'exp_b_synthetic_test.parquet')
    
    assert os.path.exists(train_path)
    assert os.path.exists(test_path)
    
    df_train = pd.read_parquet(train_path)
    df_test = pd.read_parquet(test_path)
    
    assert len(df_train) > 7000
    assert len(df_test) > 1800
    assert 'severity_level_ordinal' in df_train.columns
    # Check that leakage feature 'risk_score' was NOT kept as predictive input
    with open(os.path.join(DATA_MANIFESTS, 'feature_dictionary_experiment_b.json')) as f:
        f_dict = json.load(f)
    assert 'risk_score' in f_dict['excluded_leakage_features']
