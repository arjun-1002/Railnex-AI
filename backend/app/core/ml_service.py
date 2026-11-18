"""
Railnex AI — Machine Learning Service
Loads trained XGBoost/Random Forest models, runs calibrated severity predictions,
computes feature contributions, and compares against IRPWM 2020 thresholds.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List

from ..config import MODELS_DIR, DATA_DIR
from ..schemas.models import (
    SeverityPredictionRequest, SeverityPredictionResponse,
    ContributingFactor, StandardsComparison
)

class MLService:
    def __init__(self):
        self.model_path = os.path.join(MODELS_DIR, "real_best_severity_model.joblib")
        self.preprocessor_path = os.path.join(MODELS_DIR, "real_feature_preprocessor.joblib")
        self.eval_path = os.path.join(MODELS_DIR, "experiment_a_evaluation.json")
        self.eval_b_path = os.path.join(MODELS_DIR, "experiment_b_evaluation.json")
        self.standards_path = os.path.join(DATA_DIR, "raw", "standards", "irpwm_geometry_thresholds.csv")

        self.model = None
        self.preprocessor = None
        self.eval_data = None
        self.eval_b_data = None
        self.standards_df = None

        self._load_artifacts()

    def _load_artifacts(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        if os.path.exists(self.preprocessor_path):
            self.preprocessor = joblib.load(self.preprocessor_path)
        if os.path.exists(self.eval_path):
            with open(self.eval_path, 'r', encoding='utf-8') as f:
                self.eval_data = json.load(f)
        if os.path.exists(self.eval_b_path):
            with open(self.eval_b_path, 'r', encoding='utf-8') as f:
                self.eval_b_data = json.load(f)
        if os.path.exists(self.standards_path):
            self.standards_df = pd.read_csv(self.standards_path)

    def predict_severity(self, req: SeverityPredictionRequest) -> SeverityPredictionResponse:
        if self.model is None or self.preprocessor is None:
            raise RuntimeError("Model or preprocessor artifact not loaded.")

        # Compute engineered features
        defect_volume = req.defect_length_ft * abs(req.defect_amplitude_in)
        speed_ratio = req.freight_speed_limit_mph / (req.passenger_speed_limit_mph + 1e-4)

        input_dict = {
            'defect_length_ft': [req.defect_length_ft],
            'defect_amplitude_in': [req.defect_amplitude_in],
            'defect_volume_proxy': [defect_volume],
            'fra_track_class': [req.fra_track_class],
            'freight_speed_limit_mph': [req.freight_speed_limit_mph],
            'passenger_speed_limit_mph': [req.passenger_speed_limit_mph],
            'speed_ratio': [speed_ratio],
            'inspection_month': [req.inspection_month],
            'defect_type': [req.defect_type.upper().strip()],
            'curve_spiral_tangent_code': [req.curve_spiral_tangent_code.upper().strip()],
            'track_code': [str(req.track_code).strip()]
        }
        df_input = pd.DataFrame(input_dict)

        # Preprocess
        X_trans = self.preprocessor.transform(df_input)
        pred_class = int(self.model.predict(X_trans)[0])
        probabilities = self.model.predict_proba(X_trans)[0]

        prob_yellow = round(float(probabilities[0]), 4)
        prob_red = round(float(probabilities[1]), 4)
        confidence = prob_red if pred_class == 1 else prob_yellow

        # Classification label & Urgency
        if pred_class == 1:
            severity_label = "Red Tag — Urgent Action Required (FRA Safety Exceedance / UML)"
            urgency_level = "CRITICAL / URGENT"
            suggested_action = (
                "Issue immediate caution order / speed restriction. Dispatch permanent way gang "
                "for on-site gauge and crosslevel verification. Schedule emergency tamping."
            )
        else:
            severity_label = "Yellow Tag — Near Defect / Scheduled Maintenance (PML / NBML)"
            urgency_level = "PLANNED MAINTENANCE"
            suggested_action = (
                "Log track section in Track Management System (TMS) programmed maintenance roster. "
                "Schedule through-tamping during upcoming track machine maintenance window."
            )

        # Explainable contributing factors
        factors = []
        if abs(req.defect_amplitude_in) > 1.25:
            factors.append(ContributingFactor(
                feature="Defect Amplitude",
                impact="HIGH RISK AMPLITUDE",
                description=f"Recorded amplitude of {req.defect_amplitude_in:.2f} inches exceeds standard allowable track tolerance."
            ))
        else:
            factors.append(ContributingFactor(
                feature="Defect Amplitude",
                impact="MODERATE",
                description=f"Amplitude of {req.defect_amplitude_in:.2f} inches is within pre-defect bounds."
            ))

        if defect_volume > 20.0:
            factors.append(ContributingFactor(
                feature="Defect Spatial Extent (Volume)",
                impact="HIGH EXTENT",
                description=f"Combined length ({req.defect_length_ft:.1f} ft) and depth indicates prolonged continuous track perturbation."
            ))

        if req.fra_track_class >= 4 and req.freight_speed_limit_mph >= 40:
            factors.append(ContributingFactor(
                feature="Operational Speed Exposure",
                impact="ELEVATED DYNAMIC FORCE",
                description=f"High speed operation (Class {req.fra_track_class}, {req.freight_speed_limit_mph} mph freight) increases dynamic wheel unloading risk."
            ))

        if req.defect_type.upper() == "XLEVEL":
            factors.append(ContributingFactor(
                feature="Defect Category: Cross-Level",
                impact="DERAILMENT RISK",
                description="Cross-level discrepancies directly induce vehicle roll and dynamic flange climbing on curves."
            ))

        # Compare with IRPWM 2020 benchmarks
        # 1 inch = 25.4 mm
        amplitude_mm = abs(req.defect_amplitude_in) * 25.4
        standards_comp = []
        standards_comp.append(StandardsComparison(
            parameter=f"{req.defect_type} Amplitude (Converted)",
            recorded_value=f"{amplitude_mm:.1f} mm ({req.defect_amplitude_in:.2f} in)",
            irpwm_standard="IRPWM 2020 Table 5.1 UML: 10.0–15.0 mm",
            status="EXCEEDS URGENT MAINTENANCE LIMIT" if amplitude_mm >= 12.0 else "WITHIN NEED-BASED TOLERANCE"
        ))
        standards_comp.append(StandardsComparison(
            parameter="Operating Class Speed",
            recorded_value=f"{req.passenger_speed_limit_mph} mph (~{req.passenger_speed_limit_mph*1.609:.0f} km/h)",
            irpwm_standard="IRPWM Track Group B (110–130 km/h) / Group C (up to 110 km/h)",
            status="APPLICABLE STANDARD"
        ))

        limitations = (
            "NOTICE: Predictions are generated by machine learning trained on verified real-world "
            "track geometry car records (INFORMS 2015). This software serves as an analytical "
            "decision-support aid for railway engineers and must not replace physical on-site inspection, "
            "standard track measuring trolley audits, or statutory safety rules."
        )

        return SeverityPredictionResponse(
            predicted_class="RED" if pred_class == 1 else "YELLOW",
            severity_label=severity_label,
            urgency_level=urgency_level,
            confidence_score=round(float(confidence), 4),
            probabilities={"Yellow_Tag_Planned": prob_yellow, "Red_Tag_Urgent": prob_red},
            contributing_factors=factors,
            standards_comparison=standards_comp,
            suggested_action=suggested_action,
            limitations_disclaimer=limitations
        )

    def get_model_evaluation(self) -> Dict[str, Any]:
        return {
            "experiment_a_real": self.eval_data,
            "experiment_b_synthetic": self.eval_b_data
        }

    def get_standards(self) -> List[Dict[str, Any]]:
        if self.standards_df is not None:
            return self.standards_df.to_dict(orient="records")
        return []
