"""
Railnex AI API Endpoints
"""

import os
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
import pandas as pd

from ..schemas.models import (
    SeverityPredictionRequest, SeverityPredictionResponse,
    MaintenancePriorityItem, StationItem
)
from ..core.ml_service import MLService
from ..core.data_service import DataService

router = APIRouter(prefix="/api")

ml_service = MLService()
data_service = DataService()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "system": "Railnex AI Decision Support Engine",
        "version": "1.0.0",
        "model_loaded": ml_service.model is not None,
        "datasets_ready": data_service.df_informs is not None
    }

@router.get("/overview")
def get_overview():
    try:
        return data_service.get_overview_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/severity", response_model=SeverityPredictionResponse)
def predict_severity(payload: SeverityPredictionRequest):
    try:
        return ml_service.predict_severity(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@router.get("/track/deterioration")
def get_track_deterioration():
    try:
        return data_service.get_track_deterioration()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/stations", response_model=List[StationItem])
def get_stations(
    zone: str = Query("ALL", description="Railway Zone (e.g., NR, WR, CR, SR, SCR)"),
    limit: int = Query(150, ge=1, le=1000)
):
    try:
        return data_service.get_stations(zone=zone, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/zones")
def get_zones():
    try:
        return data_service.get_zones_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/analysis")
def get_weather_analysis():
    try:
        return data_service.get_weather_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/evaluation")
def get_models_evaluation():
    try:
        return ml_service.get_model_evaluation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/standards")
def get_standards():
    try:
        return ml_service.get_standards()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/explorer")
def explore_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    defect_type: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    line_segment: Optional[int] = Query(None)
):
    try:
        return data_service.query_inspection_records(
            page=page,
            page_size=page_size,
            defect_type=defect_type,
            priority_tag=priority,
            line_segment_id=line_segment
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
