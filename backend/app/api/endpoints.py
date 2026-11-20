"""
RailRakshak AI — Unified API Endpoints (All 19 Modules)
"""

import os
import io
import sys
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
import pandas as pd

from ..schemas.models import (
    SeverityPredictionRequest, SeverityPredictionResponse,
    MaintenancePriorityItem, StationItem, DegradationSimulationRequest,
    CvDefectPrediction, AssistantChatRequest, AssistantChatResponse
)
from ..core.ml_service import MLService
from ..core.data_service import DataService
from ..core.cv_service import CvService
from ..core.assistant_service import AssistantService
from ..config import BASE_DIR

# Ensure scripts dir is in sys.path
SCRIPTS_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

from rti_pipeline import RTIIndianRailwaysTMSPipeline
from weather_importer import WeatherDataImporter

router = APIRouter(prefix="/api")

ml_service = MLService()
data_service = DataService()
cv_service = CvService()
assistant_service = AssistantService()
rti_pipeline = RTIIndianRailwaysTMSPipeline()
weather_importer = WeatherDataImporter()

# ==============================================================================
# Health & Status
# ==============================================================================
@router.get("/health")
def health_check():
    return {
        "status": "online",
        "system": "RailRakshak AI Decision Support Engine",
        "version": "2.0.0",
        "academic_course": "Supervised Learning (INT395) Topic 20",
        "champion_model": ml_service.champion_name,
        "model_loaded": ml_service.model is not None,
        "datasets_ready": data_service.df_informs is not None,
        "total_datasets_integrated": 13
    }

# ==============================================================================
# Module 1 — National Railway Dashboard
# ==============================================================================
@router.get("/overview")
def get_overview():
    try:
        return data_service.get_overview_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 4 & 5 — AI Defect Severity Prediction (4-Class & TreeSHAP)
# ==============================================================================
@router.post("/predict/severity", response_model=SeverityPredictionResponse)
def predict_severity(payload: SeverityPredictionRequest):
    try:
        return ml_service.predict_severity(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 15 — Model Performance Dashboard (7 Competing Models & Metrics)
# ==============================================================================
@router.get("/models/evaluation")
def get_model_evaluation():
    try:
        return ml_service.get_model_evaluation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 6 — Maintenance Priority Management
# ==============================================================================
@router.get("/maintenance/prioritization", response_model=List[MaintenancePriorityItem])
def get_maintenance_prioritization(
    urgency: str = Query("ALL", description="Urgency filter: ALL, CRITICAL, HIGH"),
    defect_type: str = Query("ALL", description="Defect type filter: ALL, XLEVEL, SURFACE, DIP"),
    line_segment: Optional[int] = Query(None, description="Line segment ID"),
    limit: int = Query(100, ge=1, le=500)
):
    try:
        return data_service.get_maintenance_prioritization(
            min_urgency=urgency,
            defect_type=defect_type,
            line_segment_id=line_segment,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 6 & 18 — Official P-Way Maintenance Advisory Sheet
# ==============================================================================
@router.get("/reports/advisory")
def get_maintenance_advisory():
    try:
        priorities = data_service.get_maintenance_prioritization(limit=50)
        critical_items = [p for p in priorities if "Critical" in p.get("predicted_severity", "") or p.get("priority_tier") == "CRITICAL_REVIEW"]
        tamping_items = [p for p in priorities if p.get("priority_tier") in ["CRITICAL_REVIEW", "HIGH_PRIORITY"]]

        return {
            "advisory_ref": f"IR/PWAY/ADV/{pd.Timestamp.now().strftime('%Y%m%d')}/042",
            "statutory_mandate": "Indian Railways Permanent Way Manual (IRPWM 2020 Edition) Table 5.1 & Para 5.1",
            "generation_timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S IST"),
            "critical_exceedances": critical_items,
            "tamping_allocation": tamping_items,
            "presiding_engineer": "Senior Section Engineer (SSE / P-Way / TRC Analytics)",
            "work_orders": priorities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 3 & 8 — Track Health, Deterioration & Prognostics
# ==============================================================================
@router.get("/track/deterioration")
def get_track_deterioration():
    try:
        return data_service.get_track_deterioration()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 17 — Interactive What-If Operational Sensitivity Sandbox
# ==============================================================================
@router.post("/track/simulate-degradation")
def simulate_track_degradation(payload: DegradationSimulationRequest):
    try:
        return data_service.simulate_track_degradation(
            line_segment_id=payload.line_segment_id,
            baseline_amplitude_mm=payload.baseline_amplitude_mm,
            axle_load_tonnes=payload.axle_load_tonnes,
            traffic_mgt_annual=payload.traffic_mgt_annual,
            deferred_maintenance_days=payload.deferred_maintenance_days,
            monsoon_rainfall_mm=payload.monsoon_rainfall_mm,
            ballast_condition=payload.ballast_condition
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 2 — Network Geography, GIS Stations, Zones & Divisions
# ==============================================================================
@router.get("/network/stations", response_model=List[StationItem])
def get_stations(
    zone: Optional[str] = Query(None, description="Railway Zone filter, e.g. NR, NCR"),
    limit: int = Query(100, ge=1, le=500)
):
    try:
        return data_service.get_stations(zone=zone, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/search", response_model=List[StationItem])
def search_stations(
    q: str = Query(..., min_length=1, description="Station name, station code, or state"),
    limit: int = Query(25, ge=1, le=100)
):
    try:
        return data_service.search_stations(query=q, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/zones")
def get_network_zones():
    try:
        return data_service.get_zones_and_divisions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 14 — Data Explorer & Manifest
# ==============================================================================
@router.get("/data/explorer")
def get_data_explorer(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    defect_type: str = Query("ALL"),
    line_segment: Optional[int] = Query(None)
):
    try:
        return data_service.get_data_explorer(
            page=page,
            page_size=page_size,
            defect_type=defect_type,
            line_segment_id=line_segment
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/datasets/manifest")
def get_datasets_manifest():
    try:
        return data_service.manifest_data if data_service.manifest_data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 7 — Weather Intelligence & Buckling Risks
# ==============================================================================
@router.get("/weather/intelligence")
def get_weather_intelligence():
    try:
        return data_service.get_weather_intelligence()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 9 — Computer Vision Track Defect Detection
# ==============================================================================
@router.get("/cv/samples")
def get_cv_sample_images(limit: int = Query(12, ge=4, le=24)):
    try:
        return cv_service.list_sample_images(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cv/predict", response_model=CvDefectPrediction)
async def predict_cv_defect(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        return cv_service.analyze_image(contents, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 10 — Ultrasonic Flaw Detection (USFD)
# ==============================================================================
@router.get("/usfd/flaws")
def get_usfd_flaws(limit: int = Query(100, ge=10, le=250)):
    try:
        return data_service.get_usfd_flaws(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usfd/standards")
def get_usfd_standards():
    try:
        return data_service.get_usfd_standards()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 13 — Railway Safety & Accident Analytics
# ==============================================================================
@router.get("/safety/accidents")
def get_safety_accidents():
    try:
        return data_service.get_accident_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# Module 16 — AI Railway Maintenance Assistant
# ==============================================================================
@router.post("/assistant/chat", response_model=AssistantChatResponse)
def assistant_chat(payload: AssistantChatRequest):
    try:
        return assistant_service.chat(query=payload.query, zone=payload.context_zone)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# File Ingestion Pipelines (Module 14)
# ==============================================================================
@router.post("/upload/rti-tms")
async def upload_rti_tms_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df_uploaded = pd.read_csv(io.BytesIO(contents))
        df_clean, audit = rti_pipeline.process_dataframe(df_uploaded, source_filename=file.filename)
        return {
            "status": "SUCCESS",
            "message": f"Successfully ingested {len(df_clean)} RTI TMS inspection records.",
            "audit": audit,
            "preview_records": df_clean.head(20).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"RTI TMS ingestion failed: {str(e)}")

@router.post("/upload/weather")
async def upload_weather_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df_uploaded = pd.read_csv(io.BytesIO(contents))
        df_clean = weather_importer.standardize(df_uploaded)
        audit = weather_importer.audit_quality(df_clean)
        return {
            "status": "SUCCESS",
            "message": "Weather telemetry ingested successfully.",
            "audit": audit,
            "preview_records": df_clean.head(20).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Weather ingestion failed: {str(e)}")

# ==============================================================================
# Standards
# ==============================================================================
@router.get("/standards")
def get_standards():
    try:
        return ml_service.get_standards()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
