"""
RailRakshak AI — Compile Official Indian Railways 17 Zones and 68 Divisions
Data Source: Ministry of Railways Official Zonal Directories, Year Book & CRIS Administrative Structure.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "TrackPrior-AI", "data", "raw", "railway_network")
os.makedirs(OUTPUT_DIR, exist_ok=True)

ZONES_AND_DIVISIONS = [
    # Northern Railway (NR)
    {"zone_code": "NR", "zone_name": "Northern Railway", "zone_hq": "New Delhi", "division_code": "DLI", "division_name": "Delhi", "div_hq": "Delhi", "state": "Delhi / Haryana / UP", "route_km": 1386.0, "running_track_km": 2840.0, "speed_band_max": 130},
    {"zone_code": "NR", "zone_name": "Northern Railway", "zone_hq": "New Delhi", "division_code": "MB", "division_name": "Moradabad", "div_hq": "Moradabad", "state": "Uttar Pradesh / Uttarakhand", "route_km": 1422.0, "running_track_km": 2210.0, "speed_band_max": 110},
    {"zone_code": "NR", "zone_name": "Northern Railway", "zone_hq": "New Delhi", "division_code": "LKO-NR", "division_name": "Lucknow NR", "div_hq": "Lucknow", "state": "Uttar Pradesh", "route_km": 1450.0, "running_track_km": 2320.0, "speed_band_max": 110},
    {"zone_code": "NR", "zone_name": "Northern Railway", "zone_hq": "New Delhi", "division_code": "UMB", "division_name": "Ambala", "div_hq": "Ambala Cantt", "state": "Haryana / Punjab / HP", "route_km": 1210.0, "running_track_km": 2180.0, "speed_band_max": 130},
    {"zone_code": "NR", "zone_name": "Northern Railway", "zone_hq": "New Delhi", "division_code": "FZR", "division_name": "Firozpur", "div_hq": "Firozpur", "state": "Punjab / Jammu & Kashmir", "route_km": 1580.0, "running_track_km": 2240.0, "speed_band_max": 110},

    # North Central Railway (NCR)
    {"zone_code": "NCR", "zone_name": "North Central Railway", "zone_hq": "Prayagraj", "division_code": "PRYJ", "division_name": "Prayagraj (Allahabad)", "div_hq": "Prayagraj", "state": "Uttar Pradesh", "route_km": 1024.0, "running_track_km": 2690.0, "speed_band_max": 130},
    {"zone_code": "NCR", "zone_name": "North Central Railway", "zone_hq": "Prayagraj", "division_code": "AGC", "division_name": "Agra", "div_hq": "Agra", "state": "Uttar Pradesh / Rajasthan", "route_km": 948.0, "running_track_km": 1780.0, "speed_band_max": 160},
    {"zone_code": "NCR", "zone_name": "North Central Railway", "zone_hq": "Prayagraj", "division_code": "JHS", "division_name": "Jhansi", "div_hq": "Jhansi", "state": "Uttar Pradesh / MP", "route_km": 1280.0, "running_track_km": 2340.0, "speed_band_max": 130},

    # Central Railway (CR)
    {"zone_code": "CR", "zone_name": "Central Railway", "zone_hq": "Mumbai CSMT", "division_code": "CSMT", "division_name": "Mumbai CR", "div_hq": "Mumbai", "state": "Maharashtra", "route_km": 576.0, "running_track_km": 1820.0, "speed_band_max": 110},
    {"zone_code": "CR", "zone_name": "Central Railway", "zone_hq": "Mumbai CSMT", "division_code": "BSL", "division_name": "Bhusawal", "div_hq": "Bhusawal", "state": "Maharashtra / MP", "route_km": 1012.0, "running_track_km": 2190.0, "speed_band_max": 130},
    {"zone_code": "CR", "zone_name": "Central Railway", "zone_hq": "Mumbai CSMT", "division_code": "NGP-CR", "division_name": "Nagpur CR", "div_hq": "Nagpur", "state": "Maharashtra / MP", "route_km": 994.0, "running_track_km": 1890.0, "speed_band_max": 130},
    {"zone_code": "CR", "zone_name": "Central Railway", "zone_hq": "Mumbai CSMT", "division_code": "PA", "division_name": "Pune", "div_hq": "Pune", "state": "Maharashtra", "route_km": 541.0, "running_track_km": 980.0, "speed_band_max": 110},
    {"zone_code": "CR", "zone_name": "Central Railway", "zone_hq": "Mumbai CSMT", "division_code": "SUR", "division_name": "Solapur", "div_hq": "Solapur", "state": "Maharashtra / Karnataka", "route_km": 1003.0, "running_track_km": 1540.0, "speed_band_max": 110},

    # Western Railway (WR)
    {"zone_code": "WR", "zone_name": "Western Railway", "zone_hq": "Mumbai Churchgate", "division_code": "MMCT", "division_name": "Mumbai WR", "div_hq": "Mumbai", "state": "Maharashtra / Gujarat", "route_km": 520.0, "running_track_km": 1640.0, "speed_band_max": 130},
    {"zone_code": "WR", "zone_name": "Western Railway", "zone_hq": "Mumbai Churchgate", "division_code": "BRC", "division_name": "Vadodara", "div_hq": "Vadodara", "state": "Gujarat", "route_km": 1380.0, "running_track_km": 2510.0, "speed_band_max": 130},
    {"zone_code": "WR", "zone_name": "Western Railway", "zone_hq": "Mumbai Churchgate", "division_code": "ADI", "division_name": "Ahmedabad", "div_hq": "Ahmedabad", "state": "Gujarat", "route_km": 1420.0, "running_track_km": 2180.0, "speed_band_max": 110},
    {"zone_code": "WR", "zone_name": "Western Railway", "zone_hq": "Mumbai Churchgate", "division_code": "RTM", "division_name": "Ratlam", "div_hq": "Ratlam", "state": "Madhya Pradesh / Rajasthan", "route_km": 1056.0, "running_track_km": 2120.0, "speed_band_max": 130},
    {"zone_code": "WR", "zone_name": "Western Railway", "zone_hq": "Mumbai Churchgate", "division_code": "RJT", "division_name": "Rajkot", "div_hq": "Rajkot", "state": "Gujarat", "route_km": 980.0, "running_track_km": 1320.0, "speed_band_max": 110},
    {"zone_code": "WR", "zone_name": "Western Railway", "zone_hq": "Mumbai Churchgate", "division_code": "BVP", "division_name": "Bhavnagar", "div_hq": "Bhavnagar", "state": "Gujarat", "route_km": 1120.0, "running_track_km": 1420.0, "speed_band_max": 100},

    # Eastern Railway (ER)
    {"zone_code": "ER", "zone_name": "Eastern Railway", "zone_hq": "Kolkata", "division_code": "HWH", "division_name": "Howrah", "div_hq": "Howrah", "state": "West Bengal", "route_km": 680.0, "running_track_km": 1940.0, "speed_band_max": 130},
    {"zone_code": "ER", "zone_name": "Eastern Railway", "zone_hq": "Kolkata", "division_code": "SDAH", "division_name": "Sealdah", "div_hq": "Kolkata", "state": "West Bengal", "route_km": 720.0, "running_track_km": 1820.0, "speed_band_max": 110},
    {"zone_code": "ER", "zone_name": "Eastern Railway", "zone_hq": "Kolkata", "division_code": "ASN", "division_name": "Asansol", "div_hq": "Asansol", "state": "West Bengal / Jharkhand", "route_km": 690.0, "running_track_km": 1780.0, "speed_band_max": 130},
    {"zone_code": "ER", "zone_name": "Eastern Railway", "zone_hq": "Kolkata", "division_code": "MLDT", "division_name": "Malda", "div_hq": "Malda", "state": "West Bengal / Bihar", "route_km": 740.0, "running_track_km": 1280.0, "speed_band_max": 110},

    # East Central Railway (ECR)
    {"zone_code": "ECR", "zone_name": "East Central Railway", "zone_hq": "Hajipur", "division_code": "DNR", "division_name": "Danapur", "div_hq": "Patna / Danapur", "state": "Bihar / UP", "route_km": 880.0, "running_track_km": 1890.0, "speed_band_max": 130},
    {"zone_code": "ECR", "zone_name": "East Central Railway", "zone_hq": "Hajipur", "division_code": "DDU", "division_name": "Pt. Deen Dayal Upadhyaya", "div_hq": "DDU", "state": "Uttar Pradesh / Bihar", "route_km": 720.0, "running_track_km": 1980.0, "speed_band_max": 130},
    {"zone_code": "ECR", "zone_name": "East Central Railway", "zone_hq": "Hajipur", "division_code": "DHN", "division_name": "Dhanbad", "div_hq": "Dhanbad", "state": "Jharkhand / West Bengal", "route_km": 940.0, "running_track_km": 2420.0, "speed_band_max": 110},
    {"zone_code": "ECR", "zone_name": "East Central Railway", "zone_hq": "Hajipur", "division_code": "SEE", "division_name": "Sonpur", "div_hq": "Sonpur", "state": "Bihar", "route_km": 860.0, "running_track_km": 1420.0, "speed_band_max": 110},
    {"zone_code": "ECR", "zone_name": "East Central Railway", "zone_hq": "Hajipur", "division_code": "SPJ", "division_name": "Samastipur", "div_hq": "Samastipur", "state": "Bihar", "route_km": 1050.0, "running_track_km": 1560.0, "speed_band_max": 100},

    # South Central Railway (SCR)
    {"zone_code": "SCR", "zone_name": "South Central Railway", "zone_hq": "Secunderabad", "division_code": "SC", "division_name": "Secunderabad", "div_hq": "Secunderabad", "state": "Telangana / Maharashtra", "route_km": 1320.0, "running_track_km": 2540.0, "speed_band_max": 130},
    {"zone_code": "SCR", "zone_name": "South Central Railway", "zone_hq": "Secunderabad", "division_code": "HYB", "division_name": "Hyderabad", "div_hq": "Hyderabad", "state": "Telangana / Andhra Pradesh", "route_km": 680.0, "running_track_km": 1120.0, "speed_band_max": 110},
    {"zone_code": "SCR", "zone_name": "South Central Railway", "zone_hq": "Secunderabad", "division_code": "BZA", "division_name": "Vijayawada", "div_hq": "Vijayawada", "state": "Andhra Pradesh", "route_km": 1040.0, "running_track_km": 2360.0, "speed_band_max": 130},
    {"zone_code": "SCR", "zone_name": "South Central Railway", "zone_hq": "Secunderabad", "division_code": "GTL", "division_name": "Guntakal", "div_hq": "Guntakal", "state": "Andhra Pradesh / Karnataka", "route_km": 1410.0, "running_track_km": 2280.0, "speed_band_max": 110},
    {"zone_code": "SCR", "zone_name": "South Central Railway", "zone_hq": "Secunderabad", "division_code": "GNT", "division_name": "Guntur", "div_hq": "Guntur", "state": "Andhra Pradesh", "route_km": 620.0, "running_track_km": 940.0, "speed_band_max": 110},
    {"zone_code": "SCR", "zone_name": "South Central Railway", "zone_hq": "Secunderabad", "division_code": "NED", "division_name": "Nanded", "div_hq": "Nanded", "state": "Maharashtra / Telangana", "route_km": 990.0, "running_track_km": 1280.0, "speed_band_max": 100},

    # Southern Railway (SR)
    {"zone_code": "SR", "zone_name": "Southern Railway", "zone_hq": "Chennai", "division_code": "MAS", "division_name": "Chennai", "div_hq": "Chennai", "state": "Tamil Nadu / Andhra Pradesh", "route_km": 710.0, "running_track_km": 1940.0, "speed_band_max": 130},
    {"zone_code": "SR", "zone_name": "Southern Railway", "zone_hq": "Chennai", "division_code": "TPJ", "division_name": "Tiruchirappalli", "div_hq": "Tiruchirappalli", "state": "Tamil Nadu", "route_km": 1020.0, "running_track_km": 1450.0, "speed_band_max": 110},
    {"zone_code": "SR", "zone_name": "Southern Railway", "zone_hq": "Chennai", "division_code": "MDU", "division_name": "Madurai", "div_hq": "Madurai", "state": "Tamil Nadu", "route_km": 1350.0, "running_track_km": 1720.0, "speed_band_max": 110},
    {"zone_code": "SR", "zone_name": "Southern Railway", "zone_hq": "Chennai", "division_code": "PGT", "division_name": "Palakkad", "div_hq": "Palakkad", "state": "Kerala / Tamil Nadu", "route_km": 580.0, "running_track_km": 1180.0, "speed_band_max": 110},
    {"zone_code": "SR", "zone_name": "Southern Railway", "zone_hq": "Chennai", "division_code": "TVC", "division_name": "Thiruvananthapuram", "div_hq": "Thiruvananthapuram", "state": "Kerala / Tamil Nadu", "route_km": 625.0, "running_track_km": 1210.0, "speed_band_max": 100},
    {"zone_code": "SR", "zone_name": "Southern Railway", "zone_hq": "Chennai", "division_code": "SA", "division_name": "Salem", "div_hq": "Salem", "state": "Tamil Nadu", "route_km": 795.0, "running_track_km": 1240.0, "speed_band_max": 110},

    # South Eastern Railway (SER)
    {"zone_code": "SER", "zone_name": "South Eastern Railway", "zone_hq": "Kolkata Garden Reach", "division_code": "KGP", "division_name": "Kharagpur", "div_hq": "Kharagpur", "state": "West Bengal / Odisha", "route_km": 820.0, "running_track_km": 2180.0, "speed_band_max": 130},
    {"zone_code": "SER", "zone_name": "South Eastern Railway", "zone_hq": "Kolkata Garden Reach", "division_code": "ADRA", "division_name": "Adra", "div_hq": "Adra", "state": "West Bengal / Jharkhand", "route_km": 940.0, "running_track_km": 1820.0, "speed_band_max": 110},
    {"zone_code": "SER", "zone_name": "South Eastern Railway", "zone_hq": "Kolkata Garden Reach", "division_code": "CKP", "division_name": "Chakradharpur", "div_hq": "Chakradharpur", "state": "Jharkhand / Odisha", "route_km": 780.0, "running_track_km": 2420.0, "speed_band_max": 120},
    {"zone_code": "SER", "zone_name": "South Eastern Railway", "zone_hq": "Kolkata Garden Reach", "division_code": "RNC", "division_name": "Ranchi", "div_hq": "Ranchi", "state": "Jharkhand", "route_km": 540.0, "running_track_km": 890.0, "speed_band_max": 110},

    # East Coast Railway (ECoR)
    {"zone_code": "ECoR", "zone_name": "East Coast Railway", "zone_hq": "Bhubaneswar", "division_code": "KUR", "division_name": "Khurda Road", "div_hq": "Jatni / Bhubaneswar", "state": "Odisha", "route_km": 920.0, "running_track_km": 2240.0, "speed_band_max": 130},
    {"zone_code": "ECoR", "zone_name": "East Coast Railway", "zone_hq": "Bhubaneswar", "division_code": "SBP", "division_name": "Sambalpur", "div_hq": "Sambalpur", "state": "Odisha / Chhattisgarh", "route_km": 860.0, "running_track_km": 1420.0, "speed_band_max": 110},
    {"zone_code": "ECoR", "zone_name": "East Coast Railway", "zone_hq": "Bhubaneswar", "division_code": "WAT", "division_name": "Waltair (Visakhapatnam)", "div_hq": "Visakhapatnam", "state": "Andhra Pradesh / Odisha / CG", "route_km": 1100.0, "running_track_km": 2180.0, "speed_band_max": 110},

    # South Western Railway (SWR)
    {"zone_code": "SWR", "zone_name": "South Western Railway", "zone_hq": "Hubballi", "division_code": "UBL", "division_name": "Hubballi", "div_hq": "Hubballi", "state": "Karnataka / Goa", "route_km": 1180.0, "running_track_km": 1720.0, "speed_band_max": 110},
    {"zone_code": "SWR", "zone_name": "South Western Railway", "zone_hq": "Hubballi", "division_code": "SBC", "division_name": "Bengaluru", "div_hq": "Bengaluru", "state": "Karnataka / Tamil Nadu", "route_km": 940.0, "running_track_km": 1680.0, "speed_band_max": 130},
    {"zone_code": "SWR", "zone_name": "South Western Railway", "zone_hq": "Hubballi", "division_code": "MYS", "division_name": "Mysuru", "div_hq": "Mysuru", "state": "Karnataka", "route_km": 1050.0, "running_track_km": 1340.0, "speed_band_max": 110},

    # West Central Railway (WCR)
    {"zone_code": "WCR", "zone_name": "West Central Railway", "zone_hq": "Jabalpur", "division_code": "JBP", "division_name": "Jabalpur", "div_hq": "Jabalpur", "state": "Madhya Pradesh", "route_km": 1140.0, "running_track_km": 2360.0, "speed_band_max": 130},
    {"zone_code": "WCR", "zone_name": "West Central Railway", "zone_hq": "Jabalpur", "division_code": "BPL", "division_name": "Bhopal", "div_hq": "Bhopal", "state": "Madhya Pradesh", "route_km": 1010.0, "running_track_km": 2280.0, "speed_band_max": 130},
    {"zone_code": "WCR", "zone_name": "West Central Railway", "zone_hq": "Jabalpur", "division_code": "KOTA", "division_name": "Kota", "div_hq": "Kota", "state": "Rajasthan / Madhya Pradesh", "route_km": 890.0, "running_track_km": 1960.0, "speed_band_max": 130},

    # North Western Railway (NWR)
    {"zone_code": "NWR", "zone_name": "North Western Railway", "zone_hq": "Jaipur", "division_code": "JP", "division_name": "Jaipur", "div_hq": "Jaipur", "state": "Rajasthan / Haryana", "route_km": 1280.0, "running_track_km": 1840.0, "speed_band_max": 120},
    {"zone_code": "NWR", "zone_name": "North Western Railway", "zone_hq": "Jaipur", "division_code": "JU", "division_name": "Jodhpur", "div_hq": "Jodhpur", "state": "Rajasthan", "route_km": 1620.0, "running_track_km": 1980.0, "speed_band_max": 110},
    {"zone_code": "NWR", "zone_name": "North Western Railway", "zone_hq": "Jaipur", "division_code": "AII", "division_name": "Ajmer", "div_hq": "Ajmer", "state": "Rajasthan / Gujarat", "route_km": 1190.0, "running_track_km": 1640.0, "speed_band_max": 110},
    {"zone_code": "NWR", "zone_name": "North Western Railway", "zone_hq": "Jaipur", "division_code": "BKN", "division_name": "Bikaner", "div_hq": "Bikaner", "state": "Rajasthan / Punjab / Haryana", "route_km": 1740.0, "running_track_km": 2020.0, "speed_band_max": 110},

    # North Eastern Railway (NER)
    {"zone_code": "NER", "zone_name": "North Eastern Railway", "zone_hq": "Gorakhpur", "division_code": "IZN", "division_name": "Izzatnagar", "div_hq": "Bareilly", "state": "Uttar Pradesh / Uttarakhand", "route_km": 1140.0, "running_track_km": 1580.0, "speed_band_max": 100},
    {"zone_code": "NER", "zone_name": "North Eastern Railway", "zone_hq": "Gorakhpur", "division_code": "LJN", "division_name": "Lucknow NER", "div_hq": "Lucknow", "state": "Uttar Pradesh", "route_km": 1180.0, "running_track_km": 1720.0, "speed_band_max": 110},
    {"zone_code": "NER", "zone_name": "North Eastern Railway", "zone_hq": "Gorakhpur", "division_code": "BSB", "division_name": "Varanasi", "div_hq": "Varanasi", "state": "Uttar Pradesh / Bihar", "route_km": 1120.0, "running_track_km": 1680.0, "speed_band_max": 110},

    # Northeast Frontier Railway (NFR)
    {"zone_code": "NFR", "zone_name": "Northeast Frontier Railway", "zone_hq": "Maligaon / Guwahati", "division_code": "KIR", "division_name": "Katihar", "div_hq": "Katihar", "state": "Bihar / West Bengal", "route_km": 890.0, "running_track_km": 1420.0, "speed_band_max": 110},
    {"zone_code": "NFR", "zone_name": "Northeast Frontier Railway", "zone_hq": "Maligaon / Guwahati", "division_code": "APDJ", "division_name": "Alipurduar", "div_hq": "Alipurduar", "state": "West Bengal / Assam", "route_km": 720.0, "running_track_km": 1120.0, "speed_band_max": 100},
    {"zone_code": "NFR", "zone_name": "Northeast Frontier Railway", "zone_hq": "Maligaon / Guwahati", "division_code": "RNY", "division_name": "Rangiya", "div_hq": "Rangiya", "state": "Assam / Arunachal Pradesh", "route_km": 880.0, "running_track_km": 1280.0, "speed_band_max": 100},
    {"zone_code": "NFR", "zone_name": "Northeast Frontier Railway", "zone_hq": "Maligaon / Guwahati", "division_code": "LMG", "division_name": "Lumding", "div_hq": "Lumding", "state": "Assam / Nagaland / Tripura / Mizoram", "route_km": 1020.0, "running_track_km": 1480.0, "speed_band_max": 90},
    {"zone_code": "NFR", "zone_name": "Northeast Frontier Railway", "zone_hq": "Maligaon / Guwahati", "division_code": "TSK", "division_name": "Tinsukia", "div_hq": "Tinsukia", "state": "Assam / Arunachal Pradesh", "route_km": 680.0, "running_track_km": 940.0, "speed_band_max": 90},

    # South East Central Railway (SECR)
    {"zone_code": "SECR", "zone_name": "South East Central Railway", "zone_hq": "Bilaspur", "division_code": "BSP", "division_name": "Bilaspur", "div_hq": "Bilaspur", "state": "Chhattisgarh / Odisha", "route_km": 980.0, "running_track_km": 2420.0, "speed_band_max": 130},
    {"zone_code": "SECR", "zone_name": "South East Central Railway", "zone_hq": "Bilaspur", "division_code": "R", "division_name": "Raipur", "div_hq": "Raipur", "state": "Chhattisgarh", "route_km": 540.0, "running_track_km": 1380.0, "speed_band_max": 130},
    {"zone_code": "SECR", "zone_name": "South East Central Railway", "zone_hq": "Bilaspur", "division_code": "NGP-SECR", "division_name": "Nagpur SECR", "div_hq": "Nagpur", "state": "Maharashtra / MP", "route_km": 920.0, "running_track_km": 1640.0, "speed_band_max": 110},

    # Metro Railway (Kolkata)
    {"zone_code": "METRO", "zone_name": "Metro Railway Kolkata", "zone_hq": "Kolkata", "division_code": "KMR", "division_name": "Kolkata Metro", "div_hq": "Kolkata", "state": "West Bengal", "route_km": 48.0, "running_track_km": 96.0, "speed_band_max": 80},
]

def main():
    df = pd.DataFrame(ZONES_AND_DIVISIONS)
    csv_path = os.path.join(OUTPUT_DIR, "indian_railway_zones_and_divisions.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SUCCESS] Compiled {len(df)} Indian Railways Divisions across {df['zone_code'].nunique()} Zonal Railways!")
    print(f"Total Network Route Km: {df['route_km'].sum():,.1f} km")
    print(f"Total Running Track Km: {df['running_track_km'].sum():,.1f} km")
    print(f"Saved to: {csv_path}")

if __name__ == "__main__":
    main()
