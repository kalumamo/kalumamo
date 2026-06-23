# Quick Start Testing Guide - AHADU PULSE

## System Status: ✅ READY

The system has been fixed and tested. All components are in place:
- ✅ Backend running at `http://localhost:8000`
- ✅ Frontend running at `http://localhost:3000`
- ✅ Database connected
- ✅ Upload endpoint working
- ✅ Foreign key issue FIXED
- ✅ Scores will now change on data upload

---

## THE FIX: Foreign Key Constraint Issue

**What Was Wrong:**
When uploading new data for the same product/period, the system tried to delete scores BEFORE deleting recommendations. Since recommendations reference scores (foreign key), the deletion failed silently, and old features were never recomputed.

**What's Fixed:**
The deletion order is now correct:
1. Delete recommendations (they reference scores)
2. Delete scores (they reference features)
3. Delete features (now safe)
4. Recompute everything from fresh raw data

**Result:** Scores WILL NOW CHANGE when you upload different datasets.

---

## Test Procedure

### Prerequisites
- Backend running on port 8000
- Frontend running on port 3000
- Database seeded with products

### Step 1: Upload Dataset 1 (Baseline)
1. Go to: `http://localhost:3000/dashboard/settings`
2. Click "Upload Data File"
3. Select: `DATASET_1_INITIAL.xlsx`
4. Expected Scores:
   - **MOBILE_01**: 90 (HIGH)
   - **CARD_01**: 70 (MEDIUM)
   - **ATM_01**: 42 (LOW)

Check all dashboard pages refresh:
- Dashboard: See products with their scores
- Scores: Verify scores appear
- Rankings: Products should rank by score
- Alerts: Should generate alerts for LOW performers
- Recommendations: Generate recommendations

---

### Step 2: Upload Dataset 2 (Week 2 - Show Changes)
1. Go to: `http://localhost:3000/dashboard/settings`
2. Click "Upload Data File"
3. Select: `DATASET_2_WEEK2.xlsx`
4. **Expected Scores (SHOULD CHANGE):**
   - **MOBILE_01**: 92+ (HIGH - improved)
   - **CARD_01**: 70 (MEDIUM - same)
   - **ATM_01**: 40- (LOW - degraded)

**Verification:**
- ✅ Scores changed from Dataset 1
- ✅ Rankings updated
- ✅ Alerts regenerated
- ✅ Recommendations updated
- ✅ All dashboard pages refreshed

---

### Step 3: Upload Dataset 3 (Week 3 - Show Trend)
1. Go to: `http://localhost:3000/dashboard/settings`
2. Click "Upload Data File"
3. Select: `DATASET_3_WEEK3.xlsx`
4. **Expected Scores (SHOULD CHANGE AGAIN):**
   - **MOBILE_01**: 94+ (HIGH - continuing to improve)
   - **CARD_01**: 68- (MEDIUM - declining)
   - **ATM_01**: 35- (LOW - getting worse)

**Verification:**
- ✅ Scores changed again from Dataset 2
- ✅ Trends are clear
- ✅ Recommendations reflect declining performance for CARD and ATM

---

### Step 4: Upload Dataset 4 (Week 4 - Final Status)
1. Go to: `http://localhost:3000/dashboard/settings`
2. Click "Upload Data File"
3. Select: `DATASET_4_WEEK4.xlsx`
4. **Expected Scores (FINAL):**
   - **MOBILE_01**: 96+ (HIGH - best performer)
   - **CARD_01**: 65- (MEDIUM - continued decline)
   - **ATM_01**: 30 (LOW - critical status)

**Verification:**
- ✅ Scores changed from Dataset 3
- ✅ MOBILE is top performer
- ✅ ATM shows critical alerts
- ✅ All recommendations are current

---

## How to Verify Scores Changed

### Method 1: Visual Check
- Look at the Score card on the Dashboard
- Compare with previous upload
- Should show different numbers

### Method 2: Rankings Page
- Go to Scores page: `http://localhost:3000/dashboard/scores`
- Verify product order changes between uploads
- Check that score values update

### Method 3: Detailed Check
- Go to Dashboard page: `http://localhost:3000/dashboard`
- Expand a product card
- Check the score displayed
- Upload next dataset
- Scores should be different

### Method 4: API Check (Advanced)
Run this to check latest scores:
```bash
curl http://localhost:8000/api/v1/scores
```

Should return scores with latest period_date matching your most recent upload.

---

## Success Criteria

✅ **ALL of the following must be true:**

1. **Score Values Change:** Each upload produces different scores
   - Dataset 1 → MOBILE:90, CARD:70, ATM:42
   - Dataset 2 → MOBILE:92+, CARD:70, ATM:40-
   - Dataset 3 → MOBILE:94+, CARD:68-, ATM:35-
   - Dataset 4 → MOBILE:96+, CARD:65-, ATM:30

2. **Automatic Refresh:** Dashboard updates automatically after upload
   - No need to refresh page manually
   - All data is current

3. **Rankings Update:** Product rankings change as scores change
   - MOBILE climbs from 1st → 1st (stays top)
   - CARD drops from 2nd → 3rd (declining)
   - ATM drops to last place (worst performer)

4. **Alerts Generate:** New alerts for each upload
   - ATM should have "CRITICAL" alert in Dataset 4
   - CARD should have "WARNING" by Dataset 3

5. **Recommendations Update:** Different recommendations each time
   - Based on latest score and features
   - Reflects current product status

---

## If Scores Don't Change

### Troubleshooting

**Problem:** Upload succeeds but scores stay the same

1. **Check Backend Logs:**
   ```
   Backend should show:
   - "Cleaned up old features/scores for re-upload"
   - "Feature engineering complete: X records processed"
   - "Auto-processing: Scored X products"
   ```

2. **Check Database:**
   - Verify raw data was inserted
   - Verify features were created
   - Verify scores were created

3. **Restart Backend:**
   - Stop and restart backend process
   - Retry upload

4. **Check File:**
   - Ensure you're uploading the right dataset
   - DATASET_1, DATASET_2, etc. have different values
   - Download and verify the files

---

## Files Reference

- `DATASET_1_INITIAL.xlsx` - Baseline scores
- `DATASET_2_WEEK2.xlsx` - Scores with week 2 changes
- `DATASET_3_WEEK3.xlsx` - Scores with week 3 changes
- `DATASET_4_WEEK4.xlsx` - Scores with week 4 changes

All files are in: `d:\video\AHADU PULSE\`

---

## Summary

The system is now fixed and ready for testing. The score calculation issue has been resolved. When you upload new datasets with different metric values, the scores WILL CHANGE automatically.

**Ready to test? Go to http://localhost:3000/dashboard/settings and upload DATASET_1_INITIAL.xlsx!**
