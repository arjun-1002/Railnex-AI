"""
RailRakshak AI — Database Initialization & Dataset Seeding Script
Creates all tables and seeds administrative records, USFD standards,
accidents, and initial alerts into the SQLite/PostgreSQL database.
"""

import os
import hashlib
import pandas as pd
from datetime import datetime

from .session import engine, SessionLocal, Base
from .schema import (
    Role, User, RailwayZone, RailwayDivision, Station,
    UltrasonicInspection, AccidentRecord, AlertNotification
)
from ..config import BASE_DIR

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def seed_database():
    print("Creating all relational database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Roles
        if db.query(Role).count() == 0:
            print("Seeding RBAC Roles...")
            roles = [
                Role(name="Admin", description="Full System Administrator", can_upload_data=True, can_trigger_training=True, can_approve_maintenance=True),
                Role(name="Engineer", description="Senior Section Engineer / Track Researcher", can_upload_data=True, can_trigger_training=True, can_approve_maintenance=False),
                Role(name="Viewer", description="Auditor / Read-Only Analyst", can_upload_data=False, can_trigger_training=False, can_approve_maintenance=False),
            ]
            db.add_all(roles)
            db.commit()

        # 2. Seed Default Users
        if db.query(User).count() == 0:
            print("Seeding Initial Users...")
            admin_role = db.query(Role).filter_by(name="Admin").first()
            eng_role = db.query(Role).filter_by(name="Engineer").first()

            users = [
                User(
                    username="admin",
                    email="admin@railrakshak.ir.gov.in",
                    hashed_password=hash_pw("RailRakshak@2026"),
                    role_id=admin_role.id,
                    full_name="Chief Track Engineer (P-Way)",
                    zone_code="NR"
                ),
                User(
                    username="sse_pway",
                    email="sse.track@nr.railnet.gov.in",
                    hashed_password=hash_pw("TrackSafe@2026"),
                    role_id=eng_role.id,
                    full_name="Sr. Section Engineer (Track Monitoring)",
                    zone_code="NCR"
                )
            ]
            db.add_all(users)
            db.commit()

        # 3. Seed Railway Zones & Divisions
        zones_csv = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "railway_network", "indian_railway_zones_and_divisions.csv")
        if os.path.exists(zones_csv) and db.query(RailwayDivision).count() == 0:
            print("Seeding Zonal Railways & Operating Divisions...")
            df_div = pd.read_csv(zones_csv)
            
            # Unique Zones
            zones_seen = set()
            for _, r in df_div.iterrows():
                zc = r["zone_code"]
                if zc not in zones_seen:
                    zones_seen.add(zc)
                    z_rec = RailwayZone(
                        zone_code=zc,
                        zone_name=r["zone_name"],
                        zone_hq=r["zone_hq"],
                        total_route_km=float(df_div[df_div["zone_code"] == zc]["route_km"].sum()),
                        total_running_km=float(df_div[df_div["zone_code"] == zc]["running_track_km"].sum()),
                    )
                    db.add(z_rec)
            db.commit()

            # Divisions
            for _, r in df_div.iterrows():
                d_rec = RailwayDivision(
                    division_code=r["division_code"],
                    division_name=r["division_name"],
                    div_hq=r["div_hq"],
                    zone_code=r["zone_code"],
                    state=str(r["state"]),
                    route_km=float(r["route_km"]),
                    running_track_km=float(r["running_track_km"]),
                    speed_band_max=int(r["speed_band_max"]),
                )
                db.add(d_rec)
            db.commit()
            print(f"Seeded {len(zones_seen)} Zones and {len(df_div)} Divisions successfully.")

        # 4. Seed Accident Records
        acc_csv = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "accidents", "indian_railways_accidents_2015_2024.csv")
        if os.path.exists(acc_csv) and db.query(AccidentRecord).count() == 0:
            print("Seeding 10-Year Accident Records...")
            df_acc = pd.read_csv(acc_csv)
            for _, r in df_acc.iterrows():
                db.add(AccidentRecord(
                    fiscal_year=r["fiscal_year"],
                    total_accidents=int(r["total_consequential_accidents"]),
                    derailments=int(r["derailments"]),
                    collisions=int(r["collisions"]),
                    level_crossings=int(r["level_crossing_incidents"]),
                    fire_in_trains=int(r["fire_in_trains"]),
                    fatalities=int(r["fatalities"]),
                    injuries=int(r["injuries"]),
                ))
            db.commit()

        # 5. Seed Initial System Alerts
        if db.query(AlertNotification).count() == 0:
            print("Seeding Initial System Alerts...")
            alerts = [
                AlertNotification(
                    alert_code="ALT-NDLS-PRYJ-001",
                    alert_type="CRITICAL_DEFECT",
                    severity_level="CRITICAL",
                    title="Critical Crosslevel Exceedance Detected (MP 142.4)",
                    message="Track Recording Car run detected crosslevel anomaly of 24.2mm exceeding IRPWM 2020 Table 5.1 Urgent Maintenance Limit (UML: 22.0mm). Immediate 30 km/h speed restriction advised.",
                    location_reference="Northern Railway / Delhi Division / MP 142.4",
                    is_active=True,
                    is_simulated=False
                ),
                AlertNotification(
                    alert_code="ALT-NWR-BKN-002",
                    alert_type="BUCKLING_RISK",
                    severity_level="MAJOR",
                    title="High Thermal Buckling Risk Warning (Bikaner Division)",
                    message="Open-Meteo ambient temperature forecast > 44.5 C projects continuous welded rail (LWR) temperature > 62.5 C. Deploy hot weather keymen patrols from 11:00 to 17:00 hrs.",
                    location_reference="North Western Railway / Bikaner Division",
                    is_active=True,
                    is_simulated=False
                ),
                AlertNotification(
                    alert_code="ALT-NFR-APDJ-003",
                    alert_type="FLOOD_WARNING",
                    severity_level="WARNING",
                    title="Monsoon Waterlogging & River Gauge Advisory",
                    message="Heavy rainfall observed in Teesta river basin. Stationary bridge watchmen deployed at vulnerable culverts as per Monsoon Precautionary Orders.",
                    location_reference="Northeast Frontier Railway / Alipurduar Division",
                    is_active=True,
                    is_simulated=False
                )
            ]
            db.add_all(alerts)
            db.commit()

        print("[SUCCESS] RailRakshak AI Database Initialized & Seeded Successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
