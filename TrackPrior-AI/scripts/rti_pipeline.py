"""
TrackPrior AI — RTI Indian Railways TMS Data Integration Pipeline
Modular ingestion, schema harmonization, and engineering standard verification engine
for future official Indian Railways Track Management System (TMS) inspection records.
Supports CSV, Excel, and Parquet across heterogeneous zonal railway formats.
Classifies defect severity against official IRPWM 2020 / RDSO thresholds.
"""

import os
import sys
import json
import argparse
import datetime
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STANDARDS_PATH = os.path.join(DATA_DIR, 'raw', 'standards', 'irpwm_geometry_thresholds.csv')

class RTIIndianRailwaysTMSPipeline:
    """
    Ingestion engine for Indian Railways TMS records obtained via RTI.
    Handles schema variations across all 17 Zonal Railways and 68 Divisions.
    """
    
    STANDARD_TMS_SCHEMA = {
        'zone': 'Zonal Railway code (e.g., NR, WR, CR, SR)',
        'division': 'Railway Division (e.g., Delhi, Mumbai Central, Howrah)',
        'block_section': 'Block section identifying the track corridor',
        'track_line': 'Track identifier (UP Main, DN Main, Single, Branch)',
        'km_start': 'Start kilometrage / Chainage (km)',
        'km_end': 'End kilometrage / Chainage (km)',
        'inspection_date': 'Date of TRC / OMS inspection run (ISO format)',
        'inspection_type': 'Inspection modality (TRC, OMS-2000, USFD, Visual)',
        'geometry_parameter': 'Standard track parameter (Gauge, Unevenness, Alignment, Twist, Peak Accel)',
        'measured_value': 'Peak recorded defect measurement',
        'measurement_unit': 'Unit of measurement (mm, mm/m, g)',
        'sectional_speed_kmph': 'Permissible sectional speed (km/h)',
        'tms_defect_category': 'Raw recorded priority/urgency in TMS record',
        'standardized_severity': 'Harmonized severity (UML, NBML, PML, NORMAL)',
        'maintenance_action': 'Recorded corrective maintenance action taken',
        'rectification_date': 'Date of defect rectification'
    }

    COLUMN_MAPPINGS = {
        'zone': ['zone', 'railway_zone', 'rly', 'railway', 'zonal_railway'],
        'division': ['division', 'div', 'rly_div', 'division_name'],
        'block_section': ['block_section', 'section', 'sec_name', 'track_section', 'from_to_station', 'section_name'],
        'track_line': ['track_line', 'line', 'line_no', 'track_no', 'up_dn', 'direction', 'road', 'track'],
        'km_start': ['km_start', 'km_from', 'from_km', 'start_km', 'location_km', 'km', 'milepost'],
        'km_end': ['km_end', 'km_to', 'to_km', 'end_km', 'milepost_end'],
        'inspection_date': ['inspection_date', 'run_date', 'test_date', 'trc_date', 'date_of_run', 'test_dt', 'date'],
        'inspection_type': ['inspection_type', 'car_type', 'trc_no', 'machine_type', 'inspection_system', 'oms_no'],
        'geometry_parameter': ['geometry_parameter', 'parameter', 'param_name', 'param', 'defect_type', 'channel', 'defect_description', 'parameter_name'],
        'measured_value': ['measured_value', 'peak_value', 'amplitude', 'value_mm', 'exceedance', 'max_value', 'value'],
        'measurement_unit': ['measurement_unit', 'unit', 'units', 'dim'],
        'sectional_speed_kmph': ['sectional_speed_kmph', 'speed', 'speed_kmph', 'sectional_speed', 'max_speed', 'f_speed'],
        'tms_defect_category': ['tms_defect_category', 'severity', 'category', 'urgency', 'defect_class', 'action_required', 'priority'],
        'maintenance_action': ['maintenance_action', 'action_taken', 'tamping_done', 'speed_restriction_imposed', 'action'],
        'rectification_date': ['rectification_date', 'attended_date', 'action_date', 'date_rectified']
    }

    def __init__(self, standards_file=None):
        self.standards_file = standards_file or STANDARDS_PATH
        self.standards_df = None
        if os.path.exists(self.standards_file):
            self.standards_df = pd.read_csv(self.standards_file)

    def load_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TMS file not found: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif ext == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported TMS format {ext}. Use .csv, .xlsx, or .parquet")

    def map_columns(self, df):
        orig_cols = list(df.columns)
        mapping = {}
        lower_orig = {c.lower().strip().replace(' ', '_'): c for c in orig_cols}
        
        for std_col, aliases in self.COLUMN_MAPPINGS.items():
            for alias in aliases:
                cand = alias.lower().strip().replace(' ', '_')
                if cand in lower_orig:
                    mapping[lower_orig[cand]] = std_col
                    break
        
        df_mapped = df.rename(columns=mapping).copy()
        missing_std = [c for c in self.STANDARD_TMS_SCHEMA.keys() if c not in df_mapped.columns]
        return df_mapped, missing_std

    def standardize_severity(self, df):
        """
        Standardizes defect severity according to IRPWM 2020:
        UML: Urgent Maintenance Limit (Mandates immediate speed reduction / emergency correction)
        NBML: Need Based Maintenance Limit (Isolated defect requiring scheduled spot correction)
        PML: Planned Maintenance Limit (Through tamping / programmed overhaul)
        NORMAL: Within permissible operational tolerances
        """
        df['standardized_severity'] = 'NORMAL'
        
        # 1. Use recorded TMS category if present
        if 'tms_defect_category' in df.columns:
            cat_str = df['tms_defect_category'].astype(str).str.upper().str.strip()
            uml_mask = cat_str.str.contains('URGENT|UML|RED|CRITICAL|EMERGENCY|RESTRICTION|IMMEDIATE')
            nbml_mask = cat_str.str.contains('NEED|NBML|YELLOW|SPOT|WARNING|ATTENTION|PLANNED_SPOT')
            pml_mask = cat_str.str.contains('PLANNED|PML|TAMPING|ROUTINE|THROUGH')
            
            df.loc[pml_mask, 'standardized_severity'] = 'PML'
            df.loc[nbml_mask, 'standardized_severity'] = 'NBML'
            df.loc[uml_mask, 'standardized_severity'] = 'UML'
            
        # 2. If numerical measurements and parameter names are available, cross-verify against IRPWM 2020 limits
        if 'measured_value' in df.columns and 'geometry_parameter' in df.columns:
            df['measured_value'] = pd.to_numeric(df['measured_value'], errors='coerce')
            param_lower = df['geometry_parameter'].astype(str).str.lower()
            
            # Twist UML (> 3.5 to 5.0 mm/m)
            twist_mask = param_lower.str.contains('twist') & (df['measured_value'].abs() >= 4.0)
            df.loc[twist_mask, 'standardized_severity'] = 'UML'
            
            # Gauge slack UML (> +10 mm) or tight UML (< -6 mm)
            gauge_slack_uml = param_lower.str.contains('gauge') & (df['measured_value'] >= 10.0)
            gauge_tight_uml = param_lower.str.contains('gauge') & (df['measured_value'] <= -6.0)
            df.loc[gauge_slack_uml | gauge_tight_uml, 'standardized_severity'] = 'UML'
            
            # Crosslevel UML (>= 12.0 mm) and NBML (>= 8.0 mm)
            xlevel_uml = param_lower.str.contains('crosslevel|xlevel|cant') & (df['measured_value'].abs() >= 12.0)
            xlevel_nbml = param_lower.str.contains('crosslevel|xlevel|cant') & (df['measured_value'].abs() >= 8.0) & ~xlevel_uml
            df.loc[xlevel_nbml, 'standardized_severity'] = 'NBML'
            df.loc[xlevel_uml, 'standardized_severity'] = 'UML'

            # Unevenness / Surface Profile UML (>= 10.0 mm) and NBML (>= 6.0 mm)
            surf_uml = param_lower.str.contains('unevenness|surface|profile|dip') & (df['measured_value'].abs() >= 10.0)
            surf_nbml = param_lower.str.contains('unevenness|surface|profile|dip') & (df['measured_value'].abs() >= 6.0) & ~surf_uml
            df.loc[surf_nbml, 'standardized_severity'] = 'NBML'
            df.loc[surf_uml, 'standardized_severity'] = 'UML'

            # Peak acceleration UML (> 0.25g / 0.30g)
            accel_uml = param_lower.str.contains('accel') & (df['measured_value'].abs() >= 0.25)
            df.loc[accel_uml, 'standardized_severity'] = 'UML'
            
        return df

    def process_dataframe(self, df_raw, source_filename="uploaded_tms.csv", output_dir=None):
        df_mapped, missing = self.map_columns(df_raw)
        
        if 'inspection_date' in df_mapped.columns:
            df_mapped['inspection_date'] = pd.to_datetime(df_mapped['inspection_date'], errors='coerce')
        if 'rectification_date' in df_mapped.columns:
            df_mapped['rectification_date'] = pd.to_datetime(df_mapped['rectification_date'], errors='coerce')
            
        df_clean = self.standardize_severity(df_mapped)
        
        audit = {
            "source_file": source_filename,
            "ingested_records": len(df_clean),
            "unmapped_standard_fields": missing,
            "zonal_railways_detected": df_clean['zone'].dropna().unique().tolist() if 'zone' in df_clean.columns else [],
            "divisions_detected": df_clean['division'].dropna().unique().tolist() if 'division' in df_clean.columns else [],
            "severity_distribution": df_clean['standardized_severity'].value_counts().to_dict(),
            "pipeline_status": "READY_FOR_FEATURE_STORE"
        }
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(source_filename)[0]
            out_parquet = os.path.join(output_dir, f"standardized_tms_{base_name}.parquet")
            df_clean.to_parquet(out_parquet, index=False)
            audit["output_parquet"] = out_parquet
            
        return df_clean, audit

    def process_tms_file(self, file_path, output_dir=None):
        print(f"Processing Indian Railways TMS file: {file_path}")
        df_raw = self.load_file(file_path)
        return self.process_dataframe(df_raw, source_filename=os.path.basename(file_path), output_dir=output_dir)

def main():
    parser = argparse.ArgumentParser(description="Indian Railways RTI TMS Integration Engine")
    parser.add_argument("--file", type=str, required=True, help="Path to TMS record file (CSV, XLSX, Parquet)")
    parser.add_argument("--out-dir", type=str, default=os.path.join(DATA_DIR, 'processed'), help="Output directory")
    args = parser.parse_args()

    pipeline = RTIIndianRailwaysTMSPipeline()
    df, audit = pipeline.process_tms_file(args.file, args.out_dir)
    print("\nTMS Ingestion Audit Summary:")
    print(json.dumps(audit, indent=2))

if __name__ == '__main__':
    main()
