#!/usr/bin/env python
"""
Diagnostic script to check data sync status.
Identifies gaps in the pipeline: raw_data → features → scores → alerts → recommendations
"""

import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy import text

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.data import RawData, ProcessedFeatures
from app.models.ml_models import Score
from app.models.product import Product
from app.models.alerts import Alert
from app.models.recommendations import Recommendation

def diagnose():
    db = SessionLocal()
    
    print("\n" + "="*70)
    print("AHADU PULSE DATA SYNC DIAGNOSTIC")
    print("="*70)
    
    try:
        # 1. Count products
        product_count = db.query(Product).count()
        print(f"\n1. PRODUCTS IN SYSTEM")
        print(f"   Total products: {product_count}")
        
        # 2. Count raw data
        raw_count = db.query(RawData).count()
        raw_validated = db.query(RawData).filter(RawData.is_validated == True).count()
        print(f"\n2. RAW DATA")
        print(f"   Total rows: {raw_count}")
        print(f"   Validated: {raw_validated}")
        if raw_count > 0:
            latest_raw = db.query(RawData).order_by(RawData.period_date.desc()).first()
            oldest_raw = db.query(RawData).order_by(RawData.period_date.asc()).first()
            print(f"   Date range: {oldest_raw.period_date} → {latest_raw.period_date}")
        
        # 3. Count processed features
        features_count = db.query(ProcessedFeatures).count()
        print(f"\n3. PROCESSED FEATURES")
        print(f"   Total: {features_count}")
        if features_count > 0:
            latest_feat = db.query(ProcessedFeatures).order_by(ProcessedFeatures.period_date.desc()).first()
            print(f"   Latest period: {latest_feat.period_date}")
        
        # 4. Gap check: Raw data without features
        raw_without_features = db.execute(text("""
            SELECT r.id, r.product_id, r.period_date
            FROM raw_data r
            WHERE r.is_validated = 1
            AND NOT EXISTS (SELECT 1 FROM processed_features f WHERE f.raw_data_id = r.id)
            ORDER BY r.period_date DESC
            LIMIT 10
        """)).fetchall()
        
        print(f"\n4. GAP CHECK: RAW DATA WITHOUT FEATURES")
        if raw_without_features:
            print(f"   ⚠️  MISSING FEATURES: {len(raw_without_features)} raw records without processed features")
            for row in raw_without_features[:5]:
                print(f"      - raw_id={row[0]}, product_id={row[1]}, period={row[2]}")
        else:
            print(f"   ✓ All raw data has features processed")
        
        # 5. Count scores
        score_count = db.query(Score).count()
        print(f"\n5. SCORES")
        print(f"   Total: {score_count}")
        if score_count > 0:
            latest_score = db.query(Score).order_by(Score.period_date.desc()).first()
            print(f"   Latest period: {latest_score.period_date}")
        
        # 6. Gap check: Features without scores
        features_without_scores = db.execute(text("""
            SELECT f.id, f.product_id, f.period_date
            FROM processed_features f
            WHERE NOT EXISTS (SELECT 1 FROM ml_models_score s 
                            WHERE s.product_id = f.product_id AND s.period_date = f.period_date)
            ORDER BY f.period_date DESC
            LIMIT 10
        """)).fetchall()
        
        print(f"\n6. GAP CHECK: FEATURES WITHOUT SCORES")
        if features_without_scores:
            print(f"   ⚠️  MISSING SCORES: {len(features_without_scores)} features without scores")
            for row in features_without_scores[:5]:
                print(f"      - feature_id={row[0]}, product_id={row[1]}, period={row[2]}")
        else:
            print(f"   ✓ All features have scores")
        
        # 7. Count alerts
        alert_count = db.query(Alert).count()
        print(f"\n7. ALERTS")
        print(f"   Total: {alert_count}")
        
        # 8. Count recommendations
        rec_count = db.query(Recommendation).count()
        print(f"\n8. RECOMMENDATIONS")
        print(f"   Total: {rec_count}")
        
        # 9. Products per stage
        print(f"\n9. COVERAGE BY STAGE")
        products_with_raw = db.execute(text("""
            SELECT COUNT(DISTINCT product_id) FROM raw_data WHERE is_validated = 1
        """)).scalar() or 0
        
        products_with_features = db.execute(text("""
            SELECT COUNT(DISTINCT product_id) FROM processed_features
        """)).scalar() or 0
        
        products_with_scores = db.execute(text("""
            SELECT COUNT(DISTINCT product_id) FROM ml_models_score
        """)).scalar() or 0
        
        products_with_alerts = db.execute(text("""
            SELECT COUNT(DISTINCT product_id) FROM alerts
        """)).scalar() or 0
        
        products_with_recs = db.execute(text("""
            SELECT COUNT(DISTINCT product_id) FROM recommendations
        """)).scalar() or 0
        
        print(f"   Total products: {product_count}")
        print(f"   With raw data: {products_with_raw} ({100*products_with_raw/product_count if product_count else 0:.0f}%)")
        print(f"   With features: {products_with_features} ({100*products_with_features/product_count if product_count else 0:.0f}%)")
        print(f"   With scores: {products_with_scores} ({100*products_with_scores/product_count if product_count else 0:.0f}%)")
        print(f"   With alerts: {products_with_alerts} ({100*products_with_alerts/product_count if product_count else 0:.0f}%)")
        print(f"   With recommendations: {products_with_recs} ({100*products_with_recs/product_count if product_count else 0:.0f}%)")
        
        # 10. Data quality
        print(f"\n10. DATA QUALITY ISSUES")
        null_features = db.execute(text("""
            SELECT COUNT(*) FROM processed_features 
            WHERE active_user_rate IS NULL 
            OR transaction_success_rate IS NULL
            OR operational_efficiency_score IS NULL
        """)).scalar() or 0
        
        if null_features > 0:
            print(f"   ⚠️  {null_features} feature rows with NULL computed values")
        else:
            print(f"   ✓ No obvious data quality issues")
        
        # 11. Recent activity
        print(f"\n11. RECENT ACTIVITY")
        latest_upload = db.execute(text("""
            SELECT MAX(created_at) FROM raw_data
        """)).scalar()
        
        latest_feature_calc = db.execute(text("""
            SELECT MAX(updated_at) FROM processed_features
        """)).scalar()
        
        latest_score_calc = db.execute(text("""
            SELECT MAX(created_at) FROM ml_models_score
        """)).scalar()
        
        print(f"   Latest raw upload: {latest_upload}")
        print(f"   Latest feature calculation: {latest_feature_calc}")
        print(f"   Latest score calculation: {latest_score_calc}")
        
        # 12. Summary
        print(f"\n12. PIPELINE STATUS")
        if len(raw_without_features) > 0:
            print(f"   ❌ BLOCKED: Raw data not processed to features")
        elif len(features_without_scores) > 0:
            print(f"   ❌ BLOCKED: Features not scored")
        elif products_with_recs < products_with_scores * 0.8:
            print(f"   ⚠️  WARNING: Many scores but few recommendations")
        else:
            print(f"   ✅ HEALTHY: All stages complete")
        
    except Exception as e:
        print(f"\n❌ DIAGNOSTIC ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    diagnose()
