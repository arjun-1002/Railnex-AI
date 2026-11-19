"""
Railnex AI API Endpoints
"""

import os
import io
import sys
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
import pandas as pd

from ..schemas.models import (
    SeverityPredictionRequest, SeverityPredictionResponse,
    MaintenancePriorityItem, StationItem
)
from ..core.ml_service import MLService
from ..core.data_service import DataService
from ..config import BASE_DIR

# Ensure TrackPrior-AI scripts are importable
SCRIPTS_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

from rti_pipeline import RTIIndianRailwaysTMSPipeline
from weather_importer import WeatherDataImporter

router = APIRouter(prefix="/api")

ml_service = MLService()
data_service = DataService()
rti_pipeline = RTIIndianRailwaysTMSPipeline()
weather_importer = WeatherDataImporter()

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

@router.post("/upload/rti-tms")
async def upload_rti_tms(file: UploadFile = File(...)):
    """Accepts and audits uploaded Indian Railways TMS inspection files."""
    try:
        contents = await file.read()
        filename = file.filename or "uploaded_tms.csv"
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == ".csv":
            df_raw = pd.read_csv(io.BytesIO(contents))
        elif ext in [".xlsx", ".xls"]:
            df_raw = pd.read_excel(io.BytesIO(contents))
        elif ext == ".parquet":
            df_raw = pd.read_parquet(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Please upload .csv, .xlsx, or .parquet")
            
        df_clean, audit = rti_pipeline.process_dataframe(df_raw, source_filename=filename)
        
        sample_records = df_clean.head(20).to_dict(orient="records")
        for r in sample_records:
            for k, v in r.items():
                if pd.isna(v):
                    r[k] = None
                elif hasattr(v, 'isoformat'):
                    r[k] = v.isoformat()
                    
        return {
            "status": "SUCCESS",
            "message": f"Successfully ingested and audited {len(df_clean)} Indian Railways TMS records.",
            "audit": audit,
            "preview_records": sample_records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process TMS file: {str(e)}")

@router.post("/upload/weather")
async def upload_weather(file: UploadFile = File(...)):
    """Accepts and audits uploaded meteorological time-series records."""
    try:
        contents = await file.read()
        filename = file.filename or "uploaded_weather.csv"
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == ".csv":
            df_raw = pd.read_csv(io.BytesIO(contents))
        elif ext in [".xlsx", ".xls"]:
            df_raw = pd.read_excel(io.BytesIO(contents))
        elif ext == ".parquet":
            df_raw = pd.read_parquet(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Please upload .csv, .xlsx, or .parquet")
            
        std_df, audit = weather_importer.process_dataframe(df_raw)
        
        sample_records = std_df.head(15).to_dict(orient="records")
        for r in sample_records:
            for k, v in r.items():
                if pd.isna(v):
                    r[k] = None
                elif hasattr(v, 'isoformat'):
                    r[k] = v.isoformat()
                    
        return {
            "status": "SUCCESS",
            "message": f"Successfully standardized {len(std_df)} weather observations.",
            "audit": audit,
            "preview_records": sample_records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process weather file: {str(e)}")

@router.get("/reports/advisory")
def get_maintenance_advisory():
    """Generates an official printable Indian Railways Track Maintenance Advisory."""
    try:
        return data_service.get_maintenance_advisory()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/search")
def search_stations(q: str = Query(..., min_length=1, description="Station search query")):
    """Searches Indian Railways stations by code, name, or state."""
    try:
        return data_service.search_stations(query=q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

