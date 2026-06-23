#!/usr/bin/env python
"""
Debug script to check why scores aren't changing between uploads.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.core.database import SessionLocal
from app.models.data import RawData, ProcessedFeatures
from app.models.ml_models import Score
from app.services.ml_service import ml_service
from datetime import datetime

db = SessionLocal()

print("=" * 80)
print("DEBUGGING: Why Scores Aren't Changing")
print("=" * 80)

try:
    # Check raw data
    print("\n1. CHECKING RAW DATA")
    print("-" * 80)
    
    raw_data = db.query(RawData).order_by(RawData.period_date.desc()).limit(10).all()
    print(f"\nRecent raw data records: {len(raw_data)}")
    
    for raw in raw_data:
        print(f"\n  Period: {raw.period_date}")
        print(f"    Product {raw.product_id}: Transactions={raw.total_transactions}, "
              f"Success={raw.successful_transactions}, Revenue={raw.total_revenue}")
    
    # Check processed features
    print("\n\n2. CHECKING PROCESSED FEATURES")
    print("-" * 80)
    
    features = db.query(ProcessedFeatures).order_by(ProcessedFeatures.period_date.desc()).limit(10).all()
    print(f"\nRecent processed features: {len(features)}")
    
    for pf in features:
        print(f"\n  Period: {pf.period_date}")
        print(f"    Product {pf.product_id}:")
        print(f"      active_user_rate: {pf.active_user_rate}")
        print(f"      txn_success_rate: {pf.transaction_success_rate}")
        print(f"      revenue_per_txn: {pf.revenue_per_transaction}")
        print(f"      complaint_resolution_rate: {pf.complaint_resolution_rate}")
        print(f"      downtime_impact_score: {pf.downtime_impact_score}")
        print(f"      csat_score: {pf.csat_score}")
        print(f"      fraud_incidents: {pf.fraud_event_count}")
        print(f"      api_error_rate: {pf.api_error_rate}")
    
    # Check scores
    print("\n\n3. CHECKING SCORES")
    print("-" * 80)
    
    scores = db.query(Score).order_by(Score.period_date.desc()).limit(10).all()
    print(f"\nRecent scores: {len(scores)}")
    
    for score in scores:
        print(f"\n  Period: {score.period_date}")
        print(f"    Product {score.product_id}: Score={score.performance_score}, Tier={score.performance_tier}")
    
    # Test scoring manually
    print("\n\n4. TESTING SCORE CALCULATION MANUALLY")
    print("-" * 80)
    
    if features:
        pf = features[0]
        print(f"\nTesting with latest features (Product {pf.product_id}, Period {pf.period_date}):")
        
        # Build feature dict
        feature_dict = {
            "active_user_rate": pf.active_user_rate,
            "txn_success_rate": pf.transaction_success_rate,
            "failed_txn_rate": pf.failed_txn_rate_pct if hasattr(pf, 'failed_txn_rate_pct') else None,
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
        
        print("\n  Feature Values:")
        for k, v in feature_dict.items():
            if v is not None:
                print(f"    {k}: {v}")
        
        # Compute score
        computed_score = ml_service._compute_performance_score(feature_dict)
        print(f"\n  Computed Score: {computed_score}")
        
        # Get actual score from DB
        actual_score = db.query(Score).filter(
            Score.product_id == pf.product_id,
            Score.period_date == pf.period_date
        ).first()
        
        if actual_score:
            print(f"  Actual Score in DB: {actual_score.performance_score}")
            print(f"  Match: {computed_score == actual_score.performance_score}")
        else:
            print(f"  No score in DB for this period")
    
    print("\n" + "=" * 80)
    print("END DEBUG")
    print("=" * 80)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()
