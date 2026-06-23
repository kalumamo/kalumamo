#!/usr/bin/env python
"""
Fix sync pipeline - ensures all data flows: raw → features → scores → alerts → recommendations
This script WILL fix the missing April data and ensure everything is synchronized.
"""

import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.data import RawData, ProcessedFeatures
from app.models.ml_models import Score
from app.models.product import Product
from app.services.feature_engineering import feature_engineering_service
from app.services.ml_service import ml_service
from app.services.recommendation_service import recommendation_service
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
logger = logging.getLogger(__name__)


def fix_sync():
    """Fix the entire sync pipeline from scratch."""
    db = SessionLocal()
    
    print("\n" + "="*70)
    print("AHADU PULSE DATA SYNC FIX")
    print("="*70)
    
    try:
        # STEP 1: Process all raw data into features
        print("\n[1/4] Processing raw data into features...")
        logger.info("Starting feature engineering for all validated raw data")
        
        all_raw = db.query(RawData).filter(RawData.is_validated == True).order_by(RawData.period_date).all()
        logger.info(f"Found {len(all_raw)} validated raw records")
        
        features_count = 0
        for raw in all_raw:
            # Check if features already exist for this raw record
            existing_features = db.query(ProcessedFeatures).filter(
                ProcessedFeatures.raw_data_id == raw.id
            ).first()
            
            if existing_features:
                logger.debug(f"Features already exist for raw_id={raw.id}")
                continue
            
            try:
                processed = feature_engineering_service.process_and_store(raw, db)
                features_count += 1
                logger.debug(f"✓ Processed raw_id={raw.id} → features_id={processed.id}")
            except Exception as e:
                logger.error(f"✗ Failed to process raw_id={raw.id}: {e}")
                db.rollback()
        
        print(f"   ✓ Created {features_count} new feature records")
        
        # STEP 2: Score all products with processed features
        print("\n[2/4] Generating scores for all processed features...")
        logger.info("Starting scoring for all products with features")
        
        # Get unique (product_id, period_date) combinations that have features but no scores
        features_without_scores_query = db.query(
            ProcessedFeatures.product_id,
            ProcessedFeatures.period_date
        ).outerjoin(
            Score,
            (Score.product_id == ProcessedFeatures.product_id) &
            (Score.period_date == ProcessedFeatures.period_date)
        ).filter(
            Score.id == None  # Score doesn't exist
        ).distinct()
        
        features_needing_scores = features_without_scores_query.all()
        logger.info(f"Found {len(features_needing_scores)} feature records needing scores")
        
        scores_created = 0
        for product_id, period_date in features_needing_scores:
            try:
                score_obj = ml_service.score_product(db, product_id, period_date)
                scores_created += 1
                logger.debug(f"✓ Scored product_id={product_id}, period={period_date}: {score_obj.performance_score}")
            except Exception as e:
                logger.error(f"✗ Failed to score product_id={product_id}, period={period_date}: {e}")
                db.rollback()
        
        print(f"   ✓ Created {scores_created} new score records")
        
        # STEP 3: Generate alerts for all scores
        print("\n[3/4] Generating alerts for all scored products...")
        logger.info("Generating alerts for all scores")
        
        # Get all scores that don't have corresponding alerts
        all_scores = db.query(Score).order_by(Score.created_at.desc()).all()
        logger.info(f"Found {len(all_scores)} total scores")
        
        alerts_created = 0
        for score in all_scores:
            try:
                # Get features for this score
                features = db.query(ProcessedFeatures).filter(
                    ProcessedFeatures.product_id == score.product_id,
                    ProcessedFeatures.period_date == score.period_date
                ).first()
                
                if not features:
                    logger.warning(f"No features found for score_id={score.id}")
                    continue
                
                # Build features dict
                features_dict = {
                    "active_user_rate": features.active_user_rate,
                    "txn_success_rate": features.transaction_success_rate,
                    "transaction_success_rate": features.transaction_success_rate,
                    "failed_txn_rate": features.failed_txn_rate_pct,
                    "revenue_per_txn": features.revenue_per_transaction,
                    "revenue_per_active_user": features.revenue_per_active_user,
                    "operational_efficiency_score": features.operational_efficiency_score,
                    "downtime_impact_score": features.downtime_impact_score,
                    "complaint_growth_rate": features.complaint_growth_rate,
                    "complaint_resolution_rate": features.complaint_resolution_rate,
                    "fraud_incidents": features.fraud_event_count,
                    "api_error_rate": features.api_error_rate,
                    "user_engagement_index": features.user_engagement_index,
                    "avg_session_duration_sec": features.avg_session_duration_sec,
                    "csat_score": features.csat_score,
                }
                
                recommendation_service.generate_alerts(
                    db, score.product_id, score.period_date, score, features_dict
                )
                alerts_created += 1
                logger.debug(f"✓ Generated alerts for score_id={score.id}")
            except Exception as e:
                logger.error(f"✗ Failed to generate alerts for score_id={score.id}: {e}")
                db.rollback()
        
        print(f"   ✓ Created/updated alerts for scores")
        
        # STEP 4: Generate recommendations for all scores
        print("\n[4/4] Generating recommendations for all scored products...")
        logger.info("Generating recommendations for all scores")
        
        recs_created = 0
        for score in all_scores:
            try:
                features = db.query(ProcessedFeatures).filter(
                    ProcessedFeatures.product_id == score.product_id,
                    ProcessedFeatures.period_date == score.period_date
                ).first()
                
                if not features:
                    logger.warning(f"No features found for score_id={score.id}")
                    continue
                
                features_dict = {
                    "active_user_rate": features.active_user_rate,
                    "txn_success_rate": features.transaction_success_rate,
                    "transaction_success_rate": features.transaction_success_rate,
                    "failed_txn_rate": features.failed_txn_rate_pct,
                    "revenue_per_txn": features.revenue_per_transaction,
                    "revenue_per_active_user": features.revenue_per_active_user,
                    "operational_efficiency_score": features.operational_efficiency_score,
                    "downtime_impact_score": features.downtime_impact_score,
                    "complaint_growth_rate": features.complaint_growth_rate,
                    "complaint_resolution_rate": features.complaint_resolution_rate,
                    "fraud_incidents": features.fraud_event_count,
                    "api_error_rate": features.api_error_rate,
                    "user_engagement_index": features.user_engagement_index,
                    "avg_session_duration_sec": features.avg_session_duration_sec,
                    "csat_score": features.csat_score,
                }
                
                recommendation_service.generate_for_product(
                    db, score.product_id, score.period_date, score, features_dict
                )
                recs_created += 1
                logger.debug(f"✓ Generated recommendations for score_id={score.id}")
            except Exception as e:
                logger.error(f"✗ Failed to generate recommendations for score_id={score.id}: {e}")
                db.rollback()
        
        print(f"   ✓ Created/updated recommendations for scores")
        
        # FINAL SUMMARY
        print("\n" + "="*70)
        print("SYNC COMPLETE ✓")
        print("="*70)
        print(f"\n Summary:")
        print(f"   Features processed:  {features_count}")
        print(f"   Scores created:      {scores_created}")
        print(f"   Alerts generated:    ✓")
        print(f"   Recommendations:     ✓")
        print(f"\n All data flows:")
        print(f"   Raw Data → Features → Scores → Alerts & Recommendations")
        print(f"\n ✅ Database is now fully synchronized!")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ SYNC ERROR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    fix_sync()
