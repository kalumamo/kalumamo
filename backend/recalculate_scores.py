#!/usr/bin/env python
"""
Recalculate all scores using the new formula
"""
import sys
sys.path.insert(0, '/d:/video/AHADU PULSE/backend')

from app.core.database import SessionLocal
from app.models.data import ProcessedFeatures
from app.models.ml_models import Score
from app.models.product import Product
from app.services.ml_service import ml_service
from datetime import datetime

db = SessionLocal()

try:
    print("=" * 80)
    print("RECALCULATING ALL SCORES")
    print("=" * 80)
    
    # Get all products
    products = db.query(Product).filter(Product.is_active == True).all()
    print(f"\nProcessing {len(products)} products...\n")
    
    total_scores_updated = 0
    
    for product in products:
        print(f"Processing: {product.name} (ID: {product.id})")
        
        # Get all features for this product in chronological order
        features_list = db.query(ProcessedFeatures).filter(
            ProcessedFeatures.product_id == product.id
        ).order_by(ProcessedFeatures.period_date).all()
        
        print(f"  Found {len(features_list)} feature records")
        
        if not features_list:
            print("  No features found, skipping")
            continue
        
        # For each feature record, recalculate score
        for idx, pf in enumerate(features_list):
            # Build feature dict
            features_dict = {
                "active_user_rate": pf.active_user_rate,
                "txn_success_rate": pf.transaction_success_rate,
                "transaction_success_rate": pf.transaction_success_rate,
                "failed_txn_rate": pf.failed_txn_rate_pct,
                "revenue_per_txn": pf.revenue_per_transaction,
                "revenue_per_active_user": pf.revenue_per_active_user,
                "operational_efficiency_score": pf.operational_efficiency_score,
                "downtime_impact_score": pf.downtime_impact_score,
                "complaint_growth_rate": pf.complaint_growth_rate,
                "complaint_resolution_rate": pf.complaint_resolution_rate,
                "fraud_incidents": pf.fraud_event_count,
                "api_error_rate": pf.api_error_rate,
                "user_engagement_index": pf.user_engagement_index,
                "avg_session_duration_sec": pf.avg_session_duration_sec,
                "csat_score": pf.csat_score,
            }
            
            # Calculate new score
            new_score = ml_service._compute_performance_score(features_dict)
            new_tier = ml_service._score_to_tier(new_score)
            
            # Get or create Score record
            score_obj = db.query(Score).filter(
                Score.product_id == product.id,
                Score.period_date == pf.period_date
            ).first()
            
            if score_obj:
                # Get previous score
                prev_score_obj = db.query(Score).filter(
                    Score.product_id == product.id,
                    Score.period_date < pf.period_date
                ).order_by(Score.period_date.desc()).first()
                
                prev_score = prev_score_obj.performance_score if prev_score_obj else None
                prev_tier = prev_score_obj.performance_tier if prev_score_obj else None
                
                # Calculate change
                score_change = round(new_score - prev_score, 2) if prev_score is not None else None
                tier_changed = (prev_tier != new_tier) if prev_tier else False
                
                # Update
                score_obj.performance_score = new_score
                score_obj.performance_tier = new_tier
                score_obj.previous_score = prev_score
                score_obj.previous_tier = prev_tier
                score_obj.score_change = score_change
                score_obj.tier_changed = tier_changed
                
                print(f"  [{idx+1}] {pf.period_date}: {new_score} ({new_tier}) - Updated")
            else:
                # Create new
                prev_score_obj = db.query(Score).filter(
                    Score.product_id == product.id,
                    Score.period_date < pf.period_date
                ).order_by(Score.period_date.desc()).first()
                
                prev_score = prev_score_obj.performance_score if prev_score_obj else None
                prev_tier = prev_score_obj.performance_tier if prev_score_obj else None
                score_change = round(new_score - prev_score, 2) if prev_score is not None else None
                tier_changed = (prev_tier != new_tier) if prev_tier else False
                
                score_obj = Score(
                    product_id=product.id,
                    processed_features_id=pf.id,
                    period_date=pf.period_date,
                    performance_score=new_score,
                    performance_tier=new_tier,
                    previous_score=prev_score,
                    previous_tier=prev_tier,
                    score_change=score_change,
                    tier_changed=tier_changed,
                    model_version="rule_based_v2.0",
                    confidence=0.85
                )
                db.add(score_obj)
                print(f"  [{idx+1}] {pf.period_date}: {new_score} ({new_tier}) - Created")
            
            total_scores_updated += 1
        
        print()
    
    # Commit all changes
    db.commit()
    
    print("=" * 80)
    print(f"SUCCESS: Updated {total_scores_updated} scores")
    print("=" * 80)
    
except Exception as e:
    db.rollback()
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
