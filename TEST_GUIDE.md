# AHADU PULSE — Test Dataset Guide

## 📊 Test Dataset Created: `TEST_DATASET_3_PRODUCTS.xlsx`

This dataset contains **3 products with contrasting performance levels** to clearly demonstrate scores, ranks, alerts, and recommendations.

---

## 🎯 Three Test Products

### 1️⃣ MOBILE_01 — HIGH PERFORMER ✅ 
**Expected Score: 88-92 | Tier: HIGH**

#### KPI Metrics:
- **Engagement**: 680K active users (80% of 850K total) — Excellent
- **Transaction Success**: 96% (3,360K successful / 3,500K total)
- **Revenue**: ETB 85M total, ETB 5.1M fees
- **Uptime**: 99.8% (only 5 hours downtime)
- **API Performance**: 250ms avg response, 0.5% error rate
- **Customer Satisfaction**: CSAT 4.7/5.0 — Highest
- **Fraud/Security**: Only 2 fraud incidents, 0 security incidents
- **Complaints**: 45 total, 42 resolved (93% resolution)

#### Expected Alerts:
- ✅ **No critical alerts** — Optimal performance
- Status: Green

#### Expected Recommendations:
- Maintain current operational standards
- Share best practices with other products
- Continue investment in this channel

---

### 2️⃣ CARD_01 — MEDIUM PERFORMER ⚠️
**Expected Score: 65-75 | Tier: MEDIUM**

#### KPI Metrics:
- **Engagement**: 319K active users (58% of 550K total) — Declining
- **Transaction Success**: 90% (1,620K / 1,800K) — Below target
- **Revenue**: ETB 50M total, ETB 2.5M fees
- **Uptime**: 97.5% (18 hours downtime) — Acceptable but declining
- **API Performance**: 420ms avg response, 2.2% error rate — Moderate
- **Customer Satisfaction**: CSAT 3.8/5.0 — Needs improvement
- **Fraud/Security**: 8 fraud incidents, 1 security incident
- **Complaints**: 120 total, 96 resolved (80% resolution)

#### Expected Alerts:
- ⚠️ **Warning: Uptime below 98%**
- ⚠️ **Warning: API error rate above 2%**
- ⚠️ **Warning: CSAT declining — customer satisfaction < 4.0**
- Status: Yellow

#### Expected Recommendations:
- Investigate API performance degradation
- Implement infrastructure improvements
- Review and address complaint drivers
- Enhance customer support processes

---

### 3️⃣ ATM_01 — LOW PERFORMER 🚨 CRITICAL
**Expected Score: 35-45 | Tier: LOW**

#### KPI Metrics:
- **Engagement**: 128K active users (40% of 320K) — Very low, high churn
- **Churned Users**: 12.8K (4% of base) — Significant attrition
- **Transaction Success**: 80% (680K / 850K) — Concerning
- **Revenue**: ETB 21M total, ETB 1.05M fees — Lowest
- **Uptime**: 94.2% (136 hours downtime) — Poor
- **API Performance**: 850ms response, 6.8% error rate — Slow & unreliable
- **Customer Satisfaction**: CSAT 2.9/5.0 — Lowest satisfaction
- **Fraud/Security**: 24 fraud incidents, 3 security incidents — Highest risk
- **Complaints**: 385 total, 270 resolved (70% resolution) — Many unresolved

#### Expected Alerts:
- 🚨 **CRITICAL: Uptime < 95% — Service degradation**
- 🚨 **CRITICAL: API failure rate > 5%**
- 🚨 **CRITICAL: Score dropped below 50**
- ⚠️ **WARNING: High fraud activity — 24 incidents**
- ⚠️ **WARNING: Customer satisfaction critical — CSAT 2.9**
- ⚠️ **WARNING: Unresolved complaints — 115 pending**
- Status: Red

#### Expected Recommendations:
- **URGENT**: Investigate and resolve ATM hardware issues
- **URGENT**: Implement emergency infrastructure maintenance plan
- Increase monitoring and incident response capabilities
- Deploy additional resources for customer support
- Conduct security audit — address fraud patterns
- Develop recovery and remediation strategy

---

## 📋 How to Use This Dataset

### Step 1: Upload the File
1. Go to **Settings page** in AHADU PULSE
2. Click **"Upload KPI Data"**
3. Select **`TEST_DATASET_3_PRODUCTS.xlsx`**
4. Watch the automatic processing:
   - ✓ Reading file
   - ✓ Validating columns & values
   - ✓ Importing to database
   - ✓ Computing features
   - ✓ Scoring products
   - ✓ Generating alerts & recommendations

### Step 2: Verify Results in Dashboard

#### 📊 Dashboard Page
- Check the overview card with 3 products
- HIGH tier should show green
- MEDIUM tier should show yellow
- LOW tier should show red

#### 🏆 Rankings Page
1. **MOBILE_01** — Rank #1 (Score: ~90)
2. **CARD_01** — Rank #2 (Score: ~70)
3. **ATM_01** — Rank #3 (Score: ~42)

#### 💯 Scores Page
- MOBILE_01: 88-92 (HIGH) ✅
- CARD_01: 65-75 (MEDIUM) ⚠️
- ATM_01: 35-45 (LOW) 🚨

Each product should show:
- Performance Score (0-100)
- Tier (HIGH/MEDIUM/LOW)
- Previous score (if available)
- Score change

#### 🚨 Alerts Page
**HIGH severity (MOBILE_01)**
- None expected (optimal)

**MEDIUM severity (CARD_01)**
- Uptime Warning
- API Error Rate Warning
- CSAT Declining

**CRITICAL severity (ATM_01)**
- Uptime Critical (94.2% < 95% threshold)
- API Failure Critical (6.8% > 5% threshold)
- Score Critical (42 < 50 minimum)
- Fraud Activity Alert
- Customer Satisfaction Critical
- Unresolved Complaints Alert

#### 💡 Recommendations Page
**MOBILE_01** (1 recommendation)
- Maintain current operational standards

**CARD_01** (4 recommendations)
- Investigate API performance
- Improve infrastructure
- Review complaint drivers
- Enhance customer support

**ATM_01** (6 recommendations)
- Urgent: Fix ATM hardware
- Urgent: Maintenance plan
- Increase monitoring
- Add support resources
- Security audit
- Recovery strategy

---

## ✅ Verification Checklist

- [ ] Upload completes successfully with 3 rows imported
- [ ] Features: 3 feature records computed
- [ ] Scores: All 3 products scored
- [ ] Alerts: ATM_01 has 6+ alerts (CRITICAL severity)
- [ ] Rankings: Products ranked by score (90 > 70 > 42)
- [ ] Recommendations: At least 11 total recommendations generated

---

## 📝 Excel File Sheets

The file contains **3 sheets** for reference:

1. **Upload_Ready** — Actual data to upload (color-coded)
   - Green: MOBILE_01 (HIGH)
   - Yellow: CARD_01 (MEDIUM)  
   - Red: ATM_01 (LOW)

2. **Legend** — Scenario descriptions and expected scores

3. **Expected_Outputs** — What the system should calculate

---

## 🔍 Understanding the Scores

The ML models calculate performance score based on 12 engineered features:

### Features Used (Examples):
- **active_user_rate** — % of users engaging (60-100% range)
- **failed_txn_rate** — Transaction failure % (1-20% range)
- **revenue_per_txn** — Revenue efficiency
- **downtime_impact_score** — Uptime reliability
- **complaint_growth_rate** — Trend in complaints
- **api_error_rate** — System reliability
- **csat_score** — Customer satisfaction (1-5 scale)

### Why Scores Differ:

**MOBILE_01 = 90**: All metrics excellent (high engagement, high success rate, high uptime, high CSAT)

**CARD_01 = 70**: Mixed metrics (moderate engagement, lower uptime, declining satisfaction)

**ATM_01 = 42**: Poor metrics (low engagement, low success rate, poor uptime, very low CSAT, high fraud)

---

## 🎓 Learning Outcomes

After uploading this test dataset, you'll understand:

1. ✅ How scores are calculated from raw KPIs
2. ✅ How tiers (HIGH/MEDIUM/LOW) are assigned
3. ✅ How alerts are triggered based on thresholds
4. ✅ How recommendations are generated
5. ✅ How the ranking system works
6. ✅ The relationship between KPIs and performance

---

## 📞 Support

If you need to troubleshoot:

1. Check the backend logs for any errors
2. Verify all 3 products appear in the database
3. Check that alerts were generated with correct severity
4. Verify recommendations have detailed action items
5. Confirm rankings are sorted by score (descending)

---

**Created**: June 22, 2026  
**Purpose**: Comprehensive system testing with clear, observable outputs
