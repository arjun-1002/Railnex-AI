"""
Unit tests for RTIIndianRailwaysTMSPipeline module.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
sys.path.insert(0, SCRIPTS_DIR)

from rti_pipeline import RTIIndianRailwaysTMSPipeline

def test_rti_pipeline_initialization():
    pipeline = RTIIndianRailwaysTMSPipeline()
    assert pipeline.standards_df is not None
    assert len(pipeline.standards_df) >= 30

def test_rti_schema_mapping(tmp_path):
    pipeline = RTIIndianRailwaysTMSPipeline()
    
    # Simulate a raw zonal TMS sheet with idiosyncratic column names
    raw_zonal_df = pd.DataFrame({
        "RLY_DIV": ["Delhi", "Delhi"],
        "SEC_NAME": ["NDLS-GZB", "NDLS-GZB"],
        "TRACK": ["UP Main", "DN Main"],
        "FROM_KM": [12.45, 18.20],
        "TEST_DATE": ["2024-03-15", "2024-03-15"],
        "PARAM_NAME": ["Track Twist", "Track Gauge (Slack)"],
        "AMPLITUDE": [4.8, 11.2],
        "CATEGORY": ["URGENT", "URGENT"]
    })
    
    mapped_df, missing = pipeline.map_columns(raw_zonal_df)
    
    assert mapped_df['division'].iloc[0] == "Delhi"
    assert mapped_df['block_section'].iloc[0] == "NDLS-GZB"
    assert mapped_df['km_start'].iloc[0] == 12.45
    assert mapped_df['geometry_parameter'].iloc[0] == "Track Twist"
    assert mapped_df['measured_value'].iloc[0] == 4.8

def test_rti_severity_standardization():
    pipeline = RTIIndianRailwaysTMSPipeline()
    
    df = pd.DataFrame({
        "geometry_parameter": ["Track Twist", "Track Gauge (Slack)", "Alignment Peak", "Normal Condition"],
        "measured_value": [4.5, 12.0, 3.0, 1.0],
        "tms_defect_category": ["UML", "CRITICAL", "NBML", "NORMAL"]
    })
    
    std_df = pipeline.standardize_severity(df)
    
    assert std_df['standardized_severity'].iloc[0] == 'UML'
    assert std_df['standardized_severity'].iloc[1] == 'UML'
    assert std_df['standardized_severity'].iloc[2] == 'NBML'
    assert std_df['standardized_severity'].iloc[3] == 'NORMAL'
