"""
Pydantic schemas for Railnex AI API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SeverityPredictionRequest(BaseModel):
    defect_length_ft: float = Field(..., ge=0.1, le=500.0, description="Defect length in feet")
    defect_amplitude_in: float = Field(..., ge=-10.0, le=10.0, description="Defect amplitude in inches")
    fra_track_class: int = Field(4, ge=1, le=5, description="FRA track class (1 to 5)")
    freight_speed_limit_mph: float = Field(40.0, ge=0.0, le=120.0, description="Operating speed for freight trains")
    passenger_speed_limit_mph: float = Field(60.0, ge=0.0, le=160.0, description="Operating speed for passenger trains")
    defect_type: str = Field("XLEVEL", description="Defect type (XLEVEL, SURFACE, DIP)")
    curve_spiral_tangent_code: str = Field("T", description="Track code: T (Tangent), S (Spiral), C (Curve)")
    track_code: str = Field("0", description="Mainline or track indicator")
    inspection_month: int = Field(6, ge=1, le=12, description="Month of inspection (1 to 12)")

class ContributingFactor(BaseModel):
    feature: str
    impact: str
    description: str

class StandardsComparison(BaseModel):
    parameter: str
    recorded_value: str
    irpwm_standard: str
    status: str

class ShapAttribution(BaseModel):
    feature_name: str
    feature_label: str
    shap_value: float
    contribution_direction: str
    importance_pct: float

class SeverityPredictionResponse(BaseModel):
    predicted_class: str
    severity_label: str
    urgency_level: str
    confidence_score: float
    probabilities: Dict[str, float]
    contributing_factors: List[ContributingFactor]
    standards_comparison: List[StandardsComparison]
    shap_attributions: List[ShapAttribution] = Field(default_factory=list)
    suggested_action: str
    limitations_disclaimer: str

class MaintenancePriorityItem(BaseModel):
    record_id: int
    line_segment_id: int
    milepost: float
    defect_type: str
    defect_length_ft: float
    defect_amplitude_in: float
    predicted_severity: str
    confidence: float
    priority_score: float
    priority_tier: str
    suggested_action: str
    inspection_date: Optional[str] = None

class TrackDeteriorationItem(BaseModel):
    line_segment_id: int
    total_inspections: int
    recurring_defects_count: int
    avg_amplitude: float
    max_amplitude: float
    deterioration_trend: str
    urgency_rank: int
    last_inspection_date: Optional[str] = None
    monthly_degradation_rate_mm: float = 0.0
    projected_days_to_uml: int = 180
    prognostic_status: str = "STABLE DEGRADATION"
    remaining_tonnage_mgt: float = 25.0

class StationItem(BaseModel):
    station_code: str
    station_name: str
    state: Optional[str] = None
    zone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class DegradationSimulationRequest(BaseModel):
    line_segment_id: int = Field(10103100, description="Track line segment ID")
    baseline_amplitude_mm: float = Field(8.5, ge=1.0, le=20.0, description="Baseline peak amplitude in mm")
    axle_load_tonnes: float = Field(22.82, ge=18.0, le=35.0, description="Axle load in tonnes")
    traffic_mgt_annual: float = Field(35.0, ge=10.0, le=100.0, description="Annual traffic in Million Gross Tonnes")
    deferred_maintenance_days: int = Field(0, ge=0, le=180, description="Days deferred before tamping")
    monsoon_rainfall_mm: float = Field(0.0, ge=0.0, le=500.0, description="Recent 48h rainfall in mm")
    ballast_condition: str = Field("MODERATE", description="Ballast condition: EXCELLENT, GOOD, MODERATE, DEGRADED")
