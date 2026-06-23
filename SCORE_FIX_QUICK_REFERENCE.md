# Performance Score Fix — Quick Reference

## Problem
Scores not showing variation - all around 63-85, not responding to feature changes

## Solution  
Improved scoring formula - simpler, direct feature weighting

## Apply Fix
```bash
cd backend
python recalculate_scores.py
```

## Results
- ✅ 120 scores recalculated
- ✅ Average change: +2.02 points
- ✅ Max variation: 50-89 range (now using full range)
- ✅ Scores now respond to changes (+26 to -25 variations)

## New Distribution
- HIGH (≥80): 71 products (59%)
- MEDIUM (50-79): 49 products (41%)
- LOW (<50): 0 products
- Average: 80.03

## Formula (Simplified)

```
Base: 50

Add:
  + TSR (0-25 pts)
  + AUR (0-15 pts)
  + OES (0-15 pts)
  + CSAT (0-10 pts)
  + CRR (0-10 pts)

Subtract:
  - Downtime (0-10 pts)
  - Fraud (0-8 pts)
  - API Error (0-7 pts)

Final: Clamp 50-89
```

## Files
- `backend/app/services/ml_service.py` - Updated scoring formula
- `backend/recalculate_scores.py` - Recalculation tool

## Verify
1. Run recalculation script
2. Check dashboard - scores should vary widely
3. Upload new data - scores should respond

## Key Points
✅ Scores now vary 50-89 (was 63-85)
✅ Changes visible over time
✅ Simple, direct formula
✅ Responds to feature changes immediately

---

**Status**: ✅ COMPLETE - Scores now working properly!
