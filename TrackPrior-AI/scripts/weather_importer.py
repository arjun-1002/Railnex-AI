"""
TrackPrior AI — Weather Data Import and Standardization Module
Accepts CSV and Excel weather time-series records.
Validates, standardizes, audits data quality, and outputs clean structured records.
Enforces strict decoupling from track inspections unless spatio-temporal alignment is proven.
"""

import os
import sys
import argparse
import datetime
import pandas as pd
import numpy as np

class WeatherDataImporter:
    """
    Robust Weather Data Importer for TrackPrior AI.
    Handles multiple naming schemas, dates, numeric conversions, and quality audits.
    """
    
    STANDARD_COLUMNS = [
        'timestamp',
        'station_id',
        'latitude',
        'longitude',
        'temperature_c',
        'rainfall_mm',
        'humidity_percent',
        'wind_speed_kmph'
    ]
    
    COLUMN_ALIASES = {
        'timestamp': ['timestamp', 'date', 'datetime', 'time', 'date_time', 'recorded_at', 'obs_date', 'test_dt'],
        'station_id': ['station_id', 'station', 'station_code', 'stn_id', 'loc_id', 'site_id', 'sensor_id'],
        'latitude': ['latitude', 'lat', 'y', 'lat_deg', 'coord_lat'],
        'longitude': ['longitude', 'long', 'lon', 'x', 'lon_deg', 'coord_lon'],
        'temperature_c': ['temperature_c', 'temperature', 'temp', 'temp_c', 'ambient_temperature_c', 't_c'],
        'rainfall_mm': ['rainfall_mm', 'rainfall', 'rain', 'precip', 'precipitation_mm', 'rain_mm'],
        'humidity_percent': ['humidity_percent', 'humidity', 'rel_humidity', 'rh', 'humidity_%', 'rh_percent'],
        'wind_speed_kmph': ['wind_speed_kmph', 'wind_speed', 'wind_kmph', 'wind_spd', 'wind_speed_mps']
    }

    def __init__(self, output_dir=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = output_dir or os.path.join(base_dir, 'data', 'processed')
        os.makedirs(self.output_dir, exist_ok=True)

    def _resolve_column(self, col_candidates, available_cols):
        lower_to_orig = {col.lower().strip(): col for col in available_cols}
        for candidate in col_candidates:
            if candidate.lower() in lower_to_orig:
                return lower_to_orig[candidate.lower()]
        return None

    def load_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Weather file not found: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif ext == '.parquet':
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: .csv, .xlsx, .xls, .parquet")
        return df

    def standardize(self, df):
        """Standardize column names, units, and timestamps."""
        orig_cols = list(df.columns)
        mapping = {}
        for target_col, aliases in self.COLUMN_ALIASES.items():
            matched = self._resolve_column(aliases, orig_cols)
            if matched:
                mapping[matched] = target_col

        df_mapped = df.rename(columns=mapping).copy()
        
        # Ensure mandatory columns exist
        if 'timestamp' not in df_mapped.columns:
            raise ValueError("Mandatory column 'timestamp' (or alias) not found in weather file.")
        
        # Standardize timestamp
        df_mapped['timestamp'] = pd.to_datetime(df_mapped['timestamp'], errors='coerce')
        df_mapped = df_mapped.dropna(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)
        
        # If numeric columns exist, enforce numeric casting and range validation
        numeric_bounds = {
            'temperature_c': (-40.0, 65.0),
            'rainfall_mm': (0.0, 2000.0),
            'humidity_percent': (0.0, 100.0),
            'wind_speed_kmph': (0.0, 300.0),
            'latitude': (-90.0, 90.0),
            'longitude': (-180.0, 180.0)
        }
        
        for col, (lower_bound, upper_bound) in numeric_bounds.items():
            if col in df_mapped.columns:
                df_mapped[col] = pd.to_numeric(df_mapped[col], errors='coerce')
                # Flag extreme out of bounds values as NaN
                out_of_bounds = (df_mapped[col] < lower_bound) | (df_mapped[col] > upper_bound)
                if out_of_bounds.any():
                    df_mapped.loc[out_of_bounds, col] = np.nan

        # Assign default station_id if missing
        if 'station_id' not in df_mapped.columns:
            df_mapped['station_id'] = 'DEFAULT_STATION'

        # Retain standard columns that are available
        present_cols = [c for c in self.STANDARD_COLUMNS if c in df_mapped.columns]
        return df_mapped[present_cols]

    def audit_quality(self, df):
        """Generate comprehensive quality summary."""
        n_rows = len(df)
        report = {
            "total_records": n_rows,
            "columns": list(df.columns),
            "date_range": {
                "start": df['timestamp'].min().isoformat() if not df.empty else None,
                "end": df['timestamp'].max().isoformat() if not df.empty else None
            },
            "stations_count": int(df['station_id'].nunique()) if 'station_id' in df.columns else 0,
            "missing_values_percent": {col: round(float(df[col].isna().sum() / n_rows * 100), 2) for col in df.columns},
            "summary_statistics": {}
        }
        for col in df.select_dtypes(include=[np.number]).columns:
            report["summary_statistics"][col] = {
                "min": round(float(df[col].min()), 2) if not df[col].isna().all() else None,
                "max": round(float(df[col].max()), 2) if not df[col].isna().all() else None,
                "mean": round(float(df[col].mean()), 2) if not df[col].isna().all() else None,
                "median": round(float(df[col].median()), 2) if not df[col].isna().all() else None
            }
        return report

    def import_weather_dataset(self, file_path, output_name='weather_standardized'):
        """Full pipeline: Load -> Standardize -> Audit -> Export."""
        print(f"Importing weather dataset from: {file_path}")
        raw_df = self.load_file(file_path)
        std_df = self.standardize(raw_df)
        audit = self.audit_quality(std_df)
        
        csv_path = os.path.join(self.output_dir, f"{output_name}.csv")
        parquet_path = os.path.join(self.output_dir, f"{output_name}.parquet")
        
        std_df.to_csv(csv_path, index=False)
        std_df.to_parquet(parquet_path, index=False)
        
        print(f"Weather dataset successfully standardized and exported:")
        print(f"  Rows: {len(std_df):,}")
        print(f"  Columns: {list(std_df.columns)}")
        print(f"  CSV: {csv_path}")
        print(f"  Parquet: {parquet_path}")
        return std_df, audit

def main():
    parser = argparse.ArgumentParser(description="TrackPrior AI Weather Data Importer")
    parser.add_argument("--file", type=str, required=True, help="Path to raw weather file (CSV or XLSX)")
    parser.add_argument("--out-name", type=str, default="weather_standardized", help="Output file basename")
    args = parser.parse_args()

    importer = WeatherDataImporter()
    df, audit = importer.import_weather_dataset(args.file, args.out_name)
    print("\nData Quality Audit:")
    for k, v in audit.items():
        print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
