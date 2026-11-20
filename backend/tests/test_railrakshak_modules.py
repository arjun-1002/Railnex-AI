"""
RailRakshak AI — Test Suite for Extended Modules (Modules 7, 9, 10, 13, 14, 16)
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_weather_intelligence_module():
    res = client.get("/api/weather/intelligence")
    assert res.status_code == 200
    data = res.json()
    assert "total_weather_records" in data
    assert data["total_weather_records"] >= 10000
    assert "zonal_hubs" in data
    assert len(data["zonal_hubs"]) >= 7
    first_hub = data["zonal_hubs"][0]
    assert "station_code" in first_hub
    assert "est_rail_temp_c" in first_hub
    assert "buckling_risk_days_recorded" in first_hub

def test_usfd_flaws_module():
    res = client.get("/api/usfd/flaws?limit=50")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 50
    first = items[0]
    assert "flaw_code" in first
    assert "severity_classification" in first
    assert first["severity_classification"] in ["IMR", "OBS", "IMRW", "OBSW"]
    assert "echo_amplitude_db" in first

def test_usfd_standards_module():
    res = client.get("/api/usfd/standards")
    assert res.status_code == 200
    standards = res.json()
    assert len(standards) >= 10
    first = standards[0]
    assert "defect_code" in first
    assert "probe_angle_deg" in first
    assert "action_required" in first

def test_cv_samples_module():
    res = client.get("/api/cv/samples?limit=8")
    assert res.status_code == 200
    samples = res.json()
    assert len(samples) > 0
    first = samples[0]
    assert "filename" in first
    assert "category" in first
    assert first["category"] in ["DEFECTIVE", "HEALTHY"]

def test_safety_accidents_module():
    res = client.get("/api/safety/accidents")
    assert res.status_code == 200
    data = res.json()
    assert "ten_year_accident_history" in data
    assert len(data["ten_year_accident_history"]) >= 8
    assert "cag_track_derailment_subcauses" in data
    assert len(data["cag_track_derailment_subcauses"]) >= 4

def test_assistant_chat_module():
    # Test Crosslevel query
    payload = {"query": "What are the crosslevel limits in IRPWM?"}
    res = client.post("/api/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Crosslevel" in data["response_text"] or "IRPWM" in data["response_text"]
    assert len(data["referenced_standards"]) > 0

    # Test USFD query
    payload_usfd = {"query": "What is an IMR flaw in USFD testing?"}
    res_usfd = client.post("/api/assistant/chat", json=payload_usfd)
    assert res_usfd.status_code == 200
    data_usfd = res_usfd.json()
    assert "IMR" in data_usfd["response_text"]

def test_datasets_manifest_module():
    res = client.get("/api/datasets/manifest")
    assert res.status_code == 200
    data = res.json()
    assert "total_datasets" in data
    assert data["total_datasets"] >= 10
    assert "datasets" in data
