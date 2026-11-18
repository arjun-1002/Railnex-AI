"""
Unit tests for WeatherDataImporter module.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# Add scripts directory to path
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
sys.path.insert(0, SCRIPTS_DIR)

from weather_importer import WeatherDataImporter

def test_weather_importer_initialization(tmp_path):
    importer = WeatherDataImporter(output_dir=str(tmp_path))
    assert os.path.exists(tmp_path)

def test_weather_standardization(tmp_path):
    importer = WeatherDataImporter(output_dir=str(tmp_path))
    
    # Create test input dataframe with alias columns
    raw_df = pd.DataFrame({
        "DATE_TIME": ["2023-01-01 10:00:00", "2023-01-01 11:00:00"],
        "STN_ID": ["NDLS-01", "NDLS-01"],
        "TEMP": [25.5, 27.2],
        "RAIN": [0.0, 12.5],
        "RH": [60.0, 85.0],
        "LAT": [28.61, 28.61],
        "LON": [77.20, 77.20]
    })
    
    std_df = importer.standardize(raw_df)
    
    assert 'timestamp' in std_df.columns
    assert 'temperature_c' in std_df.columns
    assert 'rainfall_mm' in std_df.columns
    assert 'humidity_percent' in std_df.columns
    assert len(std_df) == 2
    assert std_df['temperature_c'].iloc[0] == 25.5
    assert std_df['rainfall_mm'].iloc[1] == 12.5

def test_weather_out_of_bounds_handling(tmp_path):
    importer = WeatherDataImporter(output_dir=str(tmp_path))
    
    raw_df = pd.DataFrame({
        "timestamp": ["2023-01-01 10:00:00", "2023-01-01 11:00:00"],
        "temperature_c": [25.0, 999.0],  # 999 is out of bounds
        "humidity_percent": [-10.0, 50.0]  # -10 is out of bounds
    })
    
    std_df = importer.standardize(raw_df)
    assert np.isnan(std_df['temperature_c'].iloc[1])
    assert np.isnan(std_df['humidity_percent'].iloc[0])

def test_weather_audit_generation(tmp_path):
    importer = WeatherDataImporter(output_dir=str(tmp_path))
    test_csv = tmp_path / "test_weather.csv"
    
    df = pd.DataFrame({
        "timestamp": ["2023-01-01 00:00:00", "2023-01-01 01:00:00"],
        "station_id": ["STN-1", "STN-1"],
        "temperature_c": [20.0, 21.0],
        "rainfall_mm": [0.0, 5.0],
        "humidity_percent": [50.0, 55.0]
    })
    df.to_csv(test_csv, index=False)
    
    std_df, audit = importer.import_weather_dataset(str(test_csv), output_name="test_out")
    assert audit["total_records"] == 2
    assert audit["stations_count"] == 1
    assert "temperature_c" in audit["summary_statistics"]
