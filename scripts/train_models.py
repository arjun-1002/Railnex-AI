"""
Railnex AI — Model Training and Benchmark Evaluation Engine
Trains and compares:
1. Logistic Regression (Linear Baseline with class weighting)
2. Random Forest Classifier (Non-linear Ensemble)
3. XGBoost Classifier (Gradient Boosted Decision Trees)

Evaluates:
- Accuracy, Precision, Recall, Macro-F1, Weighted-F1
- Critical Severity Recall (Red Tag / UML Recall)
- Confusion Matrices and Per-Class Breakdown
- Feature Importance Scores
Saves model artifacts and evaluation metrics to models/
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'TrackPrior-AI', 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

def train_experiment_a_real_models():
    print("=" * 80)
    print("TRAINING EXPERIMENT A: REAL TRACK GEOMETRY DEFECT SEVERITY CLASSIFICATION")
    print("=" * 80)

    train_path = os.path.join(DATA_DIR, 'processed', 'exp_a_real_train.parquet')
    test_path = os.path.join(DATA_DIR, 'processed', 'exp_a_real_test.parquet')
    preprocessor_path = os.path.join(DATA_DIR, 'processed', 'exp_a_preprocessor.joblib')

    df_train = pd.read_parquet(train_path)
    df_test = pd.read_parquet(test_path)
    preprocessor = joblib.load(preprocessor_path)

    # Features and target
    num_features = [
        'defect_length_ft',
        'defect_amplitude_in',
        'defect_volume_proxy',
        'fra_track_class',
        'freight_speed_limit_mph',
        'passenger_speed_limit_mph',
        'speed_ratio',
        'inspection_month'
    ]
    cat_features = [
        'defect_type',
        'curve_spiral_tangent_code',
        'track_code'
    ]
    feature_cols = num_features + cat_features
    target_col = 'severity_target_binary'

    X_train_raw = df_train[feature_cols]
    y_train = df_train[target_col].values
    X_test_raw = df_test[feature_cols]
    y_test = df_test[target_col].values

    # Transform features using training-fitted preprocessor
    X_train = preprocessor.transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

    # Get feature names after one-hot encoding
    cat_encoder = preprocessor.named_transformers_['cat']
    encoded_cat_names = cat_encoder.get_feature_names_out(cat_features).tolist()
    all_feature_names = num_features + encoded_cat_names

    models = {
        "Logistic Regression": LogisticRegression(
            class_weight='balanced',
            max_iter=1000,
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_split=6,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.08,
            scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),
            eval_metric='logloss',
            random_state=42,
            n_jobs=-1
        )
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        macro_f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        weighted_f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        # Critical severity recall is recall of Red Tag (Class 1)
        critical_recall = rec

        # Feature importance
        feat_imp = {}
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            sorted_idx = np.argsort(importances)[::-1]
            for idx in sorted_idx[:15]:
                feat_imp[all_feature_names[idx]] = round(float(importances[idx]), 4)
        elif hasattr(model, 'coef_'):
            coefs = np.abs(model.coef_[0])
            sorted_idx = np.argsort(coefs)[::-1]
            for idx in sorted_idx[:15]:
                feat_imp[all_feature_names[idx]] = round(float(coefs[idx]), 4)

        # Per-class metrics
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        results[name] = {
            "model_name": name,
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "macro_f1": round(float(macro_f1), 4),
            "weighted_f1": round(float(weighted_f1), 4),
            "critical_severity_recall": round(float(critical_recall), 4),
            "confusion_matrix": cm,
            "per_class": {
                "Yellow_Tag_Planned": report['0'],
                "Red_Tag_Urgent": report['1']
            },
            "top_feature_importance": feat_imp
        }

        print(f"  {name} Results: Accuracy={acc:.4f} | Recall(Red Tag)={rec:.4f} | Macro-F1={macro_f1:.4f} | Weighted-F1={weighted_f1:.4f}")

        if weighted_f1 > best_f1:
            best_f1 = weighted_f1
            best_model_name = name

        # Save individual model
        slug = name.lower().replace(' ', '_')
        joblib.dump(model, os.path.join(MODELS_DIR, f"real_model_{slug}.joblib"))

    # Save best model
    best_model = models[best_model_name]
    joblib.dump(best_model, os.path.join(MODELS_DIR, "real_best_severity_model.joblib"))
    joblib.dump(preprocessor, os.path.join(MODELS_DIR, "real_feature_preprocessor.joblib"))
    
    # Save metadata
    meta = {
        "experiment": "Experiment A (Real Track Geometry Severity Classification)",
        "best_model": best_model_name,
        "best_weighted_f1": best_f1,
        "feature_names": all_feature_names,
        "raw_features": {
            "numerical": num_features,
            "categorical": cat_features
        },
        "target_mapping": {
            "0": "Yellow Tag (Pre-Defect / Planned Maintenance)",
            "1": "Red Tag (FRA Safety Exceedance / Urgent Action Required)"
        },
        "benchmark_summary": results
    }
    with open(os.path.join(MODELS_DIR, "experiment_a_evaluation.json"), 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    print(f"\nBest Model for Real Track Geometry: {best_model_name} (Weighted-F1: {best_f1:.4f})")
    print(f"Saved artifacts to {MODELS_DIR}")
    return results

def train_experiment_b_synthetic_models():
    print("\n" + "=" * 80)
    print("TRAINING EXPERIMENT B: SYNTHETIC MULTI-CLASS MAINTENANCE URGENCY PROTOTYPE")
    print("=" * 80)

    train_path = os.path.join(DATA_DIR, 'synthetic', 'exp_b_synthetic_train.parquet')
    test_path = os.path.join(DATA_DIR, 'synthetic', 'exp_b_synthetic_test.parquet')
    preprocessor_path = os.path.join(DATA_DIR, 'synthetic', 'exp_b_preprocessor.joblib')

    df_train = pd.read_parquet(train_path)
    df_test = pd.read_parquet(test_path)
    preprocessor = joblib.load(preprocessor_path)

    num_features = [
        'track_temperature_c',
        'rail_wear_mm',
        'track_vibration_level',
        'track_curvature_degree',
        'ambient_temperature_c',
        'humidity_percent',
        'rainfall_mm',
        'wind_speed_kmph',
        'train_age_years',
        'average_speed_kmph',
        'distance_travelled_km',
        'daily_trips',
        'load_factor_percent',
        'power_consumption_kw'
    ]
    cat_features = [
        'ballast_condition',
        'region',
        'season',
        'train_type'
    ]
    feature_cols = num_features + cat_features
    target_col = 'severity_level_ordinal'

    X_train_raw = df_train[feature_cols]
    y_train = df_train[target_col].values
    X_test_raw = df_test[feature_cols]
    y_test = df_test[target_col].values

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, num_features),
            ('cat', cat_pipeline, cat_features)
        ]
    )

    X_train = preprocessor.fit_transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

    cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
    encoded_cat_names = cat_encoder.get_feature_names_out(cat_features).tolist()
    all_feature_names = num_features + encoded_cat_names

    models = {
        "Logistic Regression": LogisticRegression(
            class_weight='balanced',
            max_iter=1000,
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            eval_metric='mlogloss',
            random_state=42,
            n_jobs=-1
        )
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0

    for name, model in models.items():
        print(f"\nTraining Synthetic {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        weighted_f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        # Critical recall is class 4 (Critical)
        rep = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        critical_recall = rep.get('4', {}).get('recall', 0.0)

        results[name] = {
            "model_name": name,
            "accuracy": round(float(acc), 4),
            "macro_f1": round(float(macro_f1), 4),
            "weighted_f1": round(float(weighted_f1), 4),
            "critical_severity_recall": round(float(critical_recall), 4),
            "confusion_matrix": cm,
            "per_class": {f"Class_{k}": v for k, v in rep.items() if k.isdigit()}
        }

        print(f"  Synthetic {name}: Accuracy={acc:.4f} | Critical Recall={critical_recall:.4f} | Macro-F1={macro_f1:.4f}")
        if weighted_f1 > best_f1:
            best_f1 = weighted_f1
            best_model_name = name

        slug = name.lower().replace(' ', '_')
        joblib.dump(model, os.path.join(MODELS_DIR, f"synthetic_model_{slug}.joblib"))

    best_synth_model = models[best_model_name]
    joblib.dump(best_synth_model, os.path.join(MODELS_DIR, "synthetic_best_model.joblib"))
    joblib.dump(preprocessor, os.path.join(MODELS_DIR, "synthetic_feature_preprocessor.joblib"))

    meta = {
        "experiment": "Experiment B (Synthetic Maintenance Urgency Prototype)",
        "disclaimer": "SYNTHETIC DATA — NOT VALIDATED ON INDIAN RAILWAYS RECORDS",
        "best_model": best_model_name,
        "best_weighted_f1": best_f1,
        "feature_names": all_feature_names,
        "target_mapping": {
            "0": "None",
            "1": "Low",
            "2": "Medium",
            "3": "High",
            "4": "Critical"
        },
        "benchmark_summary": results
    }
    with open(os.path.join(MODELS_DIR, "experiment_b_evaluation.json"), 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    print(f"\nBest Synthetic Model: {best_model_name} (Weighted-F1: {best_f1:.4f})")
    return results

def main():
    train_experiment_a_real_models()
    train_experiment_b_synthetic_models()
    print("\nAll models trained and benchmarked successfully!")

if __name__ == '__main__':
    main()
