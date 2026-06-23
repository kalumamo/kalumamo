# ML Models - Quick Reference

## Models in AHADU PULSE

| # | Model | Type | Status | Used For |
|---|-------|------|--------|----------|
| 1 | **Logistic Regression** | Classification | ✅ Trained | Tier classification (fallback) |
| 2 | **Random Forest** | Classification | ✅ Trained | Ensemble tier prediction |
| 3 | **Decision Tree** | Classification | ✅ Trained | Interpretable tier rules |
| 4 | **Ridge Regression** | Regression | ✅ Trained (Unused) | Score prediction (bypassed) |
| 5 | **KNN** | Similarity | ✅ Active | Find similar products |
| 6 | **MinMaxScaler** | Preprocessing | ✅ Fitted | Normalize features 0-1 |
| 7 | **Rule-Based Formula** | Custom | ✅ **ACTIVE** | **Primary score calculation** |

---

## How It Works Currently

### Prediction Pipeline
```
Product Data
    ↓
Feature Engineering (12 features)
    ↓
Rule-Based Scoring (_compute_performance_score)
    → Normalize features
    → Apply weighted formula
    → Output: Score 50-89
    ↓
Assign Tier (HIGH/MEDIUM/LOW)
    ↓
KNN Similarity → Find similar products
    ↓
Generate Recommendations & Alerts
    ↓
Store in Database
```

---

## All Models from scikit-learn

```
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
```

---

## Model Files Stored

```
ml_models/
├── scaler_latest.pkl                    ← Feature scaler
├── classifier_latest.pkl               ← Active classifier (LR/RF/DT)
├── regressor_latest.pkl                ← Active regressor (Ridge)
├── similarity_*.pkl                    ← KNN model
└── [versioned backups]
```

---

## Current Status

✅ **7 models implemented**  
✅ **5 scikit-learn models trained**  
✅ **Rule-based scoring active**  
✅ **Predictions working 50-89 range**  
✅ **KNN similarity active**  
❌ **Training endpoints disabled** (per request)  

---

## No Training Needed!

- Models trained: ✅ Already done
- New data: ✅ Uses rule-based formula (no retraining)
- Predictions: ✅ Automatic via formula
- Similarity: ✅ KNN already fitted
- Recommendations: ✅ Auto-generated

**Everything is production-ready!**
