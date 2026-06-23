#!/usr/bin/env python
"""Quick test of predictions endpoint."""
from app.services.ml_service import ml_service
from app.core.database import SessionLocal

db = SessionLocal()
try:
    preds = ml_service.predict_3months(db, 19)
    print(f'✓ Generated {len(preds)} predictions for product 19:')
    for p in preds:
        print(f"  {p['period_date']} | Score: {p['predicted_score']:6.2f} | Tier: {p['predicted_tier']:6s}")
finally:
    db.close()
