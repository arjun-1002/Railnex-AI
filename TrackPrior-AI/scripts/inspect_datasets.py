"""
TrackPrior AI — Dataset Inspection and Quality Assessment Script
Calculates for every dataset:
1. Total records
2. Total columns
3. Missing-value percentages
4. Duplicate records
5. Numerical distributions
6. Categorical distributions
7. Date coverage
8. Geographic coverage
9. Target-label availability
10. Class imbalance
11. Potential target leakage
12. Data provenance and licensing
Generates quality visualizations in reports/figures/
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

os.makedirs(FIGURES_DIR, exist_ok=True)

def analyze_dataframe(df, name, provenance, licensing, target_col=None, date_col=None, geo_cols=None, leakage_candidates=None):
    n_rows = len(df)
    n_cols = len(df.columns)
    n_dupes = int(df.duplicated().sum())
    
    # Missing values
    missing_pct = {col: round(float(df[col].isna().sum() / n_rows * 100), 2) for col in df.columns}
    
    # Numerical distributions
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    num_summary = {}
    for col in num_cols:
        s = df[col].dropna()
        if not s.empty:
            num_summary[col] = {
                "mean": round(float(s.mean()), 3),
                "std": round(float(s.std()), 3) if len(s) > 1 else 0.0,
                "min": round(float(s.min()), 3),
                "q25": round(float(s.quantile(0.25)), 3),
                "median": round(float(s.median()), 3),
                "q75": round(float(s.quantile(0.75)), 3),
                "max": round(float(s.max()), 3)
            }
            
    # Categorical distributions
    cat_cols = df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    cat_summary = {}
    for col in cat_cols:
        vc = df[col].value_counts(dropna=False).head(10).to_dict()
        cat_summary[col] = {str(k): int(v) for k, v in vc.items()}
        
    # Date coverage
    date_coverage = None
    if date_col and date_col in df.columns:
        dt_s = pd.to_datetime(df[date_col], errors='coerce').dropna()
        if not dt_s.empty:
            date_coverage = {
                "start": dt_s.min().strftime('%Y-%m-%d'),
                "end": dt_s.max().strftime('%Y-%m-%d'),
                "total_days": int((dt_s.max() - dt_s.min()).days)
            }
            
    # Geographic coverage
    geo_coverage = None
    if geo_cols and all(c in df.columns for c in geo_cols):
        lat_col, lon_col = geo_cols
        lat_valid = pd.to_numeric(df[lat_col], errors='coerce').dropna()
        lon_valid = pd.to_numeric(df[lon_col], errors='coerce').dropna()
        if not lat_valid.empty and not lon_valid.empty:
            geo_coverage = {
                "latitude_min": round(float(lat_valid.min()), 4),
                "latitude_max": round(float(lat_valid.max()), 4),
                "longitude_min": round(float(lon_valid.min()), 4),
                "longitude_max": round(float(lon_valid.max()), 4)
            }

    # Target label and class imbalance
    target_info = None
    if target_col and target_col in df.columns:
        t_vc = df[target_col].value_counts(dropna=False).to_dict()
        target_info = {
            "target_column": target_col,
            "classes": {str(k): int(v) for k, v in t_vc.items()},
            "class_proportions": {str(k): round(float(v / n_rows * 100), 2) for k, v in t_vc.items()}
        }
        
    # Potential leakage
    leakage_analysis = {}
    if target_col and leakage_candidates:
        for cand in leakage_candidates:
            if cand in df.columns:
                # Check correlation or mutual association
                if pd.api.types.is_numeric_dtype(df[cand]) and pd.api.types.is_numeric_dtype(df[target_col]):
                    corr = df[[cand, target_col]].dropna().corr().iloc[0, 1]
                    leakage_analysis[cand] = {
                        "type": "numeric_correlation",
                        "correlation": round(float(corr), 4),
                        "risk": "HIGH" if abs(corr) > 0.85 else ("MEDIUM" if abs(corr) > 0.6 else "LOW")
                    }
                else:
                    leakage_analysis[cand] = {
                        "type": "categorical_or_mixed",
                        "risk": "HIGH (Post-failure/Inspection attribute; must be excluded from predictive inputs)"
                    }

    return {
        "dataset_name": name,
        "provenance": provenance,
        "licensing": licensing,
        "total_records": n_rows,
        "total_columns": n_cols,
        "duplicate_records": n_dupes,
        "missing_value_percentages": missing_pct,
        "numerical_distributions": num_summary,
        "categorical_distributions": cat_summary,
        "date_coverage": date_coverage,
        "geographic_coverage": geo_coverage,
        "target_information": target_info,
        "leakage_analysis": leakage_analysis
    }

def main():
    print("Running Dataset Quality Assessment across all 7 collected datasets...")
    audit_results = {}

    # 1. INFORMS Geometry Dataset (Real)
    informs_path = os.path.join(DATA_DIR, 'raw', 'informs', 'informs_training_geometry.parquet')
    if os.path.exists(informs_path):
        df_informs = pd.read_parquet(informs_path)
        audit_results['informs_geometry'] = analyze_dataframe(
            df=df_informs,
            name="INFORMS 2015 Track Geometry Analytics Dataset",
            provenance="INFORMS Railway Applications Section (RAS) Problem Solving Competition (2015)",
            licensing="Open Academic / Research Competition Dataset (Attribution required; not for commercial redistribution)",
            target_col='DEF_PRTY',
            date_col='TEST_DT',
            geo_cols=None,
            leakage_candidates=['DEF_NBR', 'GEO_CAR_NME']
        )
        print("Audited INFORMS Geometry dataset.")

    # 2. Hugging Face Synthetic Maintenance Dataset
    hf_path = os.path.join(DATA_DIR, 'raw', 'huggingface', 'Indian_Railway_maintenance_raw.parquet')
    if os.path.exists(hf_path):
        df_hf = pd.read_parquet(hf_path)
        audit_results['huggingface_maintenance_synthetic'] = analyze_dataframe(
            df=df_hf,
            name="Indian Railway Maintenance Dataset (Hugging Face - samyuktha01)",
            provenance="Hugging Face Hub (samyuktha01/Indian_Railway_maintance) - SYNTHETIC DATASET",
            licensing="Apache 2.0 / Open Source Community Data",
            target_col='failure_severity',
            date_col=None,
            geo_cols=None,
            leakage_candidates=['risk_score', 'maintenance_required', 'failure_type', 'inspection_score', 'delay_minutes']
        )
        print("Audited Hugging Face synthetic maintenance dataset.")

    # 3. Railway Stations (Network Geography)
    stations_path = os.path.join(DATA_DIR, 'raw', 'railway_network', 'railway_stations.csv')
    if os.path.exists(stations_path):
        df_stn = pd.read_csv(stations_path)
        audit_results['railway_stations'] = analyze_dataframe(
            df=df_stn,
            name="Indian Railways Operational Station Geography",
            provenance="OpenStreetMap & DataMeet Indian Railways Community Mapping Project",
            licensing="Open Database License (ODbL) / CC-BY-SA 2.0",
            target_col=None,
            date_col=None,
            geo_cols=['latitude', 'longitude']
        )
        print("Audited Railway Stations dataset.")

    # 4. Traffic Statistics
    traffic_path = os.path.join(DATA_DIR, 'raw', 'traffic', 'indian_railway_traffic_statistics_2018_2024.csv')
    if os.path.exists(traffic_path):
        df_traf = pd.read_csv(traffic_path)
        audit_results['traffic_statistics'] = analyze_dataframe(
            df=df_traf,
            name="Indian Railways Official National Traffic Statistics (2018-2024)",
            provenance="Ministry of Railways (Railway Board) Year Book & MoSPI Transport Statistics",
            licensing="Government Open Data License - India (GODL)",
            target_col=None,
            date_col=None
        )
        print("Audited National Traffic Statistics.")

    # 5. Inspection Standards
    std_path = os.path.join(DATA_DIR, 'raw', 'standards', 'irpwm_geometry_thresholds.csv')
    if os.path.exists(std_path):
        df_std = pd.read_csv(std_path)
        audit_results['inspection_standards'] = analyze_dataframe(
            df=df_std,
            name="Indian Railways Permanent Way Manual (IRPWM 2020) & RDSO Geometry Standards",
            provenance="Research Designs and Standards Organisation (RDSO) & Railway Board",
            licensing="Official Public Engineering Standard / Technical Manual",
            target_col='maintenance_classification',
            date_col=None
        )
        print("Audited Inspection Standards dataset.")

    # 6. Safety & Accident Reports
    cag_path = os.path.join(DATA_DIR, 'raw', 'accidents', 'cag_derailment_causation_2017_2021.csv')
    if os.path.exists(cag_path):
        df_cag = pd.read_csv(cag_path)
        audit_results['cag_derailments'] = analyze_dataframe(
            df=df_cag,
            name="CAG Report No. 22 of 2022 - Derailments in Indian Railways (2017-2021)",
            provenance="Comptroller and Auditor General of India (Official Audit Report tabled in Parliament)",
            licensing="Public Parliamentary Audit Report",
            target_col='cause_category',
            date_col=None
        )
        print("Audited CAG Derailment findings.")

    # 7. Weather Timeseries Template
    weather_path = os.path.join(DATA_DIR, 'raw', 'weather', 'sample_weather_timeseries.csv')
    if os.path.exists(weather_path):
        df_wtr = pd.read_csv(weather_path)
        audit_results['weather_timeseries'] = analyze_dataframe(
            df=df_wtr,
            name="Weather Station Hourly Timeseries (Sample Import Template)",
            provenance="Simulated reference dataset adhering to IMD standard reporting schemas",
            licensing="Project Internal Reference Template",
            target_col=None,
            date_col='timestamp',
            geo_cols=['latitude', 'longitude']
        )
        print("Audited Weather timeseries dataset.")

    # Save audit report to JSON
    report_json_path = os.path.join(REPORTS_DIR, 'DATA_QUALITY_AUDIT.json')
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2)
    print(f"\nSaved comprehensive data quality audit report to: {report_json_path}")

    # Generate Visualizations
    print("Generating exploratory data quality figures in reports/figures/...")
    
    # Figure 1: INFORMS Target Class & Defect Types Distribution
    if 'informs_geometry' in audit_results:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        df_inf = pd.read_parquet(informs_path)
        
        prty_counts = df_inf['DEF_PRTY'].value_counts()
        axes[0].bar(prty_counts.index, prty_counts.values, color=['#e67e22', '#c0392b'], edgecolor='black')
        axes[0].set_title("INFORMS Defect Severity Tag Distribution (Real Observational Data)", fontsize=11, fontweight='bold')
        axes[0].set_xlabel("Defect Tag (YEL: Yellow / Need Scheduled, RED: Red / Urgent Safety Action)")
        axes[0].set_ylabel("Inspection Count")
        for i, v in enumerate(prty_counts.values):
            axes[0].text(i, v + 200, f"{v:,} ({v/len(df_inf)*100:.1f}%)", ha='center', fontweight='bold')
            
        type_counts = df_inf['DFCT_TYPE'].value_counts()
        axes[1].bar(type_counts.index, type_counts.values, color=['#2980b9', '#27ae60', '#8e44ad'], edgecolor='black')
        axes[1].set_title("INFORMS Defect Types Recorded by Geometry Car", fontsize=11, fontweight='bold')
        axes[1].set_xlabel("Geometry Defect Type")
        axes[1].set_ylabel("Count")
        for i, v in enumerate(type_counts.values):
            axes[1].text(i, v + 200, f"{v:,} ({v/len(df_inf)*100:.1f}%)", ha='center', fontweight='bold')
            
        plt.tight_layout()
        fig1_path = os.path.join(FIGURES_DIR, 'fig1_informs_defect_distributions.png')
        plt.savefig(fig1_path, dpi=200)
        plt.close()
        print(f"Generated Figure 1: {fig1_path}")

    # Figure 2: Hugging Face Synthetic Failure Severity & Leakage Correlation
    if 'huggingface_maintenance_synthetic' in audit_results:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        df_synth = pd.read_parquet(hf_path)
        
        sev_counts = df_synth['failure_severity'].value_counts(dropna=False)
        sev_labels = [str(x) for x in sev_counts.index]
        colors = ['#bdc3c7', '#3498db', '#f39c12', '#e67e22', '#e74c3c']
        axes[0].bar(sev_labels, sev_counts.values, color=colors, edgecolor='black')
        axes[0].set_title("Hugging Face Synthetic failure_severity Distribution", fontsize=11, fontweight='bold')
        axes[0].set_xlabel("Failure Severity Level")
        axes[0].set_ylabel("Record Count")
        for i, v in enumerate(sev_counts.values):
            axes[0].text(i, v + 1000, f"{v:,} ({v/len(df_synth)*100:.1f}%)", ha='center', fontsize=9, fontweight='bold')
            
        # Target leakage correlation heatmap
        leakage_cols = ['risk_score', 'maintenance_required', 'rail_wear_mm', 'track_temperature_c', 'inspection_score', 'delay_minutes']
        valid_cols = [c for c in leakage_cols if c in df_synth.columns]
        corr_matrix = df_synth[valid_cols].corr()
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=axes[1])
        axes[1].set_title("Feature Correlation Matrix (Highlighting Leakage Risk with risk_score)", fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        fig2_path = os.path.join(FIGURES_DIR, 'fig2_synthetic_severity_and_leakage.png')
        plt.savefig(fig2_path, dpi=200)
        plt.close()
        print(f"Generated Figure 2: {fig2_path}")

    # Figure 3: Indian Railways Zonal Station Distribution & CAG Derailment Causation
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    if 'railway_stations' in audit_results:
        df_stn = pd.read_csv(stations_path)
        zone_counts = df_stn['zone'].value_counts().head(12)
        axes[0].barh(zone_counts.index[::-1], zone_counts.values[::-1], color='#16a085', edgecolor='black')
        axes[0].set_title("Operational Railway Stations by Zone (Top 12 Indian Railway Zones)", fontsize=11, fontweight='bold')
        axes[0].set_xlabel("Number of Operational Stations")
        for i, v in enumerate(zone_counts.values[::-1]):
            axes[0].text(v + 10, i, f"{v:,}", va='center', fontweight='bold')
            
    if 'cag_derailments' in audit_results:
        df_cag = pd.read_csv(cag_path)
        cag_grp = df_cag.groupby('cause_category')['incident_count'].sum().sort_values(ascending=True)
        axes[1].barh(cag_grp.index, cag_grp.values, color='#8e44ad', edgecolor='black')
        axes[1].set_title("Causation Breakdown of 1,127 Derailments (CAG Report 22 of 2022)", fontsize=11, fontweight='bold')
        axes[1].set_xlabel("Number of Derailment Incidents (2017–2021)")
        for i, v in enumerate(cag_grp.values):
            axes[1].text(v + 5, i, f"{v} ({v/df_cag['incident_count'].sum()*100:.1f}%)", va='center', fontweight='bold')

    plt.tight_layout()
    fig3_path = os.path.join(FIGURES_DIR, 'fig3_zonal_network_and_derailment_causation.png')
    plt.savefig(fig3_path, dpi=200)
    plt.close()
    print(f"Generated Figure 3: {fig3_path}")
    print("Quality assessment and figure generation completed successfully!")

if __name__ == '__main__':
    main()
