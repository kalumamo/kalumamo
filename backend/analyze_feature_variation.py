#!/usr/bin/env python
"""Analyze feature variation to understand score spread."""
from app.core.database import SessionLocal
from app.models.data import ProcessedFeatures
import statistics

db = SessionLocal()
try:
    pf_list = db.query(ProcessedFeatures).all()
    
    print("FEATURE VARIATION ANALYSIS")
    print("=" * 70)
    
    features_dict = {
        "active_user_rate": [],
        "transaction_success_rate": [],
        "operational_efficiency_score": [],
        "downtime_impact_score": [],
        "complaint_resolution_rate": [],
        "csat_score": [],
        "fraud_event_count": [],
        "api_error_rate": [],
    }
    
    for pf in pf_list:
        if pf.active_user_rate: features_dict["active_user_rate"].append(pf.active_user_rate)
        if pf.transaction_success_rate: features_dict["transaction_success_rate"].append(pf.transaction_success_rate)
        if pf.operational_efficiency_score: features_dict["operational_efficiency_score"].append(pf.operational_efficiency_score)
        if pf.downtime_impact_score: features_dict["downtime_impact_score"].append(pf.downtime_impact_score)
        if pf.complaint_resolution_rate: features_dict["complaint_resolution_rate"].append(pf.complaint_resolution_rate)
        if pf.csat_score: features_dict["csat_score"].append(pf.csat_score)
        if pf.fraud_event_count: features_dict["fraud_event_count"].append(pf.fraud_event_count)
        if pf.api_error_rate: features_dict["api_error_rate"].append(pf.api_error_rate)
    
    for feat_name, values in features_dict.items():
        if values:
            print(f"\n{feat_name}:")
            print(f"  Count: {len(values)}")
            print(f"  Min: {min(values):.4f}")
            print(f"  Max: {max(values):.4f}")
            print(f"  Avg: {statistics.mean(values):.4f}")
            print(f"  StdDev: {statistics.stdev(values) if len(values) > 1 else 0:.4f}")
            print(f"  Range: {max(values) - min(values):.4f}")

finally:
    db.close()
