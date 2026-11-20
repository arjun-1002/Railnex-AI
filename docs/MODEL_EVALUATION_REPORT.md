# RailRakshak AI: Academic Supervised Learning Evaluation Report

**Course:** Supervised Learning (INT395) — Topic 20: Railway Track Defect Severity Classification  
**Generated:** 2026-11-20 14:46:12  
**Partitioning Protocol:** Strict Chronological Out-of-Time Splitting ($T_{\text{split}} = \text{2012-01-01}$)  
**Sample Size:** Train: 17,283 records (2007–2011) | Test: 6,564 records (2012–2013)  
**Champion Model Selected:** **LightGBM**  

---

## 1. Comparative Model Benchmark Table

| Algorithm Architecture | Accuracy | **Macro-F1 (Primary)** | Weighted-F1 | **Critical (Class 3) Recall** | Critical False Negatives | ROC-AUC (OVR) | Fit Time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LightGBM** | 99.48% | **99.49%** | 99.48% | **99.52%** | 2 / 417 | 1.0000 | 0.38s |
| XGBoost Champion | 99.48% | **99.40%** | 99.48% | **99.04%** | 4 / 417 | 1.0000 | 0.46s |
| Random Forest | 99.39% | **99.25%** | 99.39% | **97.84%** | 9 / 417 | 1.0000 | 0.26s |
| Decision Tree | 99.27% | **99.11%** | 99.27% | **98.80%** | 5 / 417 | 0.9974 | 0.02s |
| K-Nearest Neighbours | 97.33% | **96.16%** | 97.32% | **88.49%** | 48 / 417 | 0.9956 | 0.04s |
| Logistic Regression | 96.39% | **94.35%** | 96.46% | **95.68%** | 18 / 417 | 0.9961 | 0.23s |
| Support Vector Machine | 90.95% | **87.91%** | 90.89% | **69.06%** | 129 / 417 | 0.9862 | 0.13s |

---

## 2. Confusion Matrices (Out-of-Time Test Set: 6,564 Records)

Classes: **0 = Normal (Green)**, **1 = Minor (Yellow)**, **2 = Major (Orange)**, **3 = Critical (Red)**

### LightGBM
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2090              0             16              0
Actual Class 1 :          0           1899             14              0
Actual Class 2 :          0              0           2126              2
Actual Class 3 :          0              0              2            415
```

### XGBoost Champion
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2093              0             13              0
Actual Class 1 :          0           1900             13              0
Actual Class 2 :          0              0           2124              4
Actual Class 3 :          0              0              4            413
```

### Random Forest
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2091              0             15              0
Actual Class 1 :          0           1899             14              0
Actual Class 2 :          0              0           2126              2
Actual Class 3 :          0              0              9            408
```

### Decision Tree
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2090              0             16              0
Actual Class 1 :          0           1896             17              0
Actual Class 2 :          0              2           2118              8
Actual Class 3 :          0              0              5            412
```

### K-Nearest Neighbours
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2086              4             16              0
Actual Class 1 :          7           1882             22              2
Actual Class 2 :          9             48           2052             19
Actual Class 3 :          0              0             48            369
```

### Logistic Regression
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2105              1              0              0
Actual Class 1 :          4           1845             64              0
Actual Class 2 :         14             22           1978            114
Actual Class 3 :          0              0             18            399
```

### Support Vector Machine
```
                Predicted 0    Predicted 1    Predicted 2    Predicted 3
Actual Class 0 :       2067             39              0              0
Actual Class 1 :          2           1767            144              0
Actual Class 2 :         10            218           1848             52
Actual Class 3 :          0              0            129            288
```

---

## 3. Academic Findings & Safety Invariance Analysis

1. **Macro-F1 as Primary Academic Metric:** In safety-critical railway infrastructure, treating all classes with equal priority prevents majority-class dominance (minor defects) from masking performance on rare, catastrophic defects (Class 3 Critical).
2. **Elimination of Temporal Lookahead Leakage:** By splitting chronologically at `2012-01-01` (rather than randomized k-fold splitting), test records represent future uninspected track runs, replicating true deployment conditions.
3. **Zero-Defect Safety Sensitivity:** The Champion model minimizes Critical-Class false negatives, ensuring that dangerous crosslevel and profile anomalies exceeding statutory limits are flagged for urgent specialist assessment.