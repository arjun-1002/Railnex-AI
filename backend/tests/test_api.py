"""
Integration and Unit Tests for Railnex AI Backend API
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["model_loaded"] is True
    assert data["datasets_ready"] is True

def test_overview_endpoint():
    res = client.get("/api/overview")
    assert res.status_code == 200
    data = res.json()
    assert "summary_cards" in data
    assert data["summary_cards"]["total_inspection_records"] > 20000
    assert len(data["severity_distribution"]) == 2
    assert len(data["defect_type_breakdown"]) == 3
    assert len(data["datasets_manifest"]) >= 6

def test_predict_severity_severe_defect():
    payload = {
        "defect_length_ft": 22.0,
        "defect_amplitude_in": 1.95,
        "fra_track_class": 4,
        "freight_speed_limit_mph": 45.0,
        "passenger_speed_limit_mph": 65.0,
        "defect_type": "XLEVEL",
        "curve_spiral_tangent_code": "C",
        "track_code": "0",
        "inspection_month": 7
    }
    res = client.post("/api/predict/severity", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["predicted_class"] == "RED"
    assert "URGENT" in data["urgency_level"]
    assert data["confidence_score"] > 0.85
    assert len(data["contributing_factors"]) > 0
    assert len(data["standards_comparison"]) > 0

def test_predict_severity_minor_defect():
    payload = {
        "defect_length_ft": 8.0,
        "defect_amplitude_in": 0.55,
        "fra_track_class": 3,
        "freight_speed_limit_mph": 30.0,
        "passenger_speed_limit_mph": 40.0,
        "defect_type": "SURFACE",
        "curve_spiral_tangent_code": "T",
        "track_code": "0",
        "inspection_month": 3
    }
    res = client.post("/api/predict/severity", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["predicted_class"] == "YELLOW"
    assert "PLANNED" in data["urgency_level"]

def test_maintenance_prioritization():
    res = client.get("/api/maintenance/prioritization?urgency=CRITICAL&limit=25")
    assert res.status_code == 200
    items = res.json()
    assert len(items) > 0
    assert len(items) <= 25
    for item in items:
        assert item["priority_tier"] == "CRITICAL_REVIEW"
        assert item["priority_score"] >= 40.0

def test_track_deterioration():
    res = client.get("/api/track/deterioration")
    assert res.status_code == 200
    data = res.json()
    assert "top_deteriorating_segments" in data
    assert len(data["top_deteriorating_segments"]) > 0
    assert "longitudinal_sample_segment" in data

def test_network_stations():
    res = client.get("/api/network/stations?zone=NR&limit=50")
    assert res.status_code == 200
    stations = res.json()
    assert len(stations) > 0
    assert len(stations) <= 50
    for s in stations:
        assert s["zone"] == "NR"
        assert s["latitude"] is not None
        assert s["longitude"] is not None

def test_network_zones():
    res = client.get("/api/network/zones")
    assert res.status_code == 200
    zones = res.json()
    assert len(zones) >= 16

def test_models_evaluation():
    res = client.get("/api/models/evaluation")
    assert res.status_code == 200
    data = res.json()
    assert "experiment_a_real" in data
    assert "experiment_b_synthetic" in data
    assert data["experiment_a_real"]["best_model"] == "XGBoost"
    assert data["experiment_a_real"]["best_weighted_f1"] > 0.95

def test_standards():
    res = client.get("/api/standards")
    assert res.status_code == 200
    standards = res.json()
    assert len(standards) >= 30
    first = standards[0]
    assert "parameter_name" in first
    assert "threshold_value" in first
    assert "source_document" in first

def test_data_explorer():
    res = client.get("/api/data/explorer?page=1&page_size=20&defect_type=XLEVEL")
    assert res.status_code == 200
    data = res.json()
    assert len(data["records"]) == 20
    assert data["total"] > 1000
    for r in data["records"]:
        assert r["defect_type"] == "XLEVEL"
