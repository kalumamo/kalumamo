# ML Models Used in AHADU PULSE Project

## Overview
The AHADU PULSE project uses **5 different machine learning models** from scikit-learn for classification, regression, and similarity analysis.

---

## Models by Type

### 1. **Classification Models** (Tier Prediction)

#### A. Logistic Regression Classifier
- **Library**: scikit-learn
- **Class**: `LogisticRegression`
- **Purpose**: Classify products into tiers (LOW, MEDIUM, HIGH)
- **File**: `backend/app/services/ml_service.py` (Lines 282-347)
- **Hyperparameters**:
  ```python
  C=0.1                    # Regularization strength
  max_iter=300             # Max iterations
  solver='lbfgs'          # Solver algorithm
  random_state=42         # Reproducibility
  ```
- **Metrics**: Accuracy, F1-Score, Log Loss
- **Status**: Trained and active (used as fallback if needed)

#### B. Random Forest Classifier
- **Library**: scikit-learn
- **Class**: `RandomForestClassifier`
- **Purpose**: Ensemble-based tier classification
- **File**: `backend/app/services/ml_service.py` (Lines 409-498)
- **Hyperparameters**:
  ```python
  n_estimators=20         # Number of trees
  max_depth=6             # Max tree depth
  min_samples_split=3     # Min samples to split
  random_state=42         # Reproducibility
  n_jobs=-1              # Use all cores
  ```
- **Metrics**: Accuracy, F1-Score, Log Loss, Feature Importance
- **Status**: Trained and active

#### C. Decision Tree Classifier
- **Library**: scikit-learn
- **Class**: `DecisionTreeClassifier`
- **Purpose**: Interpretable rule-based tier classification
- **File**: `backend/app/services/ml_service.py` (Lines 500-581)
- **Hyperparameters**:
  ```python
  max_depth=8             # Max tree depth
  min_samples_split=5     # Min samples to split
  min_samples_leaf=2      # Min samples in leaf
  criterion='gini'        # Split criterion
  random_state=42         # Reproducibility
  ```
- **Metrics**: Accuracy, F1-Score, Log Loss, Feature Importance
- **Status**: Trained and active

---

### 2. **Regression Model** (Score Prediction)

#### Ridge Regression
- **Library**: scikit-learn
- **Class**: `Ridge`
- **Purpose**: Predict continuous performance scores (0-95)
- **File**: `backend/app/services/ml_service.py` (Lines 349-407)
- **Hyperparameters**:
  ```python
  alpha=1.0               # Regularization strength
  ```
- **Metrics**: R² Score, MAE (Mean Absolute Error), MSE
- **Status**: Trained but **not used for predictions** (replaced by rule-based scoring)
- **Note**: System now uses `_compute_performance_score()` rule-based formula instead

---

### 3. **Similarity Model** (Product Clustering)

#### K-Nearest Neighbors (KNN) Classifier
- **Library**: scikit-learn
- **Class**: `KNeighborsClassifier`
- **Purpose**: Find similar products based on feature proximity
- **File**: `backend/app/services/ml_service.py` (Lines 583-634)
- **Hyperparameters**:
  ```python
  n_neighbors=3           # Number of nearest neighbors
  metric='euclidean'      # Distance metric
  ```
- **Metrics**: Similarity scores (0-1)
- **Status**: Trained and active
- **Output**: Stored in `SimilarProduct` table for recommendations

---

### 4. **Preprocessing Model** (Feature Scaling)

#### MinMaxScaler
- **Library**: scikit-learn
- **Class**: `MinMaxScaler`
- **Purpose**: Normalize feature values to [0, 1] range
- **File**: `backend/app/services/ml_service.py` (Lines 122-145)
- **Status**: Fitted during training, used for prediction normalization
- **File Storage**: `ml_models/scaler_latest.pkl`

---

## Feature Engineering Pipeline

### Input Features (14 total)
```python
FEATURES = [
    "active_user_rate",              # active_users / total_users
    "txn_success_rate",              # 1 - failed_txn_rate/100
    "failed_txn_rate",               # raw failure %
    "revenue_per_txn",               # revenue / transactions
    "revenue_per_active_user",       # revenue / active_users
    "operational_efficiency_score",  # weighted metric
    "downtime_impact_score",         # % of time unavailable
    "complaint_growth_rate",         # MoM % change
    "complaint_resolution_rate",     # % resolved
    "fraud_incidents",               # count
    "api_error_rate",               # %
    "user_engagement_index",         # active_rate * txn_count
    "avg_session_duration_sec",      # avg response time
    "csat_score",                    # 1-5 scale
]
```

### Feature Engineering Service
- **File**: `backend/app/services/feature_engineering.py`
- **Process**: Computes 12 derived features from 24 raw data points
- **Output**: Stores in `ProcessedFeatures` table
- **Reprocessing**: Via `reprocess_all()` method (full or per-product)

---

## Model Storage & Registry

### Database Schema
- **Table**: `model_registry`
- **Stores**: Model metadata (name, type, version, metrics, file path)
- **Active Models**: Only one model per type marked `is_active=True`

### File Storage
- **Location**: `backend/ml_models/`
- **Format**: `.pkl` (pickle serialization)
- **Naming**: 
  - `classifier_latest.pkl` - Active classification model
  - `regressor_latest.pkl` - Active regression model
  - `classifier_v20260605091011.pkl` - Versioned models
  - `scaler_latest.pkl` - Feature scaling transformer

---

## Current Prediction Strategy

### What's Actually Used
```
Instead of trained models:
✅ Rule-based scoring formula (_compute_performance_score)
   - Normalizes raw features to 0-1 range
   - Applies weighted component scoring
   - Outputs 50-89 range score
   
Prediction Flow:
Input Features → Normalize → Rule-Based Formula → Score (50-89) → Tier
```

### Why Rule-Based?
- ✅ Transparent and explainable
- ✅ Doesn't depend on trained model quality
- ✅ Consistent across all products
- ✅ Easy to adjust weights for business needs
- ✅ Faster inference (no model loading)

---

## Model Lifecycle

### Training Removed
**Status**: ❌ Training endpoints **NOT AVAILABLE**
- User requested removal of automatic retraining
- Models kept for potential future use
- System uses rule-based scoring instead

### Available Endpoints (Predictions Only)
```
GET  /ml/predictions/bulk           - All products' 3-month forecasts
GET  /ml/predictions/{product_id}   - Single product 3-month forecast
POST /ml/predict                    - Single point prediction
GET  /ml/similar/{product_id}       - Similar products (KNN-based)
```

### Training Pipeline (Available but Disabled)
```
POST /ml/train                      - Train classification models
POST /ml/retrain                    - Retrain specific model type
POST /ml/select-best                - Choose best model by metrics
GET  /ml/models                     - List all trained models
GET  /ml/drift                      - Detect model drift
```

---

## Performance Metrics Tracked

### Classification Models
- **Accuracy**: % correct predictions
- **F1-Score**: Harmonic mean of precision/recall
- **Log Loss**: Cross-entropy error (lower = better)
- **Capped at**: 0.96 max to avoid unrealistic 100% display

### Regression Model
- **R² Score**: Variance explained (0-1)
- **MAE**: Mean Absolute Error (points)
- **MSE**: Mean Squared Error

### Similarity Model
- **Similarity Scores**: 0-1 range
- **Stored Relationships**: In `similar_product` table

---

## Summary Table

| Model | Type | Library | Status | Use Case |
|-------|------|---------|--------|----------|
| **Logistic Regression** | Classification | scikit-learn | Trained | Tier prediction fallback |
| **Random Forest** | Classification | scikit-learn | Trained | Ensemble tier prediction |
| **Decision Tree** | Classification | scikit-learn | Trained | Interpretable tiers |
| **Ridge Regression** | Regression | scikit-learn | Trained (unused) | Score prediction (bypassed) |
| **KNN** | Similarity | scikit-learn | Trained | Product clustering |
| **MinMaxScaler** | Preprocessing | scikit-learn | Fitted | Feature normalization |
| **Rule-Based Formula** | Custom | Python | Active | **Primary scoring** |

---

## Key Implementation Files

- **ML Service**: `backend/app/services/ml_service.py` (1,100+ lines)
- **Feature Engineering**: `backend/app/services/feature_engineering.py` (300+ lines)
- **Models Schema**: `backend/app/models/ml_models.py`
- **API Endpoints**: `backend/app/api/v1/ml.py`
- **Prediction Schemas**: `backend/app/schemas/ml.py`

---

## Conclusion

**AHADU PULSE uses a hybrid approach:**
1. ✅ **5 scikit-learn models** (trained and stored)
2. ✅ **Custom rule-based scoring** (currently active)
3. ✅ **KNN for product similarity** (active)
4. ❌ **Training disabled** (per user request)

**Current Score Range**: 50-89 (optimized formula)  
**Active Prediction Method**: Rule-based + KNN similarity  
**All Metrics**: Tracked and stored in database

---

**Last Updated**: 2026-06-22  
**Backend Version**: Production Ready ✅
