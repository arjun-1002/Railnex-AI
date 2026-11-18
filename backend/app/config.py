"""
Railnex AI Backend Configuration
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'TrackPrior-AI', 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'TrackPrior-AI', 'reports')

API_TITLE = "Railnex AI — Railway Track Defect Severity Classification & Prioritization API"
API_VERSION = "1.0.0"
API_DESCRIPTION = (
    "Intelligent analytical decision-support API for railway track infrastructure monitoring, "
    "defect severity classification, deterioration analysis, and maintenance prioritization."
)
