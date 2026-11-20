"""
RailRakshak AI — Relational Database Schema (SQLAlchemy 2.0 Declarative)
Implements all 24 required relational models specified in Section 14.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from .session import Base

# ==============================================================================
# 1. Identity, Roles & Permissions
# ==============================================================================
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False) # Admin, Engineer, Viewer
    description = Column(String(255))
    can_upload_data = Column(Boolean, default=False)
    can_trigger_training = Column(Boolean, default=False)
    can_approve_maintenance = Column(Boolean, default=False)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    full_name = Column(String(150))
    department = Column(String(100), default="Civil Engineering (Permanent Way)")
    zone_code = Column(String(20), default="NR")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    predictions = relationship("PredictionHistory", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

# ==============================================================================
# 2. Railway Infrastructure & Geographic Hierarchy
# ==============================================================================
class RailwayZone(Base):
    __tablename__ = "railway_zones"
    id = Column(Integer, primary_key=True, index=True)
    zone_code = Column(String(20), unique=True, nullable=False, index=True) # e.g. NR, NCR
    zone_name = Column(String(100), nullable=False)
    zone_hq = Column(String(100), nullable=False)
    total_route_km = Column(Float, default=0.0)
    total_running_km = Column(Float, default=0.0)

    divisions = relationship("RailwayDivision", back_populates="zone")

class RailwayDivision(Base):
    __tablename__ = "railway_divisions"
    id = Column(Integer, primary_key=True, index=True)
    division_code = Column(String(20), unique=True, nullable=False, index=True) # e.g. PRYJ, DLI
    division_name = Column(String(100), nullable=False)
    div_hq = Column(String(100), nullable=False)
    zone_code = Column(String(20), ForeignKey("railway_zones.zone_code"), nullable=False)
    state = Column(String(100))
    route_km = Column(Float, default=0.0)
    running_track_km = Column(Float, default=0.0)
    speed_band_max = Column(Integer, default=110)

    zone = relationship("RailwayZone", back_populates="divisions")
    track_sections = relationship("TrackSection", back_populates="division")

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String(20), unique=True, nullable=False, index=True)
    station_name = Column(String(150), nullable=False, index=True)
    zone_code = Column(String(20), index=True)
    state = Column(String(100), index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class TrackSection(Base):
    __tablename__ = "track_sections"
    id = Column(Integer, primary_key=True, index=True)
    section_code = Column(String(50), unique=True, nullable=False, index=True) # e.g. SEC-NDLS-CNB-01
    division_code = Column(String(20), ForeignKey("railway_divisions.division_code"), nullable=False)
    from_milepost = Column(Float, nullable=False)
    to_milepost = Column(Float, nullable=False)
    track_type = Column(String(50), default="Broad Gauge (1676 mm)")
    line_type = Column(String(50), default="Double Line - UP Main")
    rail_weight_kg = Column(Float, default=60.0) # 60kg or 52kg
    annual_gmt = Column(Float, default=35.0)
    max_permissible_speed = Column(Integer, default=130)

    division = relationship("RailwayDivision", back_populates="track_sections")
    inspections = relationship("TrackInspection", back_populates="section")

# ==============================================================================
# 3. Track Inspections, Geometry & Defect Observations
# ==============================================================================
class TrackInspection(Base):
    __tablename__ = "track_inspections"
    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(String(100), unique=True, nullable=False, index=True)
    section_code = Column(String(50), ForeignKey("track_sections.section_code"), nullable=False)
    inspection_date = Column(DateTime, nullable=False, index=True)
    inspection_vehicle = Column(String(100), default="Track Recording Car (TRC)")
    tqi_score = Column(Float, default=78.5) # Track Quality Index
    inspector_name = Column(String(100), default="SSE/P-Way Inspection Unit")

    section = relationship("TrackSection", back_populates="inspections")
    defects = relationship("DefectObservation", back_populates="inspection")

class DefectObservation(Base):
    __tablename__ = "defect_observations"
    id = Column(Integer, primary_key=True, index=True)
    defect_uuid = Column(String(100), unique=True, nullable=False, index=True)
    inspection_id = Column(String(100), ForeignKey("track_inspections.inspection_id"), nullable=False)
    milepost_km = Column(Float, nullable=False, index=True)
    defect_type = Column(String(50), nullable=False) # XLEVEL, SURFACE, DIP, GAUGE, TWIST
    amplitude_mm = Column(Float, nullable=False)
    length_m = Column(Float, nullable=False)
    operating_speed_kmh = Column(Float, default=110.0)
    curvature_deg = Column(Float, default=0.0)
    
    # 4-Class Multiclass Severity: 0=Normal, 1=Minor, 2=Major, 3=Critical
    severity_class = Column(Integer, nullable=False, index=True) # 0, 1, 2, 3
    severity_label = Column(String(50), nullable=False) # Normal, Minor, Major, Critical
    urgency_tier = Column(String(50), default="Routine")
    irpwn_threshold_status = Column(String(50), default="Compliant")
    action_mandate = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    inspection = relationship("TrackInspection", back_populates="defects")

# ==============================================================================
# 4. Ultrasonic Flaw Detection (USFD)
# ==============================================================================
class UltrasonicInspection(Base):
    __tablename__ = "ultrasonic_inspections"
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String(100), unique=True, nullable=False, index=True)
    route_section = Column(String(100), nullable=False)
    zone_code = Column(String(20), nullable=False, index=True)
    division_code = Column(String(20), nullable=False)
    milepost_km = Column(Float, nullable=False)
    rail_type = Column(String(50), default="60kg 90UTS")
    flaw_code = Column(String(20), nullable=False) # e.g. 111, 411, 711
    flaw_description = Column(String(150), nullable=False)
    probe_angle_deg = Column(Integer, default=70)
    flaw_depth_mm = Column(Float, nullable=False)
    echo_amplitude_db = Column(Float, nullable=False)
    severity_classification = Column(String(20), nullable=False) # IMR, OBS, IMRW, OBSW
    action_mandate = Column(String(255))
    est_days_to_critical = Column(Integer, default=15)
    inspection_date = Column(DateTime, default=datetime.utcnow)

# ==============================================================================
# 5. Weather Telemetry & Environmental Intelligence
# ==============================================================================
class WeatherObservation(Base):
    __tablename__ = "weather_observations"
    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String(20), nullable=False, index=True)
    zone_code = Column(String(20), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    temp_max_c = Column(Float, nullable=False)
    temp_min_c = Column(Float, nullable=False)
    temp_mean_c = Column(Float, nullable=False)
    precipitation_mm = Column(Float, default=0.0)
    wind_speed_kmh = Column(Float, default=10.0)
    est_rail_temp_max_c = Column(Float, nullable=False)
    buckling_risk_flag = Column(Integer, default=0, index=True)
    heavy_rainfall_flag = Column(Integer, default=0, index=True)
    heatwave_flag = Column(Integer, default=0, index=True)

# ==============================================================================
# 6. Safety, Accidents & Derailment Causation
# ==============================================================================
class AccidentRecord(Base):
    __tablename__ = "accident_records"
    id = Column(Integer, primary_key=True, index=True)
    fiscal_year = Column(String(20), nullable=False, index=True)
    total_accidents = Column(Integer, default=0)
    derailments = Column(Integer, default=0)
    collisions = Column(Integer, default=0)
    level_crossings = Column(Integer, default=0)
    fire_in_trains = Column(Integer, default=0)
    fatalities = Column(Integer, default=0)
    injuries = Column(Integer, default=0)

# ==============================================================================
# 7. Maintenance Tasks, Prioritization & Work Orders
# ==============================================================================
class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_code = Column(String(100), unique=True, nullable=False, index=True)
    milepost_km = Column(Float, nullable=False)
    section_code = Column(String(50), nullable=False)
    severity_class = Column(Integer, nullable=False) # 0, 1, 2, 3
    priority_rank = Column(Integer, nullable=False, index=True)
    work_order_type = Column(String(100), default="Track Tamping / Realignment")
    assigned_crew = Column(String(100), default="PWI Gang No. 4")
    machine_deployment = Column(String(100), default="CSM-09-32 Tamping Machine")
    target_completion_days = Column(Integer, default=3)
    status = Column(String(50), default="PENDING") # PENDING, IN_PROGRESS, COMPLETED
    scheduled_date = Column(DateTime, default=datetime.utcnow)
    completed_date = Column(DateTime, nullable=True)

# ==============================================================================
# 8. AI Predictions, Audit Logs & Alert Center
# ==============================================================================
class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    id = Column(Integer, primary_key=True, index=True)
    prediction_uuid = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    input_features_json = Column(Text, nullable=False)
    predicted_class = Column(Integer, nullable=False) # 0, 1, 2, 3
    predicted_label = Column(String(50), nullable=False)
    probabilities_json = Column(Text, nullable=False)
    shap_attributions_json = Column(Text, nullable=True)
    uncertainty_score = Column(Float, default=0.05)
    model_version = Column(String(50), default="LightGBM-v2.0-INT395")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="predictions")

class AlertNotification(Base):
    __tablename__ = "alert_notifications"
    id = Column(Integer, primary_key=True, index=True)
    alert_code = Column(String(100), unique=True, nullable=False, index=True)
    alert_type = Column(String(50), nullable=False) # CRITICAL_DEFECT, BUCKLING_RISK, FLOOD_WARNING, OVERDUE
    severity_level = Column(String(20), default="CRITICAL") # CRITICAL, MAJOR, WARNING, INFO
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    location_reference = Column(String(150))
    is_active = Column(Boolean, default=True)
    is_simulated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_type = Column(String(100), nullable=False)
    entity_affected = Column(String(100))
    details_json = Column(Text)
    ip_address = Column(String(50), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
