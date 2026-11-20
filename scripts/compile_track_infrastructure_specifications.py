"""
RailRakshak AI — Track Infrastructure Engineering Specifications
Data Source: Indian Railways Permanent Way Manual (IRPWM 2020),
RDSO Guidelines for Track Structure & Track Renewal Standards.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "standards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TRACK_SPECIFICATIONS = [
    # Rail Sections
    {"category": "Rail Section", "type": "60 kg/m (UIC 60)", "steel_grade": "90 UTS", "yield_strength_mpa": 460, "tensile_strength_mpa": 880, "standard_application": "Broad Gauge Group A & B routes, High Density Corridors", "axle_load_max_tonnes": 25.0, "design_speed_max_kmh": 160},
    {"category": "Rail Section", "type": "60 kg/m (UIC 60)", "steel_grade": "110 UTS (Micro-alloyed)", "yield_strength_mpa": 560, "tensile_strength_mpa": 1080, "standard_application": "Dedicated Freight Corridors (DFC), Heavy Haul (CC+8+2, CC+6+2)", "axle_load_max_tonnes": 32.5, "design_speed_max_kmh": 100},
    {"category": "Rail Section", "type": "52 kg/m", "steel_grade": "90 UTS", "yield_strength_mpa": 410, "tensile_strength_mpa": 880, "standard_application": "Broad Gauge Group C & D routes, Secondary Main lines", "axle_load_max_tonnes": 22.82, "design_speed_max_kmh": 110},
    {"category": "Rail Section", "type": "90 R (Older section)", "steel_grade": "72 UTS", "yield_strength_mpa": 350, "tensile_strength_mpa": 710, "standard_application": "Branch lines, Loop lines, Yard sidings", "axle_load_max_tonnes": 18.0, "design_speed_max_kmh": 75},

    # Sleeper Specifications
    {"category": "Sleeper", "type": "PSC Sleeper RT-2496 (60 kg)", "weight_kg": 298.0, "sleeper_spacing_mm": 600, "density_per_km": 1660, "standard_application": "Group A & B routes, LWR/CWR Track", "service_life_years": 40, "fastening_system": "Elastic Rail Clip (ERC Mk-III/V)"},
    {"category": "Sleeper", "type": "PSC Sleeper RT-2495 (52 kg)", "weight_kg": 285.0, "sleeper_spacing_mm": 650, "density_per_km": 1540, "standard_application": "Group C, D & E routes", "service_life_years": 35, "fastening_system": "Elastic Rail Clip (ERC Mk-III)"},
    {"category": "Sleeper", "type": "Wider PSC Sleeper RT-8521", "weight_kg": 345.0, "sleeper_spacing_mm": 600, "density_per_km": 1660, "standard_application": "25t Axle Load DFC & Feeder Routes", "service_life_years": 45, "fastening_system": "Heavy Duty ERC Mk-V with GFN Liners"},

    # Ballast Cushion Depth Standards
    {"category": "Ballast Cushion", "type": "Clean Crushed Stone 50mm", "cushion_depth_mm": 350, "shoulders_width_straight_mm": 350, "shoulders_width_curve_mm": 500, "standard_application": "Group A routes (V >= 130 km/h) & 25t DFC routes", "maintenance_tamping_cycle_gmt": 50},
    {"category": "Ballast Cushion", "type": "Clean Crushed Stone 50mm", "cushion_depth_mm": 300, "shoulders_width_straight_mm": 350, "shoulders_width_curve_mm": 450, "standard_application": "Group B & C routes (110 <= V < 130 km/h)", "maintenance_tamping_cycle_gmt": 65},
    {"category": "Ballast Cushion", "type": "Clean Crushed Stone 50mm", "cushion_depth_mm": 250, "shoulders_width_straight_mm": 300, "shoulders_width_curve_mm": 400, "standard_application": "Group D & E routes (V < 100 km/h)", "maintenance_tamping_cycle_gmt": 80},

    # Turnouts / Points & Crossings
    {"category": "Turnout", "type": "1 in 12 Curved Switch (CMS Crossing)", "lead_curve_radius_m": 441.36, "switch_entry_angle_deg": 0.54, "permissible_diverging_speed_kmh": 50, "standard_application": "Mainline Loops & Junction crossovers", "inspection_frequency_days": 30},
    {"category": "Turnout", "type": "1 in 8.5 Curved Switch (CMS Crossing)", "lead_curve_radius_m": 218.89, "switch_entry_angle_deg": 0.78, "permissible_diverging_speed_kmh": 25, "standard_application": "Station yards & terminal sidings", "inspection_frequency_days": 30},
    {"category": "Turnout", "type": "1 in 16 High-Speed Crossover (Thick Web Switch)", "lead_curve_radius_m": 782.0, "switch_entry_angle_deg": 0.38, "permissible_diverging_speed_kmh": 65, "standard_application": "High speed quadruple track overtaking loops", "inspection_frequency_days": 15},
]

def main():
    df = pd.DataFrame(TRACK_SPECIFICATIONS)
    csv_path = os.path.join(OUTPUT_DIR, "indian_railways_track_specifications.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SUCCESS] Compiled Indian Railways Track Infrastructure Specifications ({len(df)} engineering entries)!")
    print(f"Saved to: {csv_path}")

if __name__ == "__main__":
    main()
