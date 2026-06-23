#!/usr/bin/env python
"""
System Diagnostic - Verifies all components are working correctly.
Run this to verify the implementation is complete and functional.
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import SessionLocal
from app.services.ml_service import ml_service
from app.services.feature_engineering import feature_engineering_service

def check_database():
    """Check database connectivity and record counts."""
    print("\n📊 DATABASE VERIFICATION")
    print("=" * 50)
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # Count records
            raw = conn.execute(text('SELECT COUNT(*) FROM raw_data WHERE is_validated = 1')).scalar()
            pf = conn.execute(text('SELECT COUNT(*) FROM processed_features')).scalar()
            scores = conn.execute(text('SELECT COUNT(*) FROM scores')).scalar()
            preds = conn.execute(text('SELECT COUNT(*) FROM predictions')).scalar()
            
            print(f"✓ Raw Data (validated):    {raw:4d} records")
            print(f"✓ Processed Features:      {pf:4d} records")
            print(f"✓ Scores:                  {scores:4d} records")
            print(f"✓ Predictions:             {preds:4d} records")
            
            # Check prediction variation
            result = conn.execute(text('''
                SELECT 
                    MIN(predicted_score) as min_score,
                    MAX(predicted_score) as max_score,
                    COUNT(DISTINCT product_id) as products
                FROM predictions
            ''')).fetchone()
            
            if result:
                print(f"\n✓ Prediction Score Range:  {result[0]:.2f} to {result[1]:.2f}")
                print(f"✓ Unique Products:         {result[2]} products")
                
                if result[0] < result[1]:
                    print("✓ Scores are VARIED (not all same) ✅")
                else:
                    print("⚠ Scores are NOT varied (all same)")
            
            return True
    except Exception as e:
        print(f"✗ Database Error: {e}")
        return False

def check_models():
    """Check if ML models are loaded."""
    print("\n🤖 ML MODEL VERIFICATION")
    print("=" * 50)
    
    try:
        db = SessionLocal()
        
        # Check for trained models
        from app.models.ml_models import ModelRegistry
        
        models = db.query(ModelRegistry).filter(ModelRegistry.is_active == True).all()
        
        if models:
            print(f"✓ Active Models Found:     {len(models)} model(s)")
            for m in models:
                print(f"  - {m.model_name} ({m.model_type}): {m.version}")
        else:
            print("⚠ No active models found (will use rule-based scoring)")
        
        db.close()
        return True
    except Exception as e:
        print(f"✗ Model Error: {e}")
        return False

def check_predictions():
    """Test prediction generation."""
    print("\n🔮 PREDICTION GENERATION TEST")
    print("=" * 50)
    
    try:
        db = SessionLocal()
        
        # Test predict_3months for product 19
        preds = ml_service.predict_3months(db, 19)
        
        print(f"✓ Generated {len(preds)} predictions for Product 19:")
        
        scores = []
        for p in preds:
            print(f"  {p['period_date']} | Score: {p['predicted_score']:6.2f} | Tier: {p['predicted_tier']:6s}")
            scores.append(p['predicted_score'])
        
        # Check variation
        if len(set(scores)) > 1:
            print("\n✓ Predictions are VARIED ✅")
        else:
            print("\n⚠ Predictions are all the same (not varied)")
        
        db.close()
        return True
    except Exception as e:
        print(f"✗ Prediction Error: {e}")
        return False

def check_features():
    """Check feature engineering."""
    print("\n⚙️  FEATURE ENGINEERING TEST")
    print("=" * 50)
    
    try:
        db = SessionLocal()
        from app.models.data import RawData, ProcessedFeatures
        
        # Get latest raw data
        raw = db.query(RawData).filter(RawData.is_validated == True).order_by(RawData.id.desc()).first()
        
        if raw:
            print(f"✓ Latest Raw Data:         Product {raw.product_id}, Date {raw.period_date}")
            
            # Check for corresponding features
            pf = db.query(ProcessedFeatures).filter(
                ProcessedFeatures.product_id == raw.product_id,
                ProcessedFeatures.period_date == raw.period_date
            ).first()
            
            if pf:
                print(f"✓ Features Computed:       Yes")
                print(f"  - Active User Rate:      {pf.active_user_rate}")
                print(f"  - Transaction Success:   {pf.transaction_success_rate}")
                print(f"  - Operational Efficiency: {pf.operational_efficiency_score}")
            else:
                print(f"⚠ Features Not Found:      No features for this raw data")
        
        db.close()
        return True
    except Exception as e:
        print(f"✗ Feature Error: {e}")
        return False

def main():
    """Run all diagnostics."""
    print("\n" + "=" * 50)
    print("🔧 AHADU PULSE - SYSTEM DIAGNOSTIC")
    print("=" * 50)
    
    results = []
    results.append(("Database", check_database()))
    results.append(("Models", check_models()))
    results.append(("Features", check_features()))
    results.append(("Predictions", check_predictions()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10s} {name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All systems operational!")
        print("\nNEXT STEPS:")
        print("1. Clear browser cache: Ctrl+Shift+Delete")
        print("2. Delete .next folder: rm -r frontend/.next")
        print("3. Restart frontend: npm run dev")
        print("4. Hard refresh: Ctrl+Shift+R")
        print("5. Test upload on Settings page")
        return 0
    else:
        print("\n⚠️  Some checks failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
