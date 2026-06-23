# AHADU PULSE — Progressive Dataset Testing Guide

## 📊 Overview

This guide shows you how to upload 4 sequential datasets to verify that **every upload refreshes and updates all dashboard pages** with new data, scores, rankings, alerts, and recommendations.

Each dataset represents a **one-week period** showing how products perform over time:
- Product metrics change
- Scores increase/decrease
- Rankings shift
- Alerts appear/disappear
- Recommendations change

---

## 🎯 Four Datasets Ready

All files are in: `D:\video\AHADU PULSE\`

| File | Date | Scenario | Upload | Verify |
|------|------|----------|--------|--------|
| **DATASET_1_INITIAL.xlsx** | Jun 22 | Baseline | 1st | All pages update |
| **DATASET_2_WEEK2.xlsx** | Jun 29 | Changes | 2nd | Data refreshes |
| **DATASET_3_WEEK3.xlsx** | Jul 6 | Trends | 3rd | Scores change |
| **DATASET_4_WEEK4.xlsx** | Jul 13 | Stable | 4th | Final status |

---

## 📈 Expected Score Changes

### DATASET 1: INITIAL BASELINE (June 22)

```
MOBILE_01:  Score 90  Tier: HIGH ✅
CARD_01:    Score 70  Tier: MEDIUM ⚠️
ATM_01:     Score 42  Tier: LOW 🚨

Rankings:
  #1 MOBILE_01 (90)
  #2 CARD_01 (70)
  #3 ATM_01 (42)
```

**Dashboard Shows:**
- 3 products displayed
- Average score: 67.3
- 1 HIGH, 1 MEDIUM, 1 LOW

**Alerts Generated:**
- MOBILE: 0 alerts
- CARD: 3 warnings
- ATM: 6+ critical

**Recommendations Generated:**
- MOBILE: 1 (maintain)
- CARD: 4 (improvements)
- ATM: 6+ (urgent)

---

### DATASET 2: WEEK 2 CHANGES (June 29)

**Data Changes:**
- MOBILE: +18K active users, -0.45K complaints, +0.1 CSAT
- CARD: +2K active users, +0.05 CSAT, stable metrics
- ATM: -10K active users, +35 complaints, -0.25 CSAT

```
MOBILE_01:  Score 92+ Tier: HIGH ✅ (IMPROVED ↑)
CARD_01:    Score 70  Tier: MEDIUM ⚠️ (STABLE →)
ATM_01:     Score 40- Tier: LOW 🚨 (WORSENED ↓)

Rankings:
  #1 MOBILE_01 (92+)
  #2 CARD_01 (70)
  #3 ATM_01 (40-)
```

**What Changes on Dashboard:**
- ✓ Average score updates (now higher)
- ✓ MOBILE score increases (90 → 92+)
- ✓ ATM score decreases (42 → 40-)
- ✓ New alerts generated for ATM
- ✓ New recommendations based on new status

**Scores Section Shows:**
- MOBILE_01: 92+ (higher than before)
- CARD_01: 70 (same as before)
- ATM_01: 40- (lower than before)
- Each shows "Previous: 90", "Previous: 70", "Previous: 42"
- Score changes displayed: ↑+2, →0, ↓-2

**Alerts Section Updates:**
- MOBILE: May go to 0 alerts (improving)
- CARD: Still 3 warnings (unchanged)
- ATM: Now 8+ critical alerts (increasing)

**Recommendations Section:**
- MOBILE: "Continue current performance" (1 rec)
- CARD: "Address emerging issues" (4 recs)
- ATM: "Escalate remediation efforts" (8+ recs)

---

### DATASET 3: WEEK 3 ACCELERATION (July 6)

**Data Changes:**
- MOBILE: +22K more active users, -7 complaints, +0.05 CSAT (96.9% success!)
- CARD: -6K active users, +17 complaints, -0.15 CSAT (declining)
- ATM: -18K more active users (crisis), +90 complaints, -0.45 CSAT, 72% success

```
MOBILE_01:  Score 94+ Tier: HIGH ✅ (EXCELLENT ↑↑)
CARD_01:    Score 68- Tier: MEDIUM ⚠️ (DECLINING ↓)
ATM_01:     Score 35- Tier: LOW 🚨 (CRISIS ↓↓)

Rankings:
  #1 MOBILE_01 (94+)
  #2 CARD_01 (68-)
  #3 ATM_01 (35-)
```

**Dashboard Reflects:**
- MOBILE leading strongly
- CARD dropping in performance
- ATM in critical condition

**Scores Page Shows:**
- MOBILE_01: 94+ (up from 92+) ✓ Improving trend
- CARD_01: 68- (down from 70) ✗ Declining trend  
- ATM_01: 35- (down from 40-) ✗✗ Critical decline
- Score components breakdown for each
- Trend arrows clearly visible

**Alerts Page Escalation:**
- MOBILE: 0 alerts (optimal, no changes)
- CARD: 5+ alerts now (was 3, added 2 new)
- ATM: 8+ critical alerts (worse than before)

**Rankings Update:**
- MOBILE continues at #1 (but with higher score)
- CARD drops further
- ATM continues at #3 (but with lower score)

**Recommendations Changes:**
- MOBILE: 1 "Sustain momentum" (slightly different message)
- CARD: 6 recommendations (more than before)
- ATM: 8+ "URGENT: Crisis response" (escalated)

---

### DATASET 4: WEEK 4 STABILIZING (July 13)

**Data Changes:**
- MOBILE: +25K more active users, 98% success, -7 complaints, 4.9 CSAT
- CARD: -13K active users total, 90% success, +20 complaints, 3.55 CSAT
- ATM: -6.5K more active users, 72.2% success, +70 complaints, 1.95 CSAT

```
MOBILE_01:  Score 96+ Tier: HIGH ✅✅ (PEAK ↑)
CARD_01:    Score 65- Tier: MEDIUM ⚠️ (POOR ↓)
ATM_01:     Score 30  Tier: LOW 🚨 (CRITICAL ↓)

Rankings:
  #1 MOBILE_01 (96+)
  #2 CARD_01 (65-)
  #3 ATM_01 (30)
```

**Final Dashboard Status:**
- MOBILE: Peak performance (96+)
- CARD: Deteriorating (65-)
- ATM: Critical state (30)

**Scores Show Progression:**
- MOBILE_01: 96+ (progression: 90 → 92 → 94 → 96) ✓
- CARD_01: 65- (progression: 70 → 70 → 68 → 65) ✗
- ATM_01: 30 (progression: 42 → 40 → 35 → 30) ✗✗

**Final Alerts:**
- MOBILE: 0 alerts (continues optimal)
- CARD: 5-6 alerts (plateauing)
- ATM: 10+ critical alerts (maximum)

**Final Recommendations:**
- MOBILE: 1 "Peak performance achieved" (highest recognition)
- CARD: 7+ recommendations (now recommending major changes)
- ATM: 10+ recommendations (critical overhaul needed)

---

## 🚀 How to Test (Step by Step)

### Upload 1: DATASET_1_INITIAL.xlsx

1. **Open Settings Page**
   - URL: http://localhost:3000/dashboard/settings

2. **Upload First Dataset**
   - Click "Upload KPI Data"
   - Select: `DATASET_1_INITIAL.xlsx`
   - Wait for completion (should see "3 rows imported")

3. **Verify Initial Dashboard**
   - Go to Dashboard page
   - Should show: Average score 67.3, 1 HIGH + 1 MEDIUM + 1 LOW
   - Go to Rankings: MOBILE #1, CARD #2, ATM #3
   - Go to Scores: 90, 70, 42
   - Go to Alerts: 0/3/6+ pattern
   - Go to Recommendations: 1/4/6+ pattern

4. **Screenshot/Note baseline values**

---

### Upload 2: DATASET_2_WEEK2.xlsx

1. **Go to Settings Page**
   - Same URL

2. **Upload Second Dataset**
   - Click "Upload KPI Data"
   - Select: `DATASET_2_WEEK2.xlsx`
   - System replaces old data with new data
   - Wait for completion

3. **Verify Data Changed**
   - Dashboard page: Average score changed
   - Rankings page: Scores updated (90→92+, 70→70, 42→40-)
   - Scores page: Shows previous scores AND new scores
   - Alerts page: New alerts for ATM
   - Recommendations page: Updated recommendations

4. **Check Score Changes**
   - MOBILE: Should increase (90 → 92+)
   - CARD: Should stay similar (~70)
   - ATM: Should decrease (42 → 40-)

5. **Verify Trend Indicators**
   - Each score should show: Previous score + current score + change arrow

---

### Upload 3: DATASET_3_WEEK3.xlsx

1. **Go to Settings Page**

2. **Upload Third Dataset**
   - Select: `DATASET_3_WEEK3.xlsx`
   - Wait for processing

3. **Observe Accelerating Trends**
   - MOBILE: Score continues upward (92+ → 94+)
   - CARD: Score continues downward (70 → 68-)
   - ATM: Score drops more (40- → 35-)

4. **Check Dashboard Changes**
   - Average score continues changing
   - Rankings remain same order but with different scores
   - Alerts increase for CARD and ATM
   - Recommendations become more urgent

5. **Verify Multiple Changes Visible**
   - Rankings page: Clearly shows 3 weeks of progression
   - Scores page: Shows trend over time
   - Alerts: More alerts for declining products

---

### Upload 4: DATASET_4_WEEK4.xlsx

1. **Go to Settings Page**

2. **Upload Fourth Dataset**
   - Select: `DATASET_4_WEEK4.xlsx`
   - This is the final status update

3. **Review Final Status**
   - MOBILE: Peak (96+)
   - CARD: Poor (65-)
   - ATM: Critical (30)

4. **Verify Complete Progression**
   - All pages should show consistent data
   - Trends should be clear across all 4 uploads
   - Rankings unchanged but scores very different
   - Alerts highest for ATM, none for MOBILE

---

## ✅ Verification Checklist

### After Each Upload:

**Dashboard Page:**
- [ ] Average score updated
- [ ] All 3 products displayed
- [ ] Tier badges correct
- [ ] Data reflects current period

**Rankings Page:**
- [ ] Products ranked by current score
- [ ] Scores match current dataset
- [ ] Order might change (if scores change significantly)

**Scores Page:**
- [ ] Each product shows current score
- [ ] Previous score shown
- [ ] Score change visible (↑/→/↓)
- [ ] Breakdown components updated

**Alerts Page:**
- [ ] New alerts generated based on new data
- [ ] Old alerts from previous upload gone
- [ ] Alert severity correct
- [ ] Descriptions match new situation

**Recommendations Page:**
- [ ] New recommendations generated
- [ ] Recommendations match new status
- [ ] Priority levels appropriate
- [ ] Action items specific to new data

**Consistency:**
- [ ] All pages show data from same period
- [ ] No mix of old and new data
- [ ] Product metrics consistent across pages

---

## 🔍 Specific Things to Watch

### Score Progression to Observe:

**MOBILE_01:**
```
Upload 1: 90  (baseline excellent)
Upload 2: 92+ (improving)
Upload 3: 94+ (very good)
Upload 4: 96+ (peak)
```
✓ Steady upward trend

**CARD_01:**
```
Upload 1: 70  (medium)
Upload 2: 70  (stable)
Upload 3: 68- (declining)
Upload 4: 65- (poor)
```
✗ Gradual decline

**ATM_01:**
```
Upload 1: 42  (low crisis)
Upload 2: 40- (worsening)
Upload 3: 35- (worse crisis)
Upload 4: 30  (critical)
```
✗✗ Rapid deterioration

---

## 🎓 What You're Testing

With these 4 uploads, you verify:

1. **Data Replacement**
   - ✓ Each upload completely replaces previous data
   - ✓ No mixing of old and new data

2. **Score Recalculation**
   - ✓ ML models recalculate for each new dataset
   - ✓ Scores change based on new metrics
   - ✓ Trends are visible over time

3. **Ranking Updates**
   - ✓ Rankings update based on new scores
   - ✓ Products can move up/down (if scores change significantly)

4. **Alert Generation**
   - ✓ Alerts generated based on new metrics
   - ✓ Alerts disappear when conditions improve
   - ✓ New alerts appear when conditions worsen

5. **Recommendation Regeneration**
   - ✓ Recommendations update for each new status
   - ✓ Recommendations become more/less urgent
   - ✓ Action items are specific to new data

6. **Dashboard Refresh**
   - ✓ All pages automatically update
   - ✓ No manual refresh needed (auto-refreshes)
   - ✓ Consistent data across all pages

---

## 📊 Sample Screenshots (What You Should See)

### Upload 1 - Initial Dashboard
```
Dashboard: 3 Products
├─ MOBILE_01: Score 90 (HIGH) - Optimal
├─ CARD_01: Score 70 (MEDIUM) - Warning
└─ ATM_01: Score 42 (LOW) - Critical

Average: 67.3
```

### Upload 4 - Final Dashboard
```
Dashboard: 3 Products
├─ MOBILE_01: Score 96+ (HIGH) - Excellent
├─ CARD_01: Score 65- (MEDIUM) - Poor
└─ ATM_01: Score 30 (LOW) - Critical

Average: 63.7 (Down from 67.3)
```

Note: Average goes down because ATM deteriorates significantly.

---

## 🐛 Troubleshooting

**Scores don't change after upload:**
- Refresh the page (Ctrl+R)
- Check backend logs for processing errors
- Verify database updated with new data

**Old data still showing:**
- Click "Run Feature Engineering" in Settings
- This reprocesses all data
- Or upload next dataset

**Alerts not updating:**
- Wait 30 seconds for processing
- Refresh the page
- Check database for alert records

**Rankings don't change:**
- This is OK if scores are similar
- They will change when scores differ significantly
- In this test, MOBILE stays #1 (score keeps increasing)

---

## 🎯 Expected Final Results

After uploading all 4 datasets:

| Metric | MOBILE | CARD | ATM | Status |
|--------|--------|------|-----|--------|
| Score | 96+ | 65- | 30 | ✓ All changed |
| Tier | HIGH | MEDIUM | LOW | ✓ Stable |
| Rank | #1 | #2 | #3 | ✓ Stable |
| Alerts | 0 | 5-6 | 10+ | ✓ Escalating |
| Recommendations | 1 | 7+ | 10+ | ✓ Urgency up |
| Trend | ↑↑ | ↓ | ↓↓ | ✓ Clear trends |

---

## 📝 Testing Log

Use this to document your test results:

```
UPLOAD 1 - DATASET_1_INITIAL.xlsx
Date: _______  Time: _______
Dashboard shows: Average 67.3 ✓/✗
Rankings: 1-MOBILE, 2-CARD, 3-ATM ✓/✗
Alerts generated: 0/3/6+ ✓/✗
Notes: ___________________________

UPLOAD 2 - DATASET_2_WEEK2.xlsx
Date: _______  Time: _______
Scores changed: 90→92+, 70→70, 42→40- ✓/✗
Previous scores shown: ✓/✗
Trend arrows visible: ✓/✗
Notes: ___________________________

UPLOAD 3 - DATASET_3_WEEK3.xlsx
Date: _______  Time: _______
Scores changed: 92+→94+, 70→68-, 40-→35- ✓/✗
Alerts increased: ✓/✗
Recommendations updated: ✓/✗
Notes: ___________________________

UPLOAD 4 - DATASET_4_WEEK4.xlsx
Date: _______  Time: _______
Final scores: 96+, 65-, 30 ✓/✗
Final alerts: 0/5-6/10+ ✓/✗
All pages refreshed: ✓/✗
Notes: ___________________________
```

---

## 🎉 Success Criteria

Your system is working correctly if:

✅ Each upload completely replaces previous data
✅ Scores change with each upload
✅ Rankings update based on new scores
✅ Alerts are regenerated for each period
✅ Recommendations update for each status
✅ Dashboard automatically refreshes all pages
✅ No manual intervention needed between uploads
✅ Data is consistent across all pages
✅ Previous scores visible (for trend comparison)
✅ All 4 uploads complete without errors

---

**Ready to test? Start with DATASET_1_INITIAL.xlsx**

Upload all 4 in order to see the complete progression!
