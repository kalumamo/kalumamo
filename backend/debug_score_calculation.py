#!/usr/bin/env python
"""
Debug script to check score calculation and feature values
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
    print("SCORE CALCULATION DEBUG")
    print("=" * 80)
    
    # Get all products
    products = db.query(Product).filter(Product.is_active == True).all()
    print(f"\nFound {len(products)} active products\n")
    
    for product in products:
        print(f"\n{'─' * 80}")
        print(f"PRODUCT: {product.name} (ID: {product.id})")
        print(f"{'─' * 80}")
        
        # Get latest score
        latest_score = db.query(Score).filter(
            Score.product_id == product.id
        ).order_by(Score.period_date.desc()).first()
        
        if latest_score:
            print(f"Latest Score: {latest_score.performance_score}")
            print(f"Tier: {latest_score.performance_tier}")
            print(f"Period: {latest_score.period_date}")
            print(f"Previous Score: {latest_score.previous_score}")
            print(f"Score Change: {latest_score.score_change}")
        else:
            print("No score found")
            continue
        
        # Get latest features
        latest_features = db.query(ProcessedFeatures).filter(
            ProcessedFeatures.product_id == product.id
        ).order_by(ProcessedFeatures.period_date.desc()).first()
        
        if latest_features:
            print(f"\nLatest Features (Period: {latest_features.period_date}):")
            print(f"  active_user_rate: {latest_features.active_user_rate}")
            print(f"  transaction_success_rate: {latest_features.transaction_success_rate}")
            print(f"  failed_txn_rate_pct: {latest_features.failed_txn_rate_pct}")
            print(f"  revenue_per_transaction: {latest_features.revenue_per_transaction}")
            print(f"  revenue_per_active_user: {latest_features.revenue_per_active_user}")
            print(f"  operational_efficiency_score: {latest_features.operational_efficiency_score}")
            print(f"  downtime_impact_score: {latest_features.downtime_impact_score}")
            print(f"  complaint_growth_rate: {latest_features.complaint_growth_rate}")
            print(f"  complaint_resolution_rate: {latest_features.complaint_resolution_rate}")
            print(f"  fraud_event_count: {latest_features.fraud_event_count}")
            print(f"  api_error_rate: {latest_features.api_error_rate}")
            print(f"  user_engagement_index: {latest_features.user_engagement_index}")
            print(f"  avg_session_duration_sec: {latest_features.avg_session_duration_sec}")
            print(f"  csat_score: {latest_features.csat_score}")
            
            # Test score calculation
            features_dict = {
                "active_user_rate": latest_features.active_user_rate,
                "txn_success_rate": latest_features.transaction_success_rate,
                "transaction_success_rate": latest_features.transaction_success_rate,
                "failed_txn_rate": latest_features.failed_txn_rate_pct,
                "revenue_per_txn": latest_features.revenue_per_transaction,
                "revenue_per_active_user": latest_features.revenue_per_active_user,
                "operational_efficiency_score": latest_features.operational_efficiency_score,
                "downtime_impact_score": latest_features.downtime_impact_score,
                "complaint_growth_rate": latest_features.complaint_growth_rate,
                "complaint_resolution_rate": latest_features.complaint_resolution_rate,
                "fraud_incidents": latest_features.fraud_event_count,
                "api_error_rate": latest_features.api_error_rate,
                "user_engagement_index": latest_features.user_engagement_index,
                "avg_session_duration_sec": latest_features.avg_session_duration_sec,
                "csat_score": latest_features.csat_score,
            }
            
            print(f"\nRecalculated Score: {ml_service._compute_performance_score(features_dict)}")
        
        # Get score history
        score_history = db.query(Score).filter(
            Score.product_id == product.id
        ).order_by(Score.period_date).all()
        
        if len(score_history) > 1:
            print(f"\nScore History ({len(score_history)} records):")
            for s in score_history[-3:]:  # Last 3
                print(f"  {s.period_date}: {s.performance_score} ({s.performance_tier})")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
    print("\n" + "=" * 80)
    print("Done")
    print("=" * 80)
