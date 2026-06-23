#!/usr/bin/env python
"""Seed complete database with all data without resetting structure"""
import logging
from app.db.seed import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting database seeding...")

# The seed_database function checks if admin user exists
# If it does, it skips seeding. We need to force it.
# Let's modify the approach - delete the check and always seed

from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
# Check if we have users
user_count = db.query(User).count()
db.close()

if user_count > 0:
    logger.info(f"Found {user_count} users. Running seed_database() which will populate other tables...")
    # The seed_database checks for admin user and skips if found
    # We need to bypass this. Let's manually call the seeding logic
    from app.db.seed import PRODUCTS_SEED, PRODUCT_PROFILES
    from app.core.database import SessionLocal
    from app.models.product import Product
    from app.models.data import RawData, ProcessedFeatures
    from app.models.ml_models import Score
    from app.models.recommendations import Recommendation
    from app.models.alerts import Alert
    from app.core.security import hash_password
    import random
    from datetime import date
    
    db = SessionLocal()
    
    try:
        # Check if products exist
        product_count = db.query(Product).count()
        if product_count == 0:
            logger.info("Seeding products...")
            for p in PRODUCTS_SEED:
                product = Product(**p, is_active=True)
                db.add(product)
            db.commit()
            logger.info(f"Seeded {len(PRODUCTS_SEED)} products")
        else:
            logger.info(f"Products already exist ({product_count}). Skipping product seeding.")
        
        # Check if scores exist
        score_count = db.query(Score).count()
        if score_count == 0:
            logger.info("Seeding products with scores, alerts, and recommendations...")
            from app.services.feature_engineering import feature_engineering_service
            from app.services.ml_service import ml_service
            from app.services.recommendation_service import recommendation_service
            
            products = {p.code: p for p in db.query(Product).all()}
            
            # Seed 12 months of MONTHLY raw data
            random.seed(42)
            today = date.today()
            
            def next_month(d: date, n: int) -> date:
                """Advance date by n months, always landing on day 1."""
                total_months = d.year * 12 + d.month - 1 + n
                return date(total_months // 12, total_months % 12 + 1, 1)
            
            base_month = date(today.year - 1, today.month, 1)
            periods = [next_month(base_month, i) for i in range(12)]
            
            raw_records = []
            for code, profile in PRODUCT_PROFILES.items():
                product = products.get(code)
                if not product:
                    continue
                
                prev_complaints = None
                for month_idx, period_date in enumerate(periods):
                    r = random.Random(hash(code + str(period_date)))
                    
                    trend = profile.get("trend", "stable")
                    t = month_idx / 11.0
                    if trend == "improving":
                        trend_factor = 1.0 + 0.08 * t
                    elif trend == "worsening":
                        trend_factor = 1.0 - 0.10 * t
                    elif trend == "slight_decline":
                        trend_factor = 1.0 - 0.04 * t
                    else:
                        trend_factor = 1.0 + r.uniform(-0.01, 0.01)
                    
                    noise = lambda lo=0.96, hi=1.04: r.uniform(lo, hi)
                    
                    total_users = int(profile["base_users"] * (1 + 0.01 * month_idx) * noise())
                    base_aur = {
                        "MOBILE_01": 0.66, "CARD_01": 0.68, "ATM_01": 0.47,
                        "POS_01": 0.55, "QR_01": 0.83, "WALLET_01": 0.75
                    }.get(code, 0.60)
                    active_rate = min(0.92, max(0.35, base_aur * trend_factor * noise(0.95, 1.05)))
                    active_users = int(total_users * active_rate)
                    new_users = int(total_users * r.uniform(0.018, 0.045))
                    churned_users = int(total_users * r.uniform(0.008, 0.025))
                    
                    txn_per_active = r.uniform(3.2, 8.5)
                    total_txns = int(active_users * txn_per_active)
                    success_rate = min(0.995, max(0.82, profile["base_success"] * trend_factor * noise(0.97, 1.03)))
                    successful_txns = int(total_txns * success_rate)
                    failed_txns = total_txns - successful_txns
                    failed_txn_rate = round(failed_txns / total_txns * 100, 4) if total_txns > 0 else 0.0
                    
                    total_revenue = int(profile["base_revenue"] * trend_factor * noise(0.93, 1.07))
                    fee_revenue = int(total_revenue * r.uniform(0.10, 0.15))
                    txn_volume = int(total_revenue * r.uniform(6.5, 12.0))
                    
                    uptime = min(99.99, max(88.0, profile["base_uptime"] * trend_factor * noise(0.995, 1.005)))
                    downtime_hours = max(0.0, (100.0 - uptime) / 100.0 * 720)
                    avg_response_ms = int(r.uniform(250, 850) * (2.0 - trend_factor + 0.05))
                    api_error = max(0.1, profile["api_error_base"] * (2.0 - trend_factor) * noise(0.90, 1.10))
                    
                    complaint_rate = profile["complaint_rate"] * (2.0 - trend_factor)
                    complaints = max(0, int(total_users / 1000 * complaint_rate * noise(0.85, 1.15)))
                    resolved = int(complaints * r.uniform(0.72, 0.96))
                    
                    csat = min(4.9, max(2.3, profile["base_csat"] * trend_factor * noise(0.97, 1.03)))
                    csat = round(csat, 2)
                    
                    fraud = max(0, int(profile["fraud_base"] * (2.0 - trend_factor) * noise(0.7, 1.4)))
                    
                    raw = RawData(
                        product_id=product.id,
                        period_date=period_date,
                        total_users=total_users,
                        active_users=active_users,
                        new_users=new_users,
                        churned_users=churned_users,
                        total_transactions=total_txns,
                        successful_transactions=successful_txns,
                        failed_transactions=failed_txns,
                        failed_txn_rate=failed_txn_rate,
                        transaction_volume=txn_volume,
                        total_revenue=total_revenue,
                        fee_revenue=fee_revenue,
                        uptime_percentage=round(uptime, 2),
                        downtime_hours=round(downtime_hours, 3),
                        downtime_minutes=round(downtime_hours * 60, 2),
                        avg_response_time_ms=avg_response_ms,
                        api_error_rate=round(api_error, 3),
                        total_complaints=complaints,
                        resolved_complaints=resolved,
                        csat_score=csat,
                        fraud_event_count=fraud,
                        security_incident_count=0,
                        source="seed",
                        is_validated=True,
                    )
                    db.add(raw)
                    raw_records.append(raw)
            
            db.commit()
            logger.info(f"Seeded {len(raw_records)} raw data records")
            
            # Generate features and scores
            all_raw = db.query(RawData).filter(RawData.source == "seed").order_by(
                RawData.product_id, RawData.period_date
            ).all()
            
            prev_scores = {}
            prev_raw_by_product = {}
            
            for raw in all_raw:
                prev_raw = prev_raw_by_product.get(raw.product_id)
                pf = feature_engineering_service.process_and_store(raw, db, prev_raw=prev_raw)
                prev_raw_by_product[raw.product_id] = raw
                
                features = {
                    "txn_success_rate": pf.transaction_success_rate,
                    "active_user_rate": pf.active_user_rate,
                    "revenue_per_transaction": pf.revenue_per_transaction,
                    "revenue_per_active_user": pf.revenue_per_active_user,
                    "transaction_success_rate": pf.transaction_success_rate,
                    "failed_txn_rate": pf.failed_txn_rate_pct,
                    "user_engagement_index": pf.user_engagement_index,
                    "complaint_growth_rate": pf.complaint_growth_rate,
                    "complaint_resolution_rate": pf.complaint_resolution_rate,
                    "downtime_impact_score": pf.downtime_impact_score,
                    "operational_efficiency_score": pf.operational_efficiency_score,
                    "csat_score": pf.csat_score,
                    "fraud_incidents": pf.fraud_event_count,
                    "api_error_rate": pf.api_error_rate,
                }
                pred = ml_service.predict(db, raw.product_id, features)
                perf_score = pred["predicted_score"]
                tier = pred["predicted_tier"]
                prev = prev_scores.get(raw.product_id)
                
                score_obj = Score(
                    product_id=raw.product_id,
                    processed_features_id=pf.id,
                    period_date=raw.period_date,
                    performance_score=perf_score,
                    previous_score=prev["score"] if prev else None,
                    score_change=round(perf_score - prev["score"], 2) if prev else None,
                    performance_tier=tier,
                    previous_tier=prev["tier"] if prev else None,
                    tier_changed=(prev["tier"] != tier) if prev else False,
                    model_version="rule_based_v1.0",
                    confidence=0.75,
                )
                db.add(score_obj)
                db.commit()
                db.refresh(score_obj)
                prev_scores[raw.product_id] = {"score": perf_score, "tier": tier}
            
            logger.info("Generated features and scores")
            
            # Generate recommendations and alerts for latest period
            for product in db.query(Product).filter(Product.is_active == True).all():
                latest_raw = (
                    db.query(RawData)
                    .filter(RawData.product_id == product.id, RawData.source == "seed")
                    .order_by(RawData.period_date.desc())
                    .first()
                )
                if not latest_raw:
                    continue
                latest_pf = (
                    db.query(ProcessedFeatures)
                    .filter(ProcessedFeatures.product_id == product.id)
                    .order_by(ProcessedFeatures.period_date.desc())
                    .first()
                )
                latest_score = (
                    db.query(Score)
                    .filter(Score.product_id == product.id)
                    .order_by(Score.period_date.desc())
                    .first()
                )
                if latest_pf and latest_score:
                    features = {
                        "txn_success_rate": latest_pf.transaction_success_rate,
                        "active_user_rate": latest_pf.active_user_rate,
                        "complaint_growth_rate": latest_pf.complaint_growth_rate,
                        "complaint_resolution_rate": latest_pf.complaint_resolution_rate,
                        "downtime_impact_score": latest_pf.downtime_impact_score,
                        "operational_efficiency_score": latest_pf.operational_efficiency_score,
                        "revenue_per_active_user": latest_pf.revenue_per_active_user,
                        "user_engagement_index": latest_pf.user_engagement_index,
                        "csat_score": latest_pf.csat_score,
                        "fraud_incidents": latest_pf.fraud_event_count,
                        "api_error_rate": latest_pf.api_error_rate,
                    }
                    recommendation_service.generate_for_product(
                        db, product.id, latest_raw.period_date, latest_score, features
                    )
                    recommendation_service.generate_alerts(
                        db, product.id, latest_raw.period_date, latest_score, features
                    )
            
            db.commit()
            logger.info("Generated recommendations and alerts")
        else:
            logger.info(f"Scores already exist ({score_count}). Skipping score seeding.")
        
        db.close()
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Seeding failed: {e}", exc_info=True)
        db.close()
else:
    logger.info("No users found. Run fix_users.py first to create users.")
