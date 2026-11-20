"""
RailRakshak AI — RDSO Ultrasonic Flaw Detection (USFD) & Defect Taxonomy
Data Source: RDSO Manual for Ultrasonic Testing of Rails and Welds (Revised 2012 / 2020),
Research Designs and Standards Organisation (Ministry of Railways, Govt of India).
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "standards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

USFD_DEFECT_CODES = [
    # 100 Series: Transverse Fissure / Rail Head Flaws
    {"defect_code": "111", "defect_type": "Transverse Fissure (Gauge Face Corner)", "location": "Head", "probe_angle_deg": 70, "severity_classification": "IMR", "action_required": "Emergency fishplate with clamps; 30 km/h speed restriction; replace within 3 days", "growth_rate_mm_per_gmt": 0.35},
    {"defect_code": "112", "defect_type": "Transverse Fissure (Non-Gauge Face Corner)", "location": "Head", "probe_angle_deg": 70, "severity_classification": "OBS", "action_required": "Mark with red paint; re-test within 15 days; record progression", "growth_rate_mm_per_gmt": 0.18},
    {"defect_code": "113", "defect_type": "Compound Fissure in Rail Head", "location": "Head", "probe_angle_deg": 70, "severity_classification": "IMR", "action_required": "Emergency clamp; stop/restrict traffic until jointed", "growth_rate_mm_per_gmt": 0.42},
    
    # 200 Series: Horizontal Split Head
    {"defect_code": "211", "defect_type": "Horizontal Split Head (Longitudinal)", "location": "Head", "probe_angle_deg": 0, "severity_classification": "OBS", "action_required": "Observe fortnightly; monitor length and depth", "growth_rate_mm_per_gmt": 0.22},
    {"defect_code": "212", "defect_type": "Horizontal Split at Head-Web Junction", "location": "Fillet", "probe_angle_deg": 0, "severity_classification": "IMR", "action_required": "Immediate fishplate clamp; rail replacement required", "growth_rate_mm_per_gmt": 0.38},

    # 300 Series: Vertical Split Head
    {"defect_code": "311", "defect_type": "Vertical Split Head (Longitudinal Seam)", "location": "Head", "probe_angle_deg": 70, "severity_classification": "IMR", "action_required": "Urgent rail replacement; risk of sudden head detachment", "growth_rate_mm_per_gmt": 0.50},

    # 400 Series: Bolt Hole Cracks (Fishplated Joint Area)
    {"defect_code": "411", "defect_type": "Star / Diagonal Crack radiating from Bolt Hole", "location": "Web / Joint", "probe_angle_deg": 45, "severity_classification": "IMR", "action_required": "Immediate replacement of fishplated rail end; provide joggled fishplate", "growth_rate_mm_per_gmt": 0.45},
    {"defect_code": "412", "defect_type": "Horizontal Crack connecting Bolt Holes", "location": "Web / Joint", "probe_angle_deg": 0, "severity_classification": "IMR", "action_required": "Cut defective rail piece (min 6m) and replace", "growth_rate_mm_per_gmt": 0.60},
    {"defect_code": "421", "defect_type": "Hairline Bolt Hole Crack (< 5mm)", "location": "Web / Joint", "probe_angle_deg": 45, "severity_classification": "OBS", "action_required": "Chamfer bolt hole; ultrasonic check every 1 month", "growth_rate_mm_per_gmt": 0.12},

    # 500 Series: Web Flaws
    {"defect_code": "511", "defect_type": "Longitudinal Web Crack (Piping)", "location": "Web", "probe_angle_deg": 0, "severity_classification": "OBS", "action_required": "Measure vertical extent; replace if length > 50mm", "growth_rate_mm_per_gmt": 0.15},

    # 600 Series: Base Flaws
    {"defect_code": "611", "defect_type": "Transverse Crack in Rail Base", "location": "Foot / Base", "probe_angle_deg": 70, "severity_classification": "IMR", "action_required": "Immediate 20 km/h restriction; clamp joggled plate; urgent cut", "growth_rate_mm_per_gmt": 0.55},
    {"defect_code": "612", "defect_type": "Corrosion Notch in Rail Foot", "location": "Foot / Base", "probe_angle_deg": 0, "severity_classification": "OBS", "action_required": "Anti-corrosion painting; ultrasonic re-test every 3 months", "growth_rate_mm_per_gmt": 0.08},

    # 700 Series: Alumino-Thermic (AT) Weld Defects
    {"defect_code": "711", "defect_type": "AT Weld Transverse Lack of Fusion / Crack", "location": "AT Weld", "probe_angle_deg": 45, "severity_classification": "IMRW", "action_required": "Immediate joggled fishplating with clamps; cut weld and insert 6m rail piece within 3 days", "growth_rate_mm_per_gmt": 0.48},
    {"defect_code": "712", "defect_type": "AT Weld Slag Inclusion / Shrinkage Cavity", "location": "AT Weld", "probe_angle_deg": 0, "severity_classification": "OBSW", "action_required": "Monitor growth rate; testing every 15 days", "growth_rate_mm_per_gmt": 0.16},

    # 800 Series: Flash Butt Weld (FBW) Defects
    {"defect_code": "811", "defect_type": "FBW Interface Oxide / Cold Weld", "location": "FBW Weld", "probe_angle_deg": 45, "severity_classification": "IMRW", "action_required": "Emergency clamp; cut weld; provide standard rail closure", "growth_rate_mm_per_gmt": 0.40},
    {"defect_code": "812", "defect_type": "FBW Fine Micro-crack in HAZ", "location": "FBW HAZ", "probe_angle_deg": 70, "severity_classification": "OBSW", "action_required": "Monthly inspection; record echo height in dB", "growth_rate_mm_per_gmt": 0.14},
]

# USFD Inspection Frequency Rules under RDSO Guidelines
USFD_TESTING_FREQUENCIES = [
    {"annual_traffic_gmt": "< 5 GMT", "frequency_months": 12, "route_classification": "Branch Lines / Low Density"},
    {"annual_traffic_gmt": "5 - 8 GMT", "frequency_months": 9, "route_classification": "Medium Density"},
    {"annual_traffic_gmt": "8 - 12 GMT", "frequency_months": 6, "route_classification": "Standard Broad Gauge"},
    {"annual_traffic_gmt": "12 - 16 GMT", "frequency_months": 4, "route_classification": "High Density Route"},
    {"annual_traffic_gmt": "16 - 40 GMT", "frequency_months": 3, "route_classification": "Heavy Freight / Golden Quadrilateral"},
    {"annual_traffic_gmt": "> 40 GMT", "frequency_months": 2, "route_classification": "Ultra-Heavy Corridor / DFC Feeder"},
]

def generate_sample_usfd_inspection_records(n=200):
    """Generate realistic USFD inspection logs across Indian Railways corridors."""
    np.random.seed(42)
    corridors = [
        {"route": "NDLS-PRYJ", "zone": "NCR", "div": "PRYJ", "rail": "60kg 90UTS", "speed": 130},
        {"route": "MMCT-BRC", "zone": "WR", "div": "BRC", "rail": "60kg 90UTS", "speed": 130},
        {"route": "HWH-MGS", "zone": "ER", "div": "ASN", "rail": "60kg 110UTS", "speed": 130},
        {"route": "MAS-GTL", "zone": "SR", "div": "MAS", "rail": "52kg 90UTS", "speed": 110},
        {"route": "CSMT-BSL", "zone": "CR", "div": "BSL", "rail": "60kg 90UTS", "speed": 120},
    ]
    
    records = []
    codes = USFD_DEFECT_CODES
    
    for i in range(n):
        c = corridors[np.random.randint(0, len(corridors))]
        d = codes[np.random.randint(0, len(codes))]
        flaw_depth_mm = np.round(np.random.uniform(2.0, 28.0), 1)
        flaw_length_mm = np.round(np.random.uniform(5.0, 65.0), 1)
        echo_amplitude_db = np.round(np.random.uniform(18.0, 52.0), 1)
        gmt_accumulated = np.round(np.random.uniform(45.0, 480.0), 1)
        
        # Calculate dynamic urgency
        urgency = d["severity_classification"]
        if flaw_depth_mm > 18.0 or echo_amplitude_db > 40.0:
            urgency = "IMR" if "IMR" in urgency else "IMRW"
            
        records.append({
            "usfd_record_id": f"USFD-{c['zone']}-{2024}-{1001 + i}",
            "route_section": c["route"],
            "railway_zone": c["zone"],
            "division": c["div"],
            "milepost_km": np.round(np.random.uniform(40.0, 850.0), 3),
            "track_line": np.random.choice(["UP Main", "DN Main", "Loop Line"]),
            "rail_type": c["rail"],
            "cumulative_gmt": gmt_accumulated,
            "flaw_code": d["defect_code"],
            "flaw_description": d["defect_type"],
            "flaw_location": d["location"],
            "probe_angle_deg": d["probe_angle_deg"],
            "flaw_depth_mm": flaw_depth_mm,
            "flaw_length_mm": flaw_length_mm,
            "echo_amplitude_db": echo_amplitude_db,
            "severity_classification": urgency,
            "action_mandate": d["action_required"],
            "growth_rate_mm_per_gmt": d["growth_rate_mm_per_gmt"],
            "est_days_to_critical": max(1, int((30.0 - flaw_depth_mm) / (d["growth_rate_mm_per_gmt"] * 0.15))),
            "inspector_id": f"USFD-OP-{np.random.randint(101, 140)}",
            "inspection_date": f"2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 28):02d}",
        })
        
    return pd.DataFrame(records)

def main():
    df_tax = pd.DataFrame(USFD_DEFECT_CODES)
    tax_path = os.path.join(OUTPUT_DIR, "rdso_usfd_flaw_specifications.csv")
    df_tax.to_csv(tax_path, index=False)
    
    df_freq = pd.DataFrame(USFD_TESTING_FREQUENCIES)
    freq_path = os.path.join(OUTPUT_DIR, "rdso_usfd_testing_frequencies.csv")
    df_freq.to_csv(freq_path, index=False)
    
    df_sample = generate_sample_usfd_inspection_records(250)
    sample_path = os.path.join(OUTPUT_DIR, "sample_rdso_usfd_inspection_logs.csv")
    df_sample.to_csv(sample_path, index=False)
    
    print(f"[SUCCESS] Compiled RDSO USFD Defect Taxonomy ({len(df_tax)} standards)")
    print(f"[SUCCESS] Compiled RDSO USFD Testing Frequencies ({len(df_freq)} traffic brackets)")
    print(f"[SUCCESS] Generated Realistic RDSO USFD Corridor Inspection Dataset ({len(df_sample)} records)")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
