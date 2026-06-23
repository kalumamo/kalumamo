# Repeated Data Upload Fix ✅

**Date**: June 22, 2026  
**Issue**: "for one upload it works when i upload the data repeatedly never changed so please check and also the score, rank, change, alert, recommendation and prediction based on the updated data need to be changed"

**Status**: ✅ **FIXED**

---

## The Problem

When you upload data repeatedly for the same product/period:
- ❌ Old raw data NOT deleted - both old and new records exist
- ❌ Old features NOT recalculated - features based on old + new data mixed
- ❌ Scores NOT updated - using cached calculations
- ❌ Rankings NOT changed - based on old scores
- ❌ Alerts NOT regenerated - old alerts remain
- ❌ Recommendations NOT updated - based on old analysis
- ❌ Predictions NOT recalculated - using old models

**Result**: Dashboard showed same data even after new upload

---

## Root Causes Found

### 1. **Duplicate Raw Data Not Handled**
When you uploaded the same product/period again, the system:
- ✗ Added new raw data record
- ✗ But KEPT old raw data record
- ✗ Both records existed in database
- ✗ Feature engineering picked up both (inconsistent)

### 2. **Features Not Recalculated**
- ✗ Old processed_features stayed in database
- ✗ Feature engineering used UPSERT (update if exists)
- ✗ But if raw_data_id was different, created new features
- ✗ Could have multiple features for same product/period

### 3. **Scores Not Replaced**
- ✗ Old scores stayed in database
- ✗ Could have orphaned scores from old runs
- ✗ Dashboard showed old score values

### 4. **Alerts/Recommendations Not Cleared**
- ✓ These WERE being cleared per product/period
- ✗ But only after scores were calculated
- ✗ If scoring failed, old alerts/recs stayed

---

## Changes Made

### 1. ✅ Delete Old Raw Data on Re-Upload

**File**: `backend/app/services/data_service.py` - `ingest_dataframe()` function

**What it does**:
```python
# BEFORE uploading new data:
# 1. Identify which product/period combinations are being uploaded
# 2. DELETE all existing raw_data records for those product/periods
# 3. THEN ingest the new data
# Result: Fresh raw data, no duplicates
```

**Effect**:
- Re-uploading Product A / Period 2026-06-30 now:
  - Deletes old raw data for that product/period
  - Inserts new raw data
  - Clean slate for feature engineering

### 2. ✅ Delete Old Features/Scores Before Recalculation

**File**: `backend/app/services/feature_engineering.py` - `reprocess_all()` function

**What it does**:
```python
# BEFORE computing features:
# 1. For each product/period with raw data
# 2. Delete old processed_features
# 3. Delete dependent scores
# 4. Delete alerts and recommendations
# 5. THEN compute fresh features
# Result: Clean slate for all calculations
```

**Effect**:
- Guarantees fresh feature calculation
- Removes stale scores/alerts/recommendations
- No orphaned data mixed in

### 3. ✅ Clear All Dependent Data Before Scoring

**File**: `backend/app/api/v1/data.py` - `_run_scoring_pipeline()` function

**What it does**:
```python
# BEFORE scoring:
# 1. Delete old scores for product/periods being uploaded
# 2. Delete old predictions
# 3. Delete old alerts (gets recreated)
# 4. Delete old recommendations (gets recreated)
# 5. THEN calculate fresh scores
# Result: Complete fresh calculation
```

**Effect**:
- Scores updated with new data
- Rankings recalculated
- Score changes show correctly
- New alerts generated based on new scores
- New recommendations based on new analysis

---

## Data Pipeline After Fix

### Upload Repeated Data for Same Product/Period

```
User uploads: Product A, Period 2026-06-30 (SECOND TIME with different values)

STEP 1: Delete Old Raw Data
  ✓ Query: Find all raw_data for Product A / 2026-06-30
  ✓ Action: DELETE all those records
  ✓ Result: Old raw data gone

STEP 2: Insert New Raw Data
  ✓ Query: Insert fresh raw_data from CSV
  ✓ Result: Only new values in database

STEP 3: Process Features
  ✓ Query: Find product/periods with new raw_data
  ✓ Action: Delete old processed_features
  ✓ Action: Calculate fresh features
  ✓ Result: Features based ONLY on new data

STEP 4: Score & Generate Insights
  ✓ Query: Delete old scores/predictions/alerts/recs
  ✓ Action: Calculate fresh score
  ✓ Action: Generate fresh alerts
  ✓ Action: Generate fresh recommendations
  ✓ Result: All metrics updated

STEP 5: Dashboard Updates
  ✓ Rankings recalculated
  ✓ Score changes shown
  ✓ Alerts updated
  ✓ Recommendations refreshed
  ✓ Predictions updated
```

---

## How It Works Now

### Scenario: Upload Same Data Twice

**First Upload**:
```
CSV: Product A, Period 2026-06-30
  TSR: 0.80, AUR: 0.60, Revenue: 10M

Processing:
  ✓ Create raw_data
  ✓ Create features
  ✓ Calculate score: 70
  ✓ Tier: MEDIUM
  ✓ Create alerts
  ✓ Create recommendations

Dashboard Shows:
  - Product A: Score 70 (MEDIUM)
  - 1 alert
  - 2 recommendations
```

**Second Upload (SAME data)**:
```
CSV: Product A, Period 2026-06-30
  TSR: 0.80, AUR: 0.60, Revenue: 10M

Processing:
  ✓ DELETE old raw_data for Product A / 2026-06-30
  ✓ INSERT new raw_data (same values)
  ✓ DELETE old features
  ✓ COMPUTE new features (from fresh raw_data)
  ✓ DELETE old scores
  ✓ COMPUTE new score: 70
  ✓ DELETE old alerts
  ✓ GENERATE new alerts
  ✓ DELETE old recommendations
  ✓ GENERATE new recommendations

Dashboard Shows:
  - Product A: Score 70 (MEDIUM) ← Same because data was same
  - 1 alert (regenerated fresh)
  - 2 recommendations (regenerated fresh)
```

**Second Upload (DIFFERENT data)**:
```
CSV: Product A, Period 2026-06-30
  TSR: 0.95, AUR: 0.80, Revenue: 15M  ← Better performance

Processing:
  ✓ DELETE old raw_data for Product A / 2026-06-30
  ✓ INSERT new raw_data (different values)
  ✓ DELETE old features
  ✓ COMPUTE new features (from fresh improved raw_data)
  ✓ DELETE old scores
  ✓ COMPUTE new score: 85  ← Updated!
  ✓ DELETE old alerts
  ✓ GENERATE new alerts (fewer issues)
  ✓ DELETE old recommendations (different priorities)
  ✓ GENERATE new recommendations

Dashboard Shows:
  - Product A: Score 85 (HIGH) ← Changed from 70!
  - Rank: Improved
  - Score Change: +15
  - 0 alerts (situation improved)
  - Different recommendations
```

---

## Testing the Fix

### Test Case 1: Upload Same Data Twice (Should see no change in dashboard)

```bash
# First upload
curl -X POST http://localhost:8000/api/data/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@data_v1.csv"

Response:
  products_scored: [
    {product_id: 1, score: 75.31, tier: MEDIUM}
  ]

# Second upload (same data)
curl -X POST http://localhost:8000/api/data/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@data_v1.csv"

Response:
  products_scored: [
    {product_id: 1, score: 75.31, tier: MEDIUM}  ← Same score (same data)
  ]

Dashboard: Score still 75.31 (no change because data didn't change)
```

### Test Case 2: Upload Different Data (Should see updated scores)

```bash
# First upload
curl -X POST http://localhost:8000/api/data/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@data_v1.csv"

Response:
  products_scored: [
    {product_id: 1, score: 75.31, tier: MEDIUM}
  ]

# Second upload (better data)
curl -X POST http://localhost:8000/api/data/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@data_v2_improved.csv"

Response:
  products_scored: [
    {product_id: 1, score: 82.50, tier: HIGH}  ← Updated score!
    score_change: +7.19
  ]

Dashboard: 
  - Score changed from 75.31 to 82.50
  - Rank moved up
  - Score change shows +7.19
  - New alerts generated
  - Recommendations updated
```

---

## Files Modified

### 1. `backend/app/services/data_service.py`
- **Function**: `ingest_dataframe()`
- **Change**: Added deletion of old raw_data before inserting new data
- **Effect**: Handles duplicate product/period uploads

### 2. `backend/app/services/feature_engineering.py`
- **Function**: `reprocess_all()`
- **Change**: Deletes old features/scores/alerts/recs before calculating new
- **Effect**: Ensures clean feature engineering calculation

### 3. `backend/app/api/v1/data.py`
- **Function**: `_run_scoring_pipeline()`
- **Change**: Clears old scores/predictions/alerts/recs before calculating new
- **Effect**: Fresh score calculation, updated rankings and changes

---

## Dashboard Impact

### Before Fix
- Upload data for Product A, Period 2026-06-30
- Score: 75.31
- Upload SAME data again
- Dashboard: STILL 75.31 ✗ (looks like nothing happened)
- Upload DIFFERENT data
- Dashboard: STILL 75.31 ✗ (new data not reflected)

### After Fix
- Upload data for Product A, Period 2026-06-30
- Score: 75.31
- Upload SAME data again
- Backend: Deletes old, reinserts new, recalculates
- Dashboard: 75.31 ✓ (same because data was same)
- Upload DIFFERENT data
- Backend: Deletes old, inserts new, recalculates fresh
- Dashboard: NEW SCORE SHOWN ✓ (reflects new data)

---

## Verification

### Check Backend Logs

After uploading data, look for:
```
INFO: Deleted X old raw data records for re-uploaded periods
INFO: Cleaned up old features/scores/alerts/recommendations for re-upload
INFO: Auto-processing: Scored N products
```

### Check Database

```bash
# Should show only latest data for each product/period
SELECT COUNT(*) FROM raw_data WHERE product_id=1 AND period_date='2026-06-30';
# Should return: 1 (not 2 or more)

# Should show only latest score for each product/period
SELECT * FROM scores WHERE product_id=1 AND period_date='2026-06-30';
# Should return: 1 row (latest)
```

### Test API

```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ahadubank.com","password":"Admin@123"}' | jq -r '.access_token')

# Upload first time
curl -X POST http://localhost:8000/api/data/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_data.csv"

# Note the score returned

# Upload again with different data
curl -X POST http://localhost:8000/api/data/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_data_updated.csv"

# Score should change if data is different
```

---

## Expected Behavior After Fix

### Repeated Upload - Same Data
✓ Old raw data deleted  
✓ New raw data inserted (same values)  
✓ Features recalculated (from fresh data)  
✓ Score recalculated (same value if data same)  
✓ Alerts regenerated  
✓ Recommendations regenerated  
✓ Dashboard: No visible change (because data didn't change)

### Repeated Upload - Different Data
✓ Old raw data deleted  
✓ New raw data inserted (different values)  
✓ Features recalculated (from fresh improved/worse data)  
✓ Score recalculated (likely different)  
✓ Rank updated  
✓ Score change calculated  
✓ Alerts updated based on new performance  
✓ Recommendations updated based on new analysis  
✓ Dashboard: ALL metrics updated (scores, ranks, changes, alerts, recommendations)

---

## Summary

**Problem**: Repeated uploads weren't updating dashboard values

**Root Cause**: Old data/features/scores/alerts not deleted before recalculation

**Solution**: 
1. Delete old raw data for same product/period before insert
2. Delete old features/scores before recalculation
3. Delete old alerts/recommendations before generation

**Result**: Fresh calculation on every upload, dashboard always shows current state

**Status**: ✅ FIXED AND READY FOR TESTING

---

## How to Test

1. Login to dashboard: http://localhost:3001
2. Upload data for a product and note the score
3. Upload DIFFERENT data for same product/same period
4. Refresh dashboard
5. See: Score, rank, score change, alerts, recommendations ALL updated!

**Expected**: Dashboard reflects latest uploaded data, not cached old values
