"""
RailRakshak AI — Backend Configuration & App Metadata
B.Tech CSE (AI & ML) Supervised Learning (INT395) Topic 20
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'TrackPrior-AI', 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'docs')

API_TITLE = "RailRakshak AI — Intelligent Railway Track Defect Classification & Predictive Maintenance System"
API_VERSION = "2.0.0"
API_DESCRIPTION = (
    "Comprehensive decision-support API for Indian Railways permanent way monitoring, "
    "multiclass defect severity classification (INT395 Topic 20), TreeSHAP feature attributions, "
    "USFD ultrasonic flaw detection, 5-year weather intelligence, and computer vision defect recognition."
)
