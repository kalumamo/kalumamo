# SHAP Explainability Integration Guide

**For AHADU PULSE ML Models — Optional Enhancement**

---

## Overview

SHAP (SHapley Additive exPlanations) provides model-agnostic explainability by decomposing predictions into feature contributions. This guide explains how to integrate SHAP with AHADU PULSE models for transparent decision-making per Ahadu Bank AI specs.

---

## Installation

```bash
pip install shap
```

**Note**: SHAP requires:
- `numpy ≥ 1.19.0`
- `scipy ≥ 1.5.0`
- `scikit-learn ≥ 0.18.0`

---

## Model-Specific SHAP Integration

### 1. XGBoost Explainability

```python
import shap
import xgboost as xgb
import joblib

# Load trained XGBoost model
model = joblib.load("ml_models/xgboost_latest.pkl")
X_test = ...  # test features

# Create SHAP explainer (fastest for tree models)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Visualizations
# 1. Summary plot (feature importance)
shap.summary_plot(shap_values, X_test, plot_type="bar")

# 2. Dependence plot (feature effect)
shap.dependence_plot("active_user_rate", shap_values, X_test)

# 3. Force plot (single prediction breakdown)
shap.force_plot(explainer.expected_value, 
                shap_values[0], 
                X_test.iloc[0])

# 4. For multi-class (tier prediction)
# shap_values is a list: [shap_for_LOW, shap_for_MEDIUM, shap_for_HIGH]
for i, class_name in enumerate(["LOW", "MEDIUM", "HIGH"]):
    print(f"\n=== Tier: {class_name} ===")
    shap.summary_plot(shap_values[i], X_test, plot_type="bar")
```

### 2. LightGBM Explainability

```python
import shap
import lightgbm as lgb
import joblib

# Load trained LightGBM model
model = joblib.load("ml_models/lightgbm_latest.pkl")
X_test = ...

# Create SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# For multi-class output (list of arrays per class)
if isinstance(shap_values, list):
    for i, class_name in enumerate(["LOW", "MEDIUM", "HIGH"]):
        print(f"=== {class_name} ===")
        shap.summary_plot(shap_values[i], X_test, plot_type="bar")
```

### 3. Logistic Regression / Other Models (Kernel SHAP)

```python
import shap
import joblib

# Load model
model = joblib.load("ml_models/classifier_latest.pkl")
X_test = ...

# Kernel SHAP — model-agnostic but slower
explainer = shap.KernelExplainer(
    lambda x: model.predict_proba(x)[:, 1],  # probability for tier
    X_test[:100]  # background sample (use subset for speed)
)

# This is much slower than TreeExplainer
shap_values = explainer.shap_values(X_test[:10])  # compute on subset

shap.summary_plot(shap_values, X_test[:10])
```

---

## Integration into `ml_service.py`

### Add SHAP Explanation to Predictions

**File**: `backend/app/services/ml_service.py`

```python
import shap

class MLService:
    def __init__(self):
        # ... existing code ...
        self.shap_explainer = None
        self._load_shap_explainer()
    
    def _load_shap_explainer(self):
        """Load SHAP explainer for model interpretability."""
        try:
            import shap
            xgb_model = self._load_artifact("xgboost_latest")
            if xgb_model:
                self.shap_explainer = shap.TreeExplainer(xgb_model)
                log.info("SHAP TreeExplainer loaded for XGBoost")
        except ImportError:
            log.warning("SHAP not installed — explainability disabled")
            self.shap_explainer = None
        except Exception as e:
            log.warning(f"Failed to load SHAP explainer: {e}")
            self.shap_explainer = None
    
    def _get_shap_explanation(self, X: np.ndarray, feature_names: list) -> dict:
        """Generate SHAP feature importance for a prediction."""
        if not self.shap_explainer:
            return {}
        
        try:
            # Get SHAP values for single sample
            shap_values = self.shap_explainer.shap_values(X.reshape(1, -1))
            
            # Handle multi-class output
            if isinstance(shap_values, list):
                # For tier prediction, use HIGH tier explanations
                shap_vals = shap_values[2]  # HIGH tier (index 2)
            else:
                shap_vals = shap_values
            
            # Create feature importance dict
            feature_importance = {}
            for feature, value in zip(feature_names, shap_vals[0]):
                feature_importance[feature] = {
                    "shap_value": float(value),
                    "impact": "positive" if value > 0 else "negative"
                }
            
            return sorted(
                feature_importance.items(),
                key=lambda x: abs(x[1]["shap_value"]),
                reverse=True
            )
        except Exception as e:
            log.warning(f"SHAP explanation failed: {e}")
            return {}
    
    def predict(self, db: Session, product_id: int, features: Optional[dict] = None) -> dict:
        """Enhanced prediction with SHAP explanations."""
        # ... existing code ...
        
        # Add SHAP explanation
        explanation_shap = self._get_shap_explanation(X, feature_names)
        
        result = {
            "product_id": product_id,
            "score": score,
            "tier": tier,
            "explanation_rule_based": explanation,  # existing
            "explanation_shap": explanation_shap,   # NEW
            "models_used": ["rule-based", "xgboost"],
            "timestamp": datetime.now().isoformat(),
        }
        
        return result
```

---

## API Endpoint Update

**File**: `backend/app/api/v1/ml.py`

```python
@router.get("/predict/{product_id}/explain")
def get_prediction_with_explanation(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get prediction with detailed SHAP explainability."""
    ml_service = MLService()
    prediction = ml_service.predict(db, product_id)
    
    return {
        "prediction": prediction,
        "shap_enabled": ml_service.shap_explainer is not None,
        "explanation_type": "shap_tree" if ml_service.shap_explainer else "rule_based_only"
    }
```

---

## Batch Explanation Generation

For explaining multiple predictions (e.g., dashboard background):

```python
def generate_batch_explanations(
    products: List[int],
    db: Session,
    top_n: int = 5
) -> dict:
    """Generate SHAP explanations for multiple products."""
    ml_service = MLService()
    explanations = {}
    
    for product_id in products:
        # Get features
        df = ml_service._load_features_df(db, product_id)
        if df.empty:
            continue
        
        features = df.iloc[0].to_dict()
        X, scaler = ml_service._prepare_X(df)
        
        # Get prediction + SHAP
        shap_exp = ml_service._get_shap_explanation(X, feature_names)
        
        explanations[product_id] = {
            "top_features": shap_exp[:top_n],  # Top 5 contributors
            "summary": f"Tier driven by {shap_exp[0][0]} and {shap_exp[1][0]}"
        }
    
    return explanations
```

---

## Visualization in Frontend (Optional)

If integrating into React dashboard:

```javascript
// Example: Display SHAP waterfall plot
// Requires plotly.js or similar

function displaySHAPExplanation(prediction) {
  if (!prediction.explanation_shap) {
    return null;
  }

  return (
    <div className="shap-explanation">
      <h3>Feature Importance (SHAP)</h3>
      <ul>
        {prediction.explanation_shap.map(([feature, impact]) => (
          <li key={feature}>
            <span className={`impact-${impact.impact}`}>
              {feature}: {impact.shap_value.toFixed(3)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Performance Considerations

### TreeExplainer (Fast)
- **Time**: ~10ms per sample
- **Best for**: XGBoost, LightGBM, Decision Trees
- **Memory**: Low
- **Use case**: Real-time predictions with explanations

### KernelExplainer (Slow)
- **Time**: ~100ms–1s per sample (depends on background samples)
- **Best for**: Any model (model-agnostic)
- **Memory**: High (stores background sample)
- **Use case**: Batch explanations, one-time analysis

### Recommendation
```python
# For production: Use TreeExplainer on XGBoost
# For analysis: Use TreeExplainer on ensemble models
# For one-offs: Use KernelExplainer on any model
```

---

## Monitoring & Interpretation

### What SHAP Values Mean

```
SHAP Value > 0  →  Feature pushes prediction toward tier (e.g., HIGH)
SHAP Value < 0  →  Feature pushes prediction away from tier
|SHAP Value|    →  Magnitude of impact on decision
```

### Example Interpretation

```
Product XYZ Prediction: MEDIUM Tier
SHAP Top Contributors:
  ✓ complaint_resolution_rate=85% → +0.12 (pushes to MEDIUM)
  ✓ csat_score=4.5 → +0.08 (positive impact)
  ✗ downtime_impact_score=35% → -0.09 (slight negative impact)
  ✓ active_user_rate=0.65 → +0.05 (moderate engagement)
```

### Drift Detection with SHAP

```python
def detect_shap_drift(
    historical_shap: np.ndarray,
    current_shap: np.ndarray,
    threshold: float = 0.1
) -> bool:
    """Detect shift in feature importance using SHAP values."""
    from scipy.spatial.distance import wasserstein_distance
    
    distance = wasserstein_distance(
        historical_shap.flatten(),
        current_shap.flatten()
    )
    return distance > threshold
```

---

## Troubleshooting

### Issue: "TreeExplainer initialization error"
```python
# Solution: Ensure model supports tree_path_dependent argument
explainer = shap.TreeExplainer(model, feature_perturbation="interventional")
```

### Issue: "Memory error on large dataset"
```python
# Solution: Use background sample subset
explainer = shap.TreeExplainer(
    model,
    data=X_train[:1000]  # Use subset, not full dataset
)
```

### Issue: "SHAP values all zeros"
```python
# Solution: Check model.objective or use check_additivity=False
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test, check_additivity=False)
```

---

## Resources

- **SHAP Documentation**: https://shap.readthedocs.io/
- **XGBoost + SHAP Example**: https://github.com/slundberg/shap/tree/master/notebooks
- **Interactive SHAP Dashboard**: Use `shap.plots.waterfall()` for single predictions

---

## Next Steps

1. **Install SHAP**: `pip install shap`
2. **Test on sample**: Run TreeExplainer on trained XGBoost
3. **Integrate into API**: Add `/predict/{id}/explain` endpoint
4. **Monitor production**: Track SHAP drift monthly
5. **Visualize in UI**: Display top features in dashboard

---

**Status**: Ready for implementation (Optional enhancement)
**Updated**: June 22, 2026
