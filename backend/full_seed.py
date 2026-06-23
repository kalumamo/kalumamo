#!/usr/bin/env python
"""Complete database seed - users, products, data, scores, alerts, recommendations, predictions"""
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User
from app.models.product import Product
from app.models.data import RawData, ProcessedFeatures
from app.models.ml_models import Score, Prediction, ModelRegistry, SimilarProduct
from app.models.alerts import Alert
from app.models.recommendations import Recommendation
from datetime import date, timedelta
import random
import json
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERS_DATA = [
    ('Abebe Girma', 'admin@ahadubank.com', 'Admin@123', 'super_admin'),
    ('Tigist Alemu', 'exec@ahadubank.com', 'Exec@123', 'executive_management'),
    ('Dawit Bekele', 'pm@ahadubank.com', 'PM@12345', 'product_manager'),
    ('Hana Tesfaye', 'de@ahadubank.com', 'DE@12345', 'data_engineer'),
    ('Yonas Haile', 'ml@ahadubank.com', 'ML@12345', 'ml_engineer'),
    ('Selamawit Tadesse', 'risk@ahadubank.com', 'Risk@123', 'risk_team'),
    ('Bereket Mulugeta', 'compliance@ahadubank.com', 'Comp@123', 'compliance_team'),
]

PRODUCTS_DATA = [
    {"name": "Ahadu Mobile Banking", "code": "MOBILE_01", "category": "mobile_banking",
     "description": "Full-featured mobile banking application"},
    {"name": "Ahadu Card Banking", "code": "CARD_01", "category": "card_banking",
     "description": "Debit and credit card management"},
    {"name": "Ahadu ATM Network", "code": "ATM_01", "category": "atm",
     "description": "Nationwide ATM deployment"},
    {"name": "Ahadu POS System", "code": "POS_01", "category": "pos",
     "description": "Point-of-sale terminal network"},
    {"name": "Ahadu QR Pay", "code": "QR_01", "category": "qr_payment",
     "description": "QR code-based payment solution"},
    {"name": "Ahadu Digital Wallet", "code": "WALLET_01", "category": "digital_wallet",
     "description": "E-wallet for peer-to-peer transfers"},
]

def seed():
    db = SessionLocal()
    try:
        logger.info("Starting complete database seed...")
        
        # Disable foreign key constraints temporarily
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))

        # ===== USERS =====
        logger.info("Creating users...")
        db.execute(text("DELETE FROM audit_logs"))
        db.execute(text("DELETE FROM users"))
        db.commit()
        
        users = []
        for full_name, email, password, role in USERS_DATA:
            user = User(
                full_name=full_name,
                email=email,
                hashed_password=hash_password(password),
                role=role,
                is_active=True,
            )
            db.add(user)
            users.append(user)
        db.commit()
        logger.info(f"✓ Created {len(users)} users")

        # ===== PRODUCTS =====
        logger.info("Creating products...")
        # Delete related data first
        db.execute(text("DELETE FROM similar_products"))
        db.execute(text("DELETE FROM alerts"))
        db.execute(text("DELETE FROM recommendations"))
        db.execute(text("DELETE FROM predictions"))
        db.execute(text("DELETE FROM scores"))
        db.execute(text("DELETE FROM processed_features"))
        db.execute(text("DELETE FROM raw_data"))
        db.execute(text("DELETE FROM products"))
        db.commit()
        
        products = []
        for p_data in PRODUCTS_DATA:
            product = Product(**p_data, is_active=True)
            db.add(product)
            products.append(product)
        db.commit()
        logger.info(f"✓ Created {len(products)} products")

        # ===== RAW DATA & SCORES =====
        logger.info("Creating raw data and scores (12 months)...")
        today = date.today()
        base_month = date(today.year - 1, today.month, 1)
        periods = [date(base_month.year + (base_month.month + i - 1) // 12, 
                        (base_month.month + i - 1) % 12 + 1, 1) 
                   for i in range(12)]
        
        raw_records = []
        scores = []
        
        for product in products:
            for period_date in periods:
                # Raw data
                raw = RawData(
                    product_id=product.id,
                    period_date=period_date,
                    total_users=random.randint(100000, 900000),
                    active_users=random.randint(50000, 700000),
                    new_users=random.randint(1000, 50000),
                    churned_users=random.randint(500, 20000),
                    total_transactions=random.randint(10000, 500000),
                    successful_transactions=random.randint(8000, 490000),
                    failed_transactions=random.randint(100, 50000),
                    failed_txn_rate=round(random.uniform(0.1, 15.0), 2),
                    transaction_volume=random.randint(1000000, 100000000),
                    total_revenue=random.randint(1000000, 100000000),
                    fee_revenue=random.randint(100000, 10000000),
                    uptime_percentage=round(random.uniform(94.0, 99.9), 2),
                    downtime_hours=round(random.uniform(0.1, 50.0), 2),
                    downtime_minutes=round(random.uniform(6, 3000), 2),
                    avg_response_time_ms=random.randint(100, 1000),
                    api_error_rate=round(random.uniform(0.1, 5.0), 3),
                    total_complaints=random.randint(10, 500),
                    resolved_complaints=random.randint(5, 480),
                    csat_score=round(random.uniform(2.5, 4.8), 2),
                    fraud_event_count=random.randint(0, 20),
                    security_incident_count=random.randint(0, 5),
                    source="seed",
                    is_validated=True,
                )
                db.add(raw)
                raw_records.append(raw)
        
        db.commit()  # Commit raw records to get IDs
        
        # Now create processed features with raw_data_id
        for raw in raw_records:
                pf = ProcessedFeatures(
                    product_id=raw.product_id,
                    raw_data_id=raw.id,
                    period_date=raw.period_date,
                    transaction_success_rate=raw.successful_transactions / raw.total_transactions if raw.total_transactions > 0 else 0,
                    active_user_rate=raw.active_users / raw.total_users if raw.total_users > 0 else 0,
                    revenue_per_transaction=raw.total_revenue / raw.total_transactions if raw.total_transactions > 0 else 0,
                    revenue_per_active_user=raw.total_revenue / raw.active_users if raw.active_users > 0 else 0,
                    failed_txn_rate_pct=raw.failed_txn_rate,
                    user_engagement_index=round(random.uniform(0.3, 0.9), 2),
                    complaint_growth_rate=round(random.uniform(-20, 30), 2),
                    complaint_resolution_rate=raw.resolved_complaints / raw.total_complaints if raw.total_complaints > 0 else 0,
                    downtime_impact_score=round(random.uniform(0, 100), 2),
                    operational_efficiency_score=round(random.uniform(40, 95), 2),
                    csat_score=raw.csat_score,
                    fraud_event_count=raw.fraud_event_count,
                    api_error_rate=raw.api_error_rate,
                )
                db.add(pf)
                
                # Score
                score_val = round(random.uniform(40, 95), 2)
                tier = "HIGH" if score_val >= 75 else "MEDIUM" if score_val >= 50 else "LOW"
                score = Score(
                    product_id=raw.product_id,
                    processed_features_id=None,
                    period_date=raw.period_date,
                    performance_score=score_val,
                    performance_tier=tier,
                    model_version="rule_based_v1.0",
                    confidence=0.85,
                )
                db.add(score)
                scores.append(score)
        
        db.commit()
        logger.info(f"✓ Created {len(raw_records)} raw records, {len(scores)} scores")

        # ===== ALERTS =====
        logger.info("Creating alerts...")
        
        alert_types = ["score_drop", "downtime_spike", "failure_rate_increase", "complaint_surge"]
        severities = ["critical", "high", "medium", "low"]
        alert_messages = {
            "score_drop": "Performance score decreased significantly",
            "downtime_spike": "System uptime fell below acceptable threshold",
            "failure_rate_increase": "Transaction failure rate increased",
            "complaint_surge": "Customer complaints increased",
        }
        
        alerts_list = []
        for product in products:
            for i in range(5):
                alert_type = random.choice(alert_types)
                alert = Alert(
                    product_id=product.id,
                    alert_type=alert_type,
                    severity=random.choice(severities),
                    title=f"{alert_type.replace('_', ' ').title()} - {product.name}",
                    message=alert_messages[alert_type],
                    metric_name=alert_type,
                    metric_value=round(random.uniform(20, 90), 2),
                    threshold_value=75.0,
                    period_date=today - timedelta(days=i),
                    is_resolved=random.choice([False, False, True]),
                )
                db.add(alert)
                alerts_list.append(alert)
        
        db.commit()
        logger.info(f"✓ Created {len(alerts_list)} alerts")

        # ===== RECOMMENDATIONS =====
        logger.info("Creating recommendations...")
        
        categories = ["infrastructure", "user_adoption", "transactions"]
        priorities = ["critical", "high", "medium", "low"]
        rec_titles = {
            "infrastructure": ["Improve system availability", "Upgrade infrastructure capacity", "Optimize API performance"],
            "user_adoption": ["Enhance user onboarding", "Improve mobile app UX", "Increase feature awareness"],
            "transactions": ["Reduce transaction failures", "Improve transaction speed", "Add transaction alerts"],
        }
        
        recommendations = []
        for product in products:
            for i in range(4):
                category = random.choice(categories)
                priority = random.choice(priorities)
                title = random.choice(rec_titles[category])
                
                rec = Recommendation(
                    product_id=product.id,
                    category=category,
                    title=title,
                    description=f"Implement improvements to {category.replace('_', ' ')} for {product.name}",
                    priority=priority,
                    trigger_metric="performance_score",
                    trigger_value=round(random.uniform(40, 75), 2),
                    threshold_value=75.0,
                    ai_explanation=f"AI suggests focusing on {category}. Can improve performance by 10-15%.",
                    period_date=today - timedelta(days=i),
                    is_acknowledged=random.choice([False, False, True]),
                )
                db.add(rec)
                recommendations.append(rec)
        
        db.commit()
        logger.info(f"✓ Created {len(recommendations)} recommendations")

        # ===== ML MODELS =====
        logger.info("Creating ML models...")
        
        models_data = [
            {
                "model_name": "Logistic Regression v1.0",
                "model_type": "classification",
                "version": "v1.0",
                "accuracy": 0.87,
                "f1_score": 0.85,
                "mse": 0.142,
                "training_samples": 450000,
                "hyperparameters": json.dumps({"solver": "lbfgs", "C": 0.1}),
                "is_active": True,
            },
            {
                "model_name": "Random Forest v1.2",
                "model_type": "random_forest",
                "version": "v1.2",
                "accuracy": 0.91,
                "f1_score": 0.89,
                "mse": 0.089,
                "training_samples": 450000,
                "hyperparameters": json.dumps({"n_estimators": 20, "max_depth": 10}),
                "is_active": True,
            },
            {
                "model_name": "Ridge Regression v2.1",
                "model_type": "regression",
                "version": "v2.1",
                "r2_score": 0.88,
                "mae": 4.23,
                "mse": 28.45,
                "training_samples": 450000,
                "hyperparameters": json.dumps({"alpha": 1.0}),
                "is_active": True,
            },
            {
                "model_name": "KNN Similarity v1.0",
                "model_type": "similarity",
                "version": "v1.0",
                "training_samples": 450000,
                "hyperparameters": json.dumps({"k": 3}),
                "is_active": True,
            },
        ]
        
        models = []
        for m_data in models_data:
            training_date = today - timedelta(days=random.randint(5, 90))
            model = ModelRegistry(
                model_name=m_data["model_name"],
                model_type=m_data["model_type"],
                version=m_data["version"],
                accuracy=m_data.get("accuracy"),
                f1_score=m_data.get("f1_score"),
                r2_score=m_data.get("r2_score"),
                mae=m_data.get("mae"),
                mse=m_data.get("mse"),
                training_date=training_date,
                dataset_version="v20260621",
                training_samples=m_data["training_samples"],
                feature_count=15,
                hyperparameters=m_data["hyperparameters"],
                is_active=m_data["is_active"],
                file_path=f"/ml_models/{m_data['model_name'].replace(' ', '_').lower()}.pkl",
            )
            db.add(model)
            models.append(model)
        
        db.commit()
        logger.info(f"✓ Created {len(models)} ML models")

        # ===== PREDICTIONS =====
        logger.info("Creating predictions (3-month forward)")
        
        predictions = []
        for product in products:
            for months_ahead in range(1, 4):
                prediction_date = today + timedelta(days=30 * months_ahead)
                predicted_score = round(random.uniform(40, 95), 2)
                predicted_tier = "HIGH" if predicted_score >= 75 else "MEDIUM" if predicted_score >= 50 else "LOW"
                
                pred = Prediction(
                    product_id=product.id,
                    period_date=prediction_date,
                    predicted_score=predicted_score,
                    predicted_tier=predicted_tier,
                    prediction_horizon_days=30 * months_ahead,
                    confidence=round(random.uniform(0.70, 0.95), 3),
                    model_version="v2.1_ensemble",
                )
                db.add(pred)
                predictions.append(pred)
        
        db.commit()
        logger.info(f"✓ Created {len(predictions)} predictions")

        # ===== SIMILAR PRODUCTS =====
        logger.info("Creating product similarity relationships...")
        
        similar_products = []
        for product in products:
            other_products = [p for p in products if p.id != product.id]
            similar_count = random.randint(2, 3)
            
            for similar_product in random.sample(other_products, min(similar_count, len(other_products))):
                similarity = SimilarProduct(
                    product_id=product.id,
                    similar_product_id=similar_product.id,
                    similarity_score=round(random.uniform(0.65, 0.95), 3),
                    cluster_id=random.randint(1, 3),
                    model_version="v1.0_knn",
                )
                db.add(similarity)
                similar_products.append(similarity)
        
        db.commit()
        logger.info(f"✓ Created {len(similar_products)} similarity relationships")

        logger.info("\n✅ Complete database seeding finished successfully!")
        logger.info("=" * 60)
        logger.info("LOGIN CREDENTIALS:")
        for full_name, email, password, role in USERS_DATA:
            logger.info(f"  {role:25} | {email:30} | {password}")
        logger.info("=" * 60)
        
        # Re-enable foreign key constraints
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        
    except Exception as e:
        logger.error(f"Seeding failed: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
