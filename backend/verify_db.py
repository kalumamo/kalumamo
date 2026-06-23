#!/usr/bin/env python
"""Verify database contents."""
from app.core.database import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.alerts import Alert
from app.models.recommendations import Recommendation
from app.models.ml_models import Prediction, Score

db = SessionLocal()

print("\n" + "="*70)
print("DATABASE VERIFICATION")
print("="*70)

# Users
users = db.query(User).all()
print(f"\n✓ Users: {len(users)}")
for u in users[:3]:
    print(f"  - {u.email} ({u.role})")

# Products
products = db.query(Product).all()
print(f"\n✓ Products: {len(products)}")
for p in products[:3]:
    print(f"  - {p.name}")

# Alerts
alerts = db.query(Alert).all()
print(f"\n✓ Alerts: {len(alerts)}")
for a in alerts[:3]:
    print(f"  - {a.title} ({a.severity})")

# Recommendations
recs = db.query(Recommendation).all()
print(f"\n✓ Recommendations: {len(recs)}")
for r in recs[:3]:
    print(f"  - {r.title} ({r.priority})")

# Scores
scores = db.query(Score).all()
print(f"\n✓ Scores: {len(scores)}")
for s in scores[:3]:
    print(f"  - {s.performance_score} ({s.performance_tier})")

# Predictions
preds = db.query(Prediction).all()
print(f"\n✓ Predictions: {len(preds)}")
for p in preds[:3]:
    print(f"  - {p.predicted_score} ({p.predicted_tier})")

print("\n" + "="*70 + "\n")
db.close()
