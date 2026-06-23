#!/usr/bin/env python
"""Debug Product 23 scoring."""
from app.core.database import SessionLocal
from app.models.data import ProcessedFeatures

db = SessionLocal()
try:
    # Get all records for product 23
    records = db.query(ProcessedFeatures).filter(
        ProcessedFeatures.product_id == 23
    ).order_by(ProcessedFeatures.period_date).all()
    
    print(f"Product 23: {len(records)} records")
    print("=" * 70)
    
    for pf in records[:3]:
        print(f"\n{pf.period_date}:")
        print(f"  TSR: {pf.transaction_success_rate}")
        print(f"  AUR: {pf.active_user_rate}")
        print(f"  OES: {pf.operational_efficiency_score}")
        print(f"  DIS: {pf.downtime_impact_score}")
        print(f"  CRR: {pf.complaint_resolution_rate}")
        print(f"  CSAT: {pf.csat_score}")
        
        # Calculate score manually
        from app.services.ml_service import ml_service
        features = {
            "txn_success_rate": pf.transaction_success_rate,
            "transaction_success_rate": pf.transaction_success_rate,
            "active_user_rate": pf.active_user_rate,
            "operational_efficiency_score": pf.operational_efficiency_score,
            "downtime_impact_score": pf.downtime_impact_score,
            "complaint_resolution_rate": pf.complaint_resolution_rate,
            "csat_score": pf.csat_score,
            "fraud_incidents": pf.fraud_event_count,
            "api_error_rate": pf.api_error_rate,
        }
        
        score = ml_service._compute_performance_score(features)
        print(f"  Calculated Score: {score}")

finally:
    db.close()
