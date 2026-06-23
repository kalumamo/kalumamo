# AHADU PULSE — Expected Dashboard Outputs After Upload

After uploading the test dataset, here's exactly what you should see on each dashboard page.

---

## 📊 DASHBOARD HOME PAGE

```
┌─────────────────────────────────────────────────────────────────┐
│                    AHADU PULSE DASHBOARD                        │
│                        June 22, 2026                            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ PERFORMANCE OVERVIEW                                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Total Products: 3      Average Score: 71.7     Date: 2026-06-22│
│                                                                  │
│  HIGH (1)    MEDIUM (1)    LOW (1)                             │
│  ✓ MOBILE   ⚠ CARD       🚨 ATM                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ PRODUCT SUMMARY CARDS                                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   MOBILE_01     │  │    CARD_01      │  │    ATM_01       │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │ Score: 90       │  │ Score: 70       │  │ Score: 42       │ │
│  │ Tier: HIGH ✓    │  │ Tier: MEDIUM ⚠  │  │ Tier: LOW 🚨   │ │
│  │ Rank: #1        │  │ Rank: #2        │  │ Rank: #3        │ │
│  │ Status: Optimal │  │ Status: Warning │  │ Status: Critical│ │
│  │                 │  │                 │  │                 │ │
│  │ ↑ 0 alerts      │  │ ↑ 3 warnings    │  │ ↑ 6+ critical   │ │
│  │ → 1 recommend   │  │ → 4 recommends  │  │ → 6+ recommends │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│   (Green bg)            (Yellow bg)          (Red bg)           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🏆 RANKINGS PAGE

```
┌──────────────────────────────────────────────────────────────────┐
│ PRODUCT RANKINGS (Sorted by Performance Score)                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ RANK  PRODUCT        SCORE   TIER      STATUS         ALERTS    │
│ ────  ─────────────  ─────   ────────  ─────────────  ────────  │
│  #1   MOBILE_01       90      HIGH ✅  Optimal         0        │
│  #2   CARD_01         70      MEDIUM   Warning         3        │
│  #3   ATM_01          42      LOW 🚨   Critical        6+       │
│                                                                  │
│ Score Distribution:                                             │
│ ╭────────────────────────────────────────────────────────────╮ │
│ │ MOBILE_01  ████████████████████████ 90/100                │ │
│ │ CARD_01    ██████████████ 70/100                          │ │
│ │ ATM_01     ██████ 42/100                                  │ │
│ ╰────────────────────────────────────────────────────────────╯ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 💯 SCORES PAGE

```
┌──────────────────────────────────────────────────────────────────┐
│ PRODUCT SCORES & PERFORMANCE TIERS                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ MOBILE_01 — HIGH TIER ✅                                   │ │
│ ├─────────────────────────────────────────────────────────────┤ │
│ │                                                             │ │
│ │  Performance Score:         90 / 100                        │ │
│ │  Status:                    Excellent ✓                    │ │
│ │  Previous Score:            — (first upload)               │ │
│ │  Change:                    — N/A                          │ │
│ │                                                             │ │
│ │  Score Breakdown:                                           │ │
│ │  ├─ Active User Rate:       80% (Weight: 15%)             │ │
│ │  ├─ Transaction Success:    96% (Weight: 25%)             │ │
│ │  ├─ Uptime Impact:          99.8% (Weight: 20%)           │ │
│ │  ├─ API Reliability:        99.5% (Weight: 15%)           │ │
│ │  ├─ Customer Satisfaction:  94% (4.7/5.0, Weight: 15%)   │ │
│ │  └─ Operational Health:     100% (Weight: 10%)            │ │
│ │                                                             │ │
│ │  Total Alerts:          0 (Optimal)                        │ │
│ │  Recommendations:       1 (Maintain performance)           │ │
│ │                                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ CARD_01 — MEDIUM TIER ⚠️                                   │ │
│ ├─────────────────────────────────────────────────────────────┤ │
│ │                                                             │ │
│ │  Performance Score:         70 / 100                        │ │
│ │  Status:                    Requires Attention ⚠           │ │
│ │  Previous Score:            — (first upload)               │ │
│ │  Change:                    — N/A                          │ │
│ │                                                             │ │
│ │  Score Breakdown:                                           │ │
│ │  ├─ Active User Rate:       58% (Weight: 15%) ⚠            │ │
│ │  ├─ Transaction Success:    90% (Weight: 25%)              │ │
│ │  ├─ Uptime Impact:          97.5% (Weight: 20%) ⚠          │ │
│ │  ├─ API Reliability:        97.8% (Weight: 15%) ⚠          │ │
│ │  ├─ Customer Satisfaction:  76% (3.8/5.0, Weight: 15%) ⚠  │ │
│ │  └─ Operational Health:     80% (Weight: 10%)              │ │
│ │                                                             │ │
│ │  Total Alerts:          3 (Warnings)                        │ │
│ │  Recommendations:       4 (Infrastructure improvements)    │ │
│ │                                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ATM_01 — LOW TIER 🚨 CRITICAL                             │ │
│ ├─────────────────────────────────────────────────────────────┤ │
│ │                                                             │ │
│ │  Performance Score:         42 / 100                        │ │
│ │  Status:                    Critical ⛔                     │ │
│ │  Previous Score:            — (first upload)               │ │
│ │  Change:                    — N/A                          │ │
│ │                                                             │ │
│ │  Score Breakdown:                                           │ │
│ │  ├─ Active User Rate:       40% (Weight: 15%) 🚨           │ │
│ │  ├─ Transaction Success:    80% (Weight: 25%) 🚨           │ │
│ │  ├─ Uptime Impact:          94.2% (Weight: 20%) 🚨         │ │
│ │  ├─ API Reliability:        93.2% (Weight: 15%) 🚨         │ │
│ │  ├─ Customer Satisfaction:  58% (2.9/5.0, Weight: 15%) 🚨 │ │
│ │  └─ Operational Health:     70% (Weight: 10%) 🚨           │ │
│ │                                                             │ │
│ │  Total Alerts:          6+ (Critical severity)              │ │
│ │  Recommendations:       6+ (Urgent action required)         │ │
│ │                                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚨 ALERTS PAGE

```
┌──────────────────────────────────────────────────────────────────┐
│ SYSTEM ALERTS (Sorted by Severity & Date)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ CRITICAL (6 alerts for ATM_01)                                  │
│ ───────────────────────────────────────────────────────────────  │
│ 🚨 [CRITICAL] Uptime Below 95% Threshold                        │
│    Product: ATM_01 | Period: 2026-06-22 | Time: 12:15 UTC      │
│    Current: 94.2% | Threshold: 95.0% | Gap: -0.8%              │
│    Impact: Service reliability compromised                      │
│    Action: Investigate infrastructure issues immediately        │
│                                                                  │
│ 🚨 [CRITICAL] API Failure Rate > 5%                            │
│    Product: ATM_01 | Period: 2026-06-22 | Time: 12:15 UTC      │
│    Current: 6.8% | Threshold: 5.0% | Gap: +1.8%                │
│    Impact: System reliability degraded                          │
│    Action: Review and fix API errors, scale infrastructure      │
│                                                                  │
│ 🚨 [CRITICAL] Performance Score Below Minimum                   │
│    Product: ATM_01 | Period: 2026-06-22 | Time: 12:15 UTC      │
│    Score: 42 | Minimum: 50 | Gap: -8 points                    │
│    Impact: Product below acceptable performance levels          │
│    Action: Implement comprehensive improvement plan             │
│                                                                  │
│ 🚨 [CRITICAL] High Fraud Activity Detected                     │
│    Product: ATM_01 | Period: 2026-06-22 | Time: 12:15 UTC      │
│    Incidents: 24 | Previous: — | Trend: New spike              │
│    Impact: Security and financial risk                          │
│    Action: Enhanced monitoring and fraud investigation          │
│                                                                  │
│ 🚨 [CRITICAL] Customer Satisfaction Critical (< 3.0)          │
│    Product: ATM_01 | Period: 2026-06-22 | Time: 12:15 UTC      │
│    CSAT: 2.9/5.0 | Target: 4.0+ | Gap: -1.1 points             │
│    Impact: Customer churn risk, brand reputation                │
│    Action: Immediate customer support review needed             │
│                                                                  │
│ 🚨 [CRITICAL] Unresolved Complaint Spike                       │
│    Product: ATM_01 | Period: 2026-06-22 | Time: 12:15 UTC      │
│    Unresolved: 115 | Total: 385 | Resolution: 70%              │
│    Impact: Customer satisfaction and retention at risk          │
│    Action: Escalate support team, add resources                 │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ WARNING (3 alerts for CARD_01)                                  │
│ ───────────────────────────────────────────────────────────────  │
│ ⚠️  [WARNING] Uptime Below 98% Threshold                        │
│    Product: CARD_01 | Period: 2026-06-22 | Time: 12:15 UTC     │
│    Current: 97.5% | Threshold: 98.0% | Gap: -0.5%              │
│    Recommended Action: Monitor and plan maintenance             │
│                                                                  │
│ ⚠️  [WARNING] API Error Rate > 2%                              │
│    Product: CARD_01 | Period: 2026-06-22 | Time: 12:15 UTC     │
│    Current: 2.2% | Threshold: 2.0% | Gap: +0.2%                │
│    Recommended Action: Investigate API issues                   │
│                                                                  │
│ ⚠️  [WARNING] Customer Satisfaction Below Target (< 4.0)       │
│    Product: CARD_01 | Period: 2026-06-22 | Time: 12:15 UTC     │
│    CSAT: 3.8/5.0 | Target: 4.0+ | Gap: -0.2 points             │
│    Recommended Action: Review feedback and improve services     │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ OK (0 alerts for MOBILE_01)                                     │
│ ───────────────────────────────────────────────────────────────  │
│ ✅ [OK] All Metrics Normal - Optimal Performance               │
│    Product: MOBILE_01 | Status: Green                           │
│    All KPIs within acceptable ranges                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 💡 RECOMMENDATIONS PAGE

```
┌──────────────────────────────────────────────────────────────────┐
│ AI-GENERATED RECOMMENDATIONS                                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ MOBILE_01 — 1 Recommendation (Maintenance)                      │
│ ─────────────────────────────────────────────────────────────    │
│ ✅ Maintain Current Operational Excellence                      │
│    Category: Operations | Priority: Low | Target Date: —        │
│    Description:                                                 │
│    Your product is performing at optimal levels across all KPIs.│
│    Continue current operational practices and infrastructure    │
│    investments to maintain this performance level.              │
│                                                                  │
│    Action Items:                                                │
│    □ Share best practices with CARD_01 and ATM_01 teams        │
│    □ Document current architecture and processes               │
│    □ Plan quarterly optimization reviews                       │
│                                                                  │
│    Expected Impact: Sustained HIGH tier performance             │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ CARD_01 — 4 Recommendations (Improvements Needed)                │
│ ─────────────────────────────────────────────────────────────    │
│ ⚠️  1. Investigate API Performance Degradation                  │
│    Category: Infrastructure | Priority: High | Target: 1 week   │
│    Description:                                                 │
│    API error rate (2.2%) and response time (420ms) are above    │
│    acceptable thresholds. This impacts user experience and can  │
│    contribute to declining transaction success rates.           │
│                                                                  │
│    Action Items:                                                │
│    □ Analyze API logs for error patterns                        │
│    □ Review infrastructure capacity                             │
│    □ Implement caching or load balancing                        │
│    □ Set up improved monitoring                                 │
│                                                                  │
│    Expected Impact: Reduce API errors to < 1%                   │
│                                                                  │
│ ⚠️  2. Improve Infrastructure Reliability                      │
│    Category: Operations | Priority: High | Target: 2 weeks      │
│    Description:                                                 │
│    Uptime has dropped to 97.5% (18 hours downtime), indicating │
│    infrastructure stability issues. This directly impacts       │
│    customer satisfaction and revenue.                           │
│                                                                  │
│    Action Items:                                                │
│    □ Conduct infrastructure audit                              │
│    □ Upgrade underperforming components                         │
│    □ Implement redundancy                                       │
│    □ Test failover procedures                                   │
│                                                                  │
│    Expected Impact: Increase uptime to > 99%                    │
│                                                                  │
│ ⚠️  3. Address Customer Complaint Drivers                      │
│    Category: Customer Service | Priority: Medium | Target: 1mo  │
│    Description:                                                 │
│    120 complaints with only 80% resolution rate. Understanding │
│    root causes will help improve CSAT (currently 3.8/5.0).     │
│                                                                  │
│    Action Items:                                                │
│    □ Analyze complaint categories                              │
│    □ Identify systemic issues                                  │
│    □ Implement targeted fixes                                  │
│    □ Improve complaint resolution process                      │
│                                                                  │
│    Expected Impact: Reduce complaints by 30%, increase          │
│                    resolution to 95%                             │
│                                                                  │
│ ⚠️  4. Enhance Customer Support Capabilities                   │
│    Category: Customer Service | Priority: Medium | Target: 2wks │
│    Description:                                                 │
│    Customer satisfaction (3.8/5.0) is below target. Improving  │
│    support responsiveness and quality will improve retention.   │
│                                                                  │
│    Action Items:                                                │
│    □ Assess current support team capacity                      │
│    □ Implement ticket tracking system                          │
│    □ Provide support team training                             │
│    □ Set up customer feedback loop                             │
│                                                                  │
│    Expected Impact: Increase CSAT to > 4.2/5.0                 │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ ATM_01 — 6+ Recommendations (URGENT - Crisis Mode)               │
│ ─────────────────────────────────────────────────────────────    │
│ 🚨 1. URGENT: Resolve ATM Hardware Failures                    │
│    Category: Operations | Priority: CRITICAL | Target: 3 days   │
│    Description:                                                 │
│    The severe downtime (136 hours, 94.2% uptime) indicates     │
│    critical hardware issues. This must be resolved immediately. │
│                                                                  │
│    Action Items:                                                │
│    □ Dispatch technical team to ATM locations                  │
│    □ Identify failed components (power, network, drive)        │
│    □ Repair/replace hardware                                   │
│    □ Test all ATMs before returning to service                 │
│                                                                  │
│    Expected Impact: Restore uptime to > 97% within 72 hours    │
│                                                                  │
│ 🚨 2. URGENT: Implement Emergency Infrastructure Plan           │
│    Category: Operations | Priority: CRITICAL | Target: 1 week   │
│    Description:                                                 │
│    Current infrastructure is failing (80% transaction success,  │
│    94.2% uptime). A comprehensive maintenance and upgrade plan  │
│    is required immediately.                                     │
│                                                                  │
│    Action Items:                                                │
│    □ Comprehensive infrastructure audit                         │
│    □ Identify critical failure points                          │
│    □ Develop detailed remediation roadmap                      │
│    □ Allocate resources and budget                             │
│    □ Establish weekly progress reviews                         │
│                                                                  │
│    Expected Impact: Stabilize infrastructure, prevent further   │
│                    degradation                                   │
│                                                                  │
│ 🚨 3. Increase Monitoring and Incident Response                │
│    Category: Operations | Priority: CRITICAL | Target: ASAP     │
│    Description:                                                 │
│    With only 94.2% uptime, the response to incidents must be   │
│    immediate and automated where possible.                      │
│                                                                  │
│    Action Items:                                                │
│    □ Deploy real-time monitoring on all ATMs                   │
│    □ Set up automated alerts for failures                      │
│    □ Establish on-call incident response team                  │
│    □ Create escalation procedures                              │
│                                                                  │
│    Expected Impact: Reduce mean time to detect/resolve (MTTR)  │
│                    from current ~hours to minutes               │
│                                                                  │
│ 🚨 4. Add Customer Support Resources                           │
│    Category: Customer Service | Priority: HIGH | Target: 1 week │
│    Description:                                                 │
│    With 385 complaints (270 unresolved) and CSAT 2.9/5.0,     │
│    customers need immediate support attention.                  │
│                                                                  │
│    Action Items:                                                │
│    □ Hire temporary support staff (+3-5 people)                │
│    □ Set up dedicated escalation hotline                       │
│    □ Provide compensatory service (fee waivers, etc)           │
│    □ Create customer communication plan                        │
│                                                                  │
│    Expected Impact: Reduce unresolved complaints, show          │
│                    commitment to fixing issues                   │
│                                                                  │
│ 🚨 5. Conduct Comprehensive Security Audit                     │
│    Category: Security | Priority: HIGH | Target: 2 weeks        │
│    Description:                                                 │
│    24 fraud incidents is concerning. A full security review is │
│    needed immediately to identify and close vulnerabilities.    │
│                                                                  │
│    Action Items:                                                │
│    □ Forensic analysis of fraud patterns                       │
│    □ Review ATM security protocols                             │
│    □ Audit access controls                                     │
│    □ Implement additional fraud prevention measures             │
│    □ Brief all staff on security procedures                    │
│                                                                  │
│    Expected Impact: Reduce fraud incidents by 80%+              │
│                                                                  │
│ 🚨 6. Develop Comprehensive Recovery Strategy                  │
│    Category: Strategy | Priority: HIGH | Target: 2 weeks        │
│    Description:                                                 │
│    ATM_01 requires a holistic recovery plan addressing all      │
│    aspects of the business: operations, technology, security,   │
│    and customer relations.                                      │
│                                                                  │
│    Action Items:                                                │
│    □ Executive steering committee (weekly meetings)            │
│    □ Define 30/60/90-day recovery targets                      │
│    □ Secure required budget and resources                      │
│    □ Create internal and external communication plans           │
│    □ Establish success metrics and dashboards                  │
│                                                                  │
│    Expected Impact: Move from LOW tier (42) to MEDIUM tier      │
│                    (65+) within 90 days                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Summary

After uploading the test dataset, you should observe:

| Page | Expected Display |
|------|------------------|
| **Dashboard** | 3 product cards with clear green/yellow/red status |
| **Rankings** | 3 products sorted by score (90 > 70 > 42) |
| **Scores** | Individual scores with tier assignments and breakdowns |
| **Alerts** | 9 total alerts (0 for MOBILE, 3 for CARD, 6 for ATM) |
| **Recommendations** | 11 total recommendations with actionable items |

**Total Verifiable Outputs: 26+ system-generated items showing comprehensive analysis**

This demonstrates the full capability of AHADU PULSE's ML-powered evaluation system.
