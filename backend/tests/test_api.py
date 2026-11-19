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

def test_predict_severity_shap_attributions():
    payload = {
        "defect_length_ft": 30.0,
        "defect_amplitude_in": 1.75,
        "fra_track_class": 4,
        "freight_speed_limit_mph": 50.0,
        "passenger_speed_limit_mph": 70.0,
        "defect_type": "XLEVEL",
        "curve_spiral_tangent_code": "C",
        "track_code": "1",
        "inspection_month": 8
    }
    res = client.post("/api/predict/severity", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "shap_attributions" in data
    assert len(data["shap_attributions"]) >= 4
    for item in data["shap_attributions"]:
        assert "feature_name" in item
        assert "shap_value" in item
        assert item["contribution_direction"] in ["INCREASES_RISK", "REDUCES_RISK"]
        assert item["importance_pct"] >= 0.0

def test_track_deterioration_prognostic_rul():
    res = client.get("/api/track/deterioration")
    assert res.status_code == 200
    data = res.json()
    assert "top_deteriorating_segments" in data
    top_seg = data["top_deteriorating_segments"][0]
    assert "monthly_degradation_rate_mm" in top_seg
    assert "projected_days_to_uml" in top_seg
    assert "prognostic_status" in top_seg
    assert top_seg["projected_days_to_uml"] > 0

def test_upload_rti_tms_endpoint():
    csv_content = b"zone,division,section,track,km,param,amplitude,speed\nNR,Delhi,NDLS-GZB,UP,14.5,XLEVEL,16.5,110\nWR,Mumbai,BCT-VR,DN,22.0,TWIST,4.5,100\n"
    res = client.post(
        "/api/upload/rti-tms",
        files={"file": ("sample_tms_upload.csv", csv_content, "text/csv")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert "audit" in data
    assert data["audit"]["ingested_records"] == 2
    assert "UML" in data["audit"]["severity_distribution"]

def test_upload_weather_endpoint():
    weather_csv = b"timestamp,station_id,temperature_c,rainfall_mm,humidity_percent\n2023-01-01 10:00:00,STN_01,24.5,0.0,65.0\n2023-01-01 11:00:00,STN_01,25.2,1.2,68.0\n"
    res = client.post(
        "/api/upload/weather",
        files={"file": ("sample_weather_upload.csv", weather_csv, "text/csv")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert data["audit"]["total_records"] == 2

def test_get_maintenance_advisory():
    res = client.get("/api/reports/advisory")
    assert res.status_code == 200
    data = res.json()
    assert "advisory_ref" in data
    assert "IRPWM 2020" in data["statutory_mandate"]
    assert len(data["critical_exceedances"]) > 0
    assert len(data["tamping_allocation"]) > 0

def test_search_stations_endpoint():
    res = client.get("/api/network/search?q=NDLS")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    codes = [s["station_code"] for s in data]
    assert "NDLS" in codes

def test_ir_trc_corridor_sample_ingestion():
    file_path = "TrackPrior-AI/data/raw/tms_samples/sample_ir_trc_corridor_run.csv"
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    res = client.post(
        "/api/upload/rti-tms",
        files={"file": ("sample_ir_trc_corridor_run.csv", file_bytes, "text/csv")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    audit = data["audit"]
    assert audit["ingested_records"] == 150
    assert "NR" in audit["zonal_railways_detected"]
    assert "NCR" in audit["zonal_railways_detected"]
    assert "Delhi" in audit["divisions_detected"]
    assert "Prayagraj" in audit["divisions_detected"]
    assert audit["severity_distribution"]["UML"] > 0
    assert len(data["preview_records"]) == 20

def test_track_degradation_simulation():
    payload = {
        "line_segment_id": 10103100,
        "baseline_amplitude_mm": 8.5,
        "axle_load_tonnes": 25.0,
        "traffic_mgt_annual": 45.0,
        "deferred_maintenance_days": 45,
        "monsoon_rainfall_mm": 180.0,
        "ballast_condition": "DEGRADED"
    }
    res = client.post("/api/track/simulate-degradation", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "degradation_metrics" in data
    metrics = data["degradation_metrics"]
    assert metrics["simulated_rate_mm_per_month"] > metrics["baseline_rate_mm_per_month"]
    assert metrics["degradation_acceleration_pct"] > 50.0
    assert len(data["projection_timeline"]) == 13
    assert data["advisory"]["mandated_speed_restriction_kmph"] <= 100



