"""
RailRakshak AI — Unified Pydantic Schemas for All 19 Modules
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# ==============================================================================
# 1. Defect Severity Prediction (Module 4 & 5)
# ==============================================================================
class SeverityPredictionRequest(BaseModel):
    defect_length_ft: float = Field(12.0, ge=0.1, le=500.0, description="Defect length in feet")
    defect_amplitude_in: float = Field(1.2, ge=-10.0, le=10.0, description="Defect amplitude in inches")
    fra_track_class: int = Field(4, ge=1, le=5, description="FRA track class (1 to 5)")
    freight_speed_limit_mph: float = Field(40.0, ge=0.0, le=120.0, description="Operating speed for freight trains")
    passenger_speed_limit_mph: float = Field(60.0, ge=0.0, le=160.0, description="Operating speed for passenger trains")
    defect_type: str = Field("XLEVEL", description="Defect type (XLEVEL, SURFACE, DIP, GAUGE, TWIST)")
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
    predicted_class: str # "NORMAL", "MINOR", "MAJOR", "CRITICAL"
    severity_code: int # 0, 1, 2, 3
    severity_label: str
    urgency_level: str
    confidence_score: float
    uncertainty_score: float = 0.04
    probabilities: Dict[str, float]
    severity_color: str # #10b981 (green), #f59e0b (yellow), #f97316 (orange), #ef4444 (red)
    contributing_factors: List[ContributingFactor]
    standards_comparison: List[StandardsComparison]
    shap_attributions: List[ShapAttribution] = Field(default_factory=list)
    suggested_action: str
    limitations_disclaimer: str

# ==============================================================================
# 2. Maintenance Priority Management (Module 6)
# ==============================================================================
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
    urgency_color: str = "#f59e0b"

# ==============================================================================
# 3. Track Health & Deterioration (Module 3 & 8)
# ==============================================================================
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

class DegradationSimulationRequest(BaseModel):
    line_segment_id: int = Field(10103100, description="Track line segment ID")
    baseline_amplitude_mm: float = Field(8.5, ge=1.0, le=20.0, description="Baseline peak amplitude in mm")
    axle_load_tonnes: float = Field(22.82, ge=18.0, le=35.0, description="Axle load in tonnes")
    traffic_mgt_annual: float = Field(35.0, ge=10.0, le=100.0, description="Annual traffic in Million Gross Tonnes")
    deferred_maintenance_days: int = Field(0, ge=0, le=180, description="Days deferred before tamping")
    monsoon_rainfall_mm: float = Field(0.0, ge=0.0, le=500.0, description="Recent 48h rainfall in mm")
    ballast_condition: str = Field("MODERATE", description="Ballast condition: EXCELLENT, GOOD, MODERATE, DEGRADED")

# ==============================================================================
# 4. Geography, Stations, Zones & Divisions (Module 2)
# ==============================================================================
class StationItem(BaseModel):
    station_code: str
    station_name: str
    state: Optional[str] = None
    zone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class DivisionItem(BaseModel):
    division_code: str
    division_name: str
    div_hq: str
    zone_code: str
    state: str
    route_km: float
    running_track_km: float
    speed_band_max: int

class ZoneItem(BaseModel):
    zone_code: str
    zone_name: str
    zone_hq: str
    route_km: float
    running_track_km: float

# ==============================================================================
# 5. Ultrasonic Flaw Analysis (Module 10)
# ==============================================================================
class UsfdFlawStandard(BaseModel):
    defect_code: str
    defect_type: str
    location: str
    probe_angle_deg: int
    severity_classification: str
    action_required: str
    growth_rate_mm_per_gmt: float

class UsfdInspectionItem(BaseModel):
    usfd_record_id: str
    route_section: str
    railway_zone: str
    division: str
    milepost_km: float
    track_line: str
    rail_type: str
    cumulative_gmt: float
    flaw_code: str
    flaw_description: str
    flaw_location: str
    flaw_depth_mm: float
    echo_amplitude_db: float
    severity_classification: str
    action_mandate: str
    est_days_to_critical: int
    inspection_date: str

# ==============================================================================
# 6. Computer Vision Defect Detection (Module 9)
# ==============================================================================
class CvDefectPrediction(BaseModel):
    image_filename: str
    detected_class: str # "DEFECTIVE", "HEALTHY"
    confidence: float
    defect_subtype: str # "Surface Crack", "Damaged Sleeper Seat", "Missing Fastener Clip", "Normal Track"
    annotated_bounding_box: Dict[str, float] = Field(default_factory=dict)
    engineering_recommendation: str
    disclaimer: str

# ==============================================================================
# 7. AI Maintenance Assistant (Module 16)
# ==============================================================================
class AssistantChatRequest(BaseModel):
    query: str
    context_zone: Optional[str] = None
    context_section: Optional[str] = None

class AssistantChatResponse(BaseModel):
    response_text: str
    referenced_standards: List[str] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    timestamp: str

# ==============================================================================
# 8. Weather & Accidents (Module 7 & 13)
# ==============================================================================
class WeatherHubSummary(BaseModel):
    station_code: str
    station_name: str
    zone: str
    current_temp_max_c: float
    current_rail_temp_c: float
    buckling_risk: bool
    heavy_rain_risk: bool
    monsoon_warning: str

class AccidentSummaryItem(BaseModel):
    fiscal_year: str
    total_consequential_accidents: int
    derailments: int
    collisions: int
    fatalities: int
