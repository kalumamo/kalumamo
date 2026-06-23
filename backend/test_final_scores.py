#!/usr/bin/env python
"""Final test of improved scoring."""
from app.services.ml_service import ml_service
from app.core.database import SessionLocal
from sqlalchemy import func
from app.models.ml_models import Score

db = SessionLocal()
try:
    # Test predictions
    print("=== PREDICTIONS FOR PRODUCT 19 ===")
    preds = ml_service.predict_3months(db, 19)
    for p in preds:
        print(f"{p['period_date']}: Score {p['predicted_score']:.2f} | Tier: {p['predicted_tier']}")
    
    # Get score stats
    print("\n=== SCORE STATISTICS ===")
    result = db.query(
        func.min(Score.performance_score).label("min_score"),
        func.max(Score.performance_score).label("max_score"),
        func.avg(Score.performance_score).label("avg_score"),
        func.count(Score.id).label("total_scores")
    ).first()
    
    print(f"Min Score: {result.min_score:.2f}")
    print(f"Max Score: {result.max_score:.2f}")
    print(f"Avg Score: {result.avg_score:.2f}")
    print(f"Total Scores: {result.total_scores}")
    
    # Count by tier
    print("\n=== SCORES BY TIER ===")
    tier_counts = db.query(
        Score.performance_tier,
        func.count(Score.id)
    ).group_by(Score.performance_tier).all()
    
    for tier, count in tier_counts:
        print(f"{tier}: {count} products")

finally:
    db.close()
