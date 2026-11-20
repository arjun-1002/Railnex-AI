"""
RailRakshak AI — Historical Weather Ingestion Script
Fetches 5 Fiscal Years (2020-2025) of Real Daily Weather Telemetry
from Open-Meteo Archive API across 8 Critical Indian Railways Zonal Hubs.
"""

import os
import json
import time
import urllib.request
import pandas as pd
import numpy as np

# Output directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "weather")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 8 Strategic Indian Railway Junctions across zones
ZONAL_HUBS = [
    {"station_code": "NDLS", "name": "New Delhi", "zone": "NR", "lat": 28.6139, "lon": 77.2090},
    {"station_code": "CNB", "name": "Kanpur Central", "zone": "NCR", "lat": 26.4499, "lon": 80.3319},
    {"station_code": "PRYJ", "name": "Prayagraj Jn", "zone": "NCR", "lat": 25.4358, "lon": 81.8463},
    {"station_code": "CSMT", "name": "Mumbai CSMT", "zone": "CR", "lat": 18.9401, "lon": 72.8355},
    {"station_code": "HWH", "name": "Howrah Jn", "zone": "ER", "lat": 22.5839, "lon": 88.3426},
    {"station_code": "MAS", "name": "Chennai Central", "zone": "SR", "lat": 13.0827, "lon": 80.2707},
    {"station_code": "NGP", "name": "Nagpur Jn", "zone": "CR", "lat": 21.1458, "lon": 79.0882},
    {"station_code": "GHY", "name": "Guwahati Jn", "zone": "NFR", "lat": 26.1856, "lon": 91.7483},
]

def fetch_weather_for_hub(hub, start_date="2020-01-01", end_date="2024-12-31"):
    print(f"Fetching weather for {hub['name']} ({hub['zone']})...")
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={hub['lat']}&longitude={hub['lon']}&"
        f"start_date={start_date}&end_date={end_date}&"
        f"daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
        f"precipitation_sum,rain_sum,wind_speed_10m_max&"
        f"timezone=Asia%2FKolkata"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "RailRakshak-AI/1.0 (Academic/BTech)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    
    daily = data["daily"]
    df = pd.DataFrame({
        "date": daily["time"],
        "station_code": hub["station_code"],
        "station_name": hub["name"],
        "zone": hub["zone"],
        "latitude": hub["lat"],
        "longitude": hub["lon"],
        "temp_max_c": daily["temperature_2m_max"],
        "temp_min_c": daily["temperature_2m_min"],
        "temp_mean_c": daily["temperature_2m_mean"],
        "precipitation_mm": daily["precipitation_sum"],
        "rain_mm": daily["rain_sum"],
        "wind_speed_kmh": daily["wind_speed_10m_max"],
    })
    
    # Calculate engineering proxies
    # Rail temp is estimated using RDSO guidelines: in high sun, rail temp is 15-20 C higher than ambient max
    # On overcast/rainy days, solar boost is negligible (1-3 C)
    solar_boost = np.where(df["precipitation_mm"] > 5.0, 2.0, 18.0)
    df["est_rail_temp_max_c"] = np.round(df["temp_max_c"] + solar_boost, 1)
    
    # Buckling risk flag: Rail temp > 60 C (RDSO IRPWM criteria for 52kg/60kg LWR destressing temp ~38C + 20C)
    df["buckling_risk_flag"] = (df["est_rail_temp_max_c"] >= 60.0).astype(int)
    
    # Flood / Heavy rain flag: Daily rain > 64.5 mm (IMD Heavy Rainfall criterion)
    df["heavy_rainfall_flag"] = (df["precipitation_mm"] >= 64.5).astype(int)
    
    # Heatwave flag: Ambient temp_max >= 40 C
    df["heatwave_flag"] = (df["temp_max_c"] >= 40.0).astype(int)
    
    return df

def main():
    all_dfs = []
    for hub in ZONAL_HUBS:
        try:
            df_hub = fetch_weather_for_hub(hub)
            all_dfs.append(df_hub)
            time.sleep(0.5) # Gentle rate limit
        except Exception as e:
            print(f"Error fetching for {hub['name']}: {e}")
            
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        csv_path = os.path.join(OUTPUT_DIR, "indian_railways_historical_weather_2020_2024.csv")
        parquet_path = os.path.join(OUTPUT_DIR, "indian_railways_historical_weather_2020_2024.parquet")
        
        combined_df.to_csv(csv_path, index=False)
        try:
            combined_df.to_parquet(parquet_path, index=False)
        except Exception:
            pass # graceful fallback
            
        print(f"\n[SUCCESS] Successfully acquired {len(combined_df):,} weather records across {len(ZONAL_HUBS)} railway hubs!")
        print(f"Saved to: {csv_path}")

if __name__ == "__main__":
    main()
