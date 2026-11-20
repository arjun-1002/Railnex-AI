"""
RailRakshak AI — AI Railway Maintenance Assistant (Module 16)
Domain-grounded conversational agent referencing official Indian Railways standards
(IRPWM 2020, RDSO USFD Manual, CAG Report No. 22 of 2022) and ML model metrics.
"""

from datetime import datetime
from typing import Dict, Any, List
from ..schemas.models import AssistantChatResponse

KNOWLEDGE_BASE = {
    "crosslevel": {
        "keywords": ["crosslevel", "xlevel", "superelevation", "cant"],
        "answer": (
            "Crosslevel (XLEVEL) refers to the difference in vertical elevation between the running rails. "
            "Under Indian Railways Permanent Way Manual (IRPWM 2020 Table 5.1), on Broad Gauge routes with speed >= 130 km/h (Group A), "
            "the Need-Based Maintenance Limit (NBML) is 6.0 mm, Planned Maintenance Limit (PML) is 10.0 mm, "
            "and Urgent Maintenance Limit (UML) is 15.0 mm. Exceeding UML requires immediate 30 km/h caution orders "
            "because sudden crosslevel change triggers wheel unloading and flange climb derailment (Nadal Criterion)."
        ),
        "standards": ["IRPWM 2020 Table 5.1 (Crosslevel Limits)", "IRPWM Para 5.1 Track Monitoring"]
    },
    "twist": {
        "keywords": ["twist", "warp", "cant deficiency"],
        "answer": (
            "Track Twist is the rate of change of crosslevel per unit length (measured on 3.0m or 3.6m base). "
            "Excessive track twist causes diagonal wheel unloading where one wheel loses contact pressure with the rail head, "
            "creating an acute derailment risk on curves and turnout transitions. "
            "According to the CAG Derailment Audit (Report No. 22 of 2022), excessive crosslevel variation and twist "
            "accounted for 22.7% of all investigated track-defect derailments in Indian Railways."
        ),
        "standards": ["CAG Report No. 22 of 2022", "IRPWM 2020 Para 5.1 Track Twist"]
    },
    "usfd": {
        "keywords": ["usfd", "ultrasonic", "flaw", "imr", "obs", "probe"],
        "answer": (
            "Ultrasonic Flaw Detection (USFD) is governed by the RDSO Manual for Ultrasonic Testing of Rails and Welds. "
            "Key flaw classifications include: 111/113 (Transverse Fissure in head - IMR), 411 (Bolt hole star cracks - IMR), "
            "and 711 (Alumino-Thermic weld lack of fusion - IMRW). "
            "IMR (Immediate Removal) mandates immediate clamping with joggled fishplates, a 30 km/h emergency speed restriction, "
            "and rail replacement within 3 days. Testing frequency ranges from every 2 months for routes carrying > 40 GMT "
            "to once a year for branch lines (< 5 GMT)."
        ),
        "standards": ["RDSO USFD Manual (Revised 2020)", "IRPWM Chapter 4 Rail Maintenance"]
    },
    "buckling": {
        "keywords": ["buckle", "buckling", "heat", "rail temperature", "summer", "lwr", "cwr"],
        "answer": (
            "Track buckling occurs when thermal compressive stress in Continuous Welded Rails (CWR/LWR) exceeds "
            "the lateral resistance of the ballast shoulder. Rail temperature (T_rail) in direct sun typically reaches "
            "18–20°C above ambient air temperature. If T_rail exceeds Destressing Temperature (Td) + 20°C (usually > 60°C), "
            "hot weather patrolling is mandatory from 11:00 to 17:00 hrs. Ballast shoulder width must be maintained at >= 350 mm."
        ),
        "standards": ["IRPWM Chapter 8 LWR/CWR Manual", "RDSO Track Buckling Prevention Guidelines"]
    },
    "model": {
        "keywords": ["model", "macro-f1", "accuracy", "algorithm", "lightgbm", "xgboost", "metric"],
        "answer": (
            "RailRakshak AI evaluated 7 supervised learning algorithms on 23,847 real geometry car records using a "
            "strict chronological split at 2012-01-01. LightGBM achieved the Champion score with a Macro-F1 of 99.49%, "
            "Overall Accuracy of 99.48%, and a safety-critical Class 3 (Critical) Recall of 99.52% (missing only 2 out of 417 critical defects). "
            "Macro-F1 is selected as the primary academic metric to ensure equal weighting across minority safety-critical defects."
        ),
        "standards": ["INT395 Topic 20 Benchmark", "docs/MODEL_EVALUATION_REPORT.md"]
    },
    "macro-f1": {
        "keywords": ["macro", "f1", "imbalance", "recall"],
        "answer": (
            "Macro-F1 computes the unweighted arithmetic mean of F1 scores across all four classes: "
            "Macro-F1 = (F1_0 + F1_1 + F1_2 + F1_3) / 4. Unlike Weighted-F1, Macro-F1 treats the critical minority class (Class 3: 6.91% of data) "
            "with identical importance as the majority normal class, preventing high accuracy on common defects from concealing missed critical hazards."
        ),
        "standards": ["INT395 Academic Requirements Section 7", "Scikit-Learn Evaluation Protocol"]
    }
}

class AssistantService:
    def chat(self, query: str, zone: str = None) -> AssistantChatResponse:
        q_lower = query.lower().strip()
        matched_kb = None

        for key, entry in KNOWLEDGE_BASE.items():
            if any(kw in q_lower for kw in entry["keywords"]):
                matched_kb = entry
                break

        if matched_kb:
            resp_text = matched_kb["answer"]
            standards = matched_kb["standards"]
            followups = [
                "What are the IRPWM 2020 Urgent Maintenance Limits for speed >= 130 km/h?",
                "How does Track Twist differ from Crosslevel anomaly?",
                "What actions are mandated for an RDSO Code 111 IMR defect?",
                "Explain how Macro-F1 evaluates class imbalance in RailRakshak AI."
            ]
        else:
            resp_text = (
                f"RailRakshak AI Assistant received your query: '{query}'. "
                "I can assist with Indian Railways Permanent Way Manual (IRPWM 2020) geometry thresholds, "
                "RDSO Ultrasonic Flaw Detection (USFD) defect codes (IMR, OBS), CAG derailment causation audit analytics, "
                "climate buckling risks, or supervised learning evaluation metrics (Macro-F1, TreeSHAP). "
                "Please specify a track defect parameter or operational standard you wish to explore."
            )
            standards = ["IRPWM 2020 Table 5.1", "RDSO USFD Manual", "CAG Derailment Report No. 22"]
            followups = [
                "Explain Crosslevel vs Track Twist derailment risks",
                "What is the difference between IMR and OBS in USFD?",
                "Show LightGBM model evaluation metrics on the 2012–2013 test set",
                "How does summer rail temperature relate to track buckling?"
            ]

        return AssistantChatResponse(
            response_text=resp_text,
            referenced_standards=standards,
            suggested_followups=followups,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
