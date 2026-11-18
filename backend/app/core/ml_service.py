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
    ContributingFactor, StandardsComparison, ShapAttribution
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

        # Compute exact TreeSHAP feature contributions
        shap_list: List[ShapAttribution] = []
        try:
            import xgboost as xgb
            feature_names = self.preprocessor.get_feature_names_out()
            dmat = xgb.DMatrix(X_trans, feature_names=list(feature_names))
            contribs = self.model.get_booster().predict(dmat, pred_contribs=True)[0]
            
            feature_label_map = {
                'num__defect_amplitude_in': 'Defect Amplitude (Peak Deviation)',
                'num__defect_volume_proxy': 'Defect Volume Proxy (Length × Amplitude)',
                'num__defect_length_ft': 'Defect Length Extent',
                'num__fra_track_class': 'FRA Track Class Tolerance Limit',
                'num__freight_speed_limit_mph': 'Freight Operational Speed',
                'num__passenger_speed_limit_mph': 'Passenger Operational Speed',
                'num__speed_ratio': 'Speed Differential Ratio',
                'num__inspection_month': 'Seasonal Weather / Inspection Cycle',
                'cat__defect_type_CROSSLEVEL': 'Cross-Level Geometry Perturbation',
                'cat__defect_type_XLEVEL': 'Cross-Level Geometry Perturbation',
                'cat__defect_type_SURFACE': 'Longitudinal Profile / Rail Surface',
                'cat__defect_type_DIP': 'Track Joint / Foundation Dip',
                'cat__curve_spiral_tangent_code_CURVED': 'Curved Track Alignment',
                'cat__curve_spiral_tangent_code_C': 'Curved Track Alignment',
                'cat__curve_spiral_tangent_code_SPIRAL': 'Spiral Transition Alignment',
                'cat__curve_spiral_tangent_code_S': 'Spiral Transition Alignment',
                'cat__curve_spiral_tangent_code_TANGENT': 'Tangent (Straight) Alignment',
                'cat__curve_spiral_tangent_code_T': 'Tangent (Straight) Alignment',
            }

            raw_shap = list(zip(list(feature_names), contribs[:-1]))
            total_abs = sum(abs(v) for _, v in raw_shap) + 1e-6

            raw_shap_sorted = sorted(raw_shap, key=lambda x: abs(x[1]), reverse=True)
            for fname, sval in raw_shap_sorted[:6]:
                flabel = feature_label_map.get(fname, fname.replace("num__", "").replace("cat__", "").replace("_", " ").title())
                direction = "INCREASES_RISK" if sval > 0 else "REDUCES_RISK"
                pct = round(float((abs(sval) / total_abs) * 100), 1)
                shap_list.append(ShapAttribution(
                    feature_name=fname,
                    feature_label=flabel,
                    shap_value=round(float(sval), 4),
                    contribution_direction=direction,
                    importance_pct=pct
                ))
        except Exception:
            pass

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
            shap_attributions=shap_list,
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
