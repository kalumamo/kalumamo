#!/usr/bin/env python
"""Generate alerts for all products"""
import logging
from app.core.database import SessionLocal
from app.models.product import Product
from app.models.data import ProcessedFeatures
from app.models.ml_models import Score
from app.services.recommendation_service import recommendation_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SessionLocal()

try:
    products = db.query(Product).filter(Product.is_active == True).all()
    logger.info(f"Found {len(products)} active products")
    
    for product in products:
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
            
            logger.info(f"Generating alerts for {product.name}...")
            recommendation_service.generate_alerts(
                db, product.id, latest_pf.period_date, latest_score, features
            )
            db.commit()
    
    logger.info("Alert generation completed!")
    
    from app.models.alerts import Alert
    alert_count = db.query(Alert).count()
    logger.info(f"Total alerts created: {alert_count}")

except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
finally:
    db.close()
