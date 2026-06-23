#!/usr/bin/env python
"""Test new scoring formula."""
from app.core.database import SessionLocal
from app.models.ml_models import Score

db = SessionLocal()
try:
    # Recalculate and get new scores
    from app.services.ml_service import ml_service
    from app.models.data import ProcessedFeatures
    
    pf_list = db.query(ProcessedFeatures).all()
    
    for pf in pf_list[:6]:  # Just test first 6
        features = {
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
        
        score = ml_service._compute_performance_score(features)
        print(f"Product {pf.product_id} {pf.period_date}: {score:.2f}")

finally:
    db.close()
