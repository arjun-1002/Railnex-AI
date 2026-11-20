"""
RailRakshak AI — Extended Railway Safety & Accident Statistics (2015–2024)
Data Source: Ministry of Railways Annual Statistical Statements,
Comptroller & Auditor General of India (CAG Report No. 22 of 2022 on Derailment in Indian Railways),
and Commission of Railway Safety (CRS) Investigation Summaries.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "accidents")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 10 Fiscal Years of National Consequential Train Accidents
HISTORICAL_ACCIDENTS = [
    {"fiscal_year": "2014-15", "total_consequential_accidents": 135, "derailments": 63, "collisions": 5, "level_crossing_incidents": 56, "fire_in_trains": 11, "misc_accidents": 0, "fatalities": 292, "injuries": 473},
    {"fiscal_year": "2015-16", "total_consequential_accidents": 107, "derailments": 65, "collisions": 3, "level_crossing_incidents": 35, "fire_in_trains": 4, "misc_accidents": 0, "fatalities": 122, "injuries": 204},
    {"fiscal_year": "2016-17", "total_consequential_accidents": 104, "derailments": 78, "collisions": 5, "level_crossing_incidents": 20, "fire_in_trains": 1, "misc_accidents": 0, "fatalities": 238, "injuries": 381},
    {"fiscal_year": "2017-18", "total_consequential_accidents": 73, "derailments": 54, "collisions": 3, "level_crossing_incidents": 13, "fire_in_trains": 3, "misc_accidents": 0, "fatalities": 57, "injuries": 202},
    {"fiscal_year": "2018-19", "total_consequential_accidents": 59, "derailments": 46, "collisions": 0, "level_crossing_incidents": 6, "fire_in_trains": 6, "misc_accidents": 1, "fatalities": 37, "injuries": 108},
    {"fiscal_year": "2019-20", "total_consequential_accidents": 55, "derailments": 40, "collisions": 5, "level_crossing_incidents": 1, "fire_in_trains": 8, "misc_accidents": 1, "fatalities": 0, "injuries": 0},
    {"fiscal_year": "2020-21", "total_consequential_accidents": 22, "derailments": 17, "collisions": 1, "level_crossing_incidents": 1, "fire_in_trains": 3, "misc_accidents": 0, "fatalities": 0, "injuries": 0},
    {"fiscal_year": "2021-22", "total_consequential_accidents": 35, "derailments": 26, "collisions": 2, "level_crossing_incidents": 1, "fire_in_trains": 6, "misc_accidents": 0, "fatalities": 9, "injuries": 45},
    {"fiscal_year": "2022-23", "total_consequential_accidents": 48, "derailments": 36, "collisions": 6, "level_crossing_incidents": 0, "fire_in_trains": 6, "misc_accidents": 0, "fatalities": 296, "injuries": 1200},
    {"fiscal_year": "2023-24", "total_consequential_accidents": 40, "derailments": 31, "collisions": 4, "level_crossing_incidents": 0, "fire_in_trains": 5, "misc_accidents": 0, "fatalities": 14, "injuries": 52},
]

# Track-Related Derailment Specific Causation (CAG Report No. 22 of 2022 Audit Analysis)
TRACK_DEFECT_DERAILMENT_SUBCAUSES = [
    {"track_causation_category": "Track Gauge Widening / Slack Gauge", "incident_count_cag_audit": 118, "pct_share_of_track_causes": 28.0, "primary_contributing_mechanism": "Decayed wooden/damaged PSC sleeper seats, missing/worn ERC clips, widened dynamic gauge under lateral hunting oscillation", "speed_restriction_mandated": "Yes (30-45 km/h)", "irpwn_para_reference": "IRPWM Para 5.1 Gauge Variation"},
    {"track_causation_category": "Excessive Crosslevel Variation / Twist", "incident_count_cag_audit": 96, "pct_share_of_track_causes": 22.7, "primary_contributing_mechanism": "Differential ballast settlement on approaches to bridges and level crossings, wheel unloading triggering flange climbing (Nadal Criterion)", "speed_restriction_mandated": "Yes (Emergency stop or 20 km/h)", "irpwn_para_reference": "IRPWM Para 5.1 Track Twist"},
    {"track_causation_category": "Rail Fracture / Weld Joint Failure", "incident_count_cag_audit": 84, "pct_share_of_track_causes": 19.9, "primary_contributing_mechanism": "Internal transverse fatigue fissures, AT weld porosity, high tensile stress during winter thermal drop below destressing temp (Td - 25 C)", "speed_restriction_mandated": "Yes (Stop train, joggled fishplate)", "irpwn_para_reference": "IRPWM Para 5.1 & RDSO USFD Manual"},
    {"track_causation_category": "Track Buckling / Thermal Misalignment", "incident_count_cag_audit": 48, "pct_share_of_track_causes": 11.4, "primary_contributing_mechanism": "High compressive thermal stress when rail temperature exceeds Td + 20 C in deficient ballast shoulder conditions (< 350mm)", "speed_restriction_mandated": "Yes (Imposition of temporary speed restriction 30 km/h during peak heat hours)", "irpwn_para_reference": "IRPWM Chapter 8 LWR Manual"},
    {"track_causation_category": "Turnout / Points & Crossings Defect", "incident_count_cag_audit": 42, "pct_share_of_track_causes": 10.0, "primary_contributing_mechanism": "Chipped switch rail tongue, gap at switch toe > 3mm, excessive nose wear of crossing, deficient check rail clearance", "speed_restriction_mandated": "Yes (15-30 km/h over turnout)", "irpwn_para_reference": "IRPWM Table 5.2 Points and Crossings"},
    {"track_causation_category": "Ballast Fouling & Waterlogging / Subgrade", "incident_count_cag_audit": 34, "pct_share_of_track_causes": 8.1, "primary_contributing_mechanism": "Pumping joints, cess deterioration, drainage clogging during monsoon leading to ballast liquefaction under 22.82t axle loading", "speed_restriction_mandated": "Yes (Deep screening and ballast recoupment required)", "irpwn_para_reference": "IRPWM Chapter 6 Drainage & Formation"},
]

def main():
    df_acc = pd.DataFrame(HISTORICAL_ACCIDENTS)
    acc_path = os.path.join(OUTPUT_DIR, "indian_railways_accidents_2015_2024.csv")
    df_acc.to_csv(acc_path, index=False)

    df_track = pd.DataFrame(TRACK_DEFECT_DERAILMENT_SUBCAUSES)
    track_path = os.path.join(OUTPUT_DIR, "cag_derailment_track_subcauses_audit.csv")
    df_track.to_csv(track_path, index=False)

    print(f"[SUCCESS] Compiled 10-Year Consequential Train Accidents (2015-2024: {len(df_acc)} fiscal years)!")
    print(f"[SUCCESS] Compiled Granular CAG Track Derailment Subcauses ({len(df_track)} causation categories)!")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
