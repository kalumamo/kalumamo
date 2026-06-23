"""
Data Management API — upload, validate, feature engineering.
Two-step flow:
  Step 1 — POST /upload     : validate + bulk ingest raw_data only (fast)
  Step 2 — POST /engineer   : features → scoring → alerts → recommendations
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional
from datetime import date
import logging

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User
from app.models.data import RawData, ProcessedFeatures
from app.models.ml_models import Score
from app.models.product import Product
from app.schemas.data import RawDataCreate, RawDataResponse, ProcessedFeaturesResponse
from app.services.data_service import data_service
from app.services.feature_engineering import feature_engineering_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/data", tags=["Data Management"])


def _run_scoring_pipeline(db: Session, product_ids: List[int], period_dates: List[date]):
    """Score products and generate recommendations + alerts."""
    from app.services.ml_service import ml_service
    from app.services.recommendation_service import recommendation_service

    scored = []
    for product_id in set(product_ids):
        product_periods = [d for pid, d in zip(product_ids, period_dates) if pid == product_id]
        if not product_periods:
            continue
        latest_period = max(product_periods)

        try:
            pf = (
                db.query(ProcessedFeatures)
                .filter(
                    ProcessedFeatures.product_id == product_id,
                    ProcessedFeatures.period_date == latest_period,
                )
                .first()
            )
            if not pf:
                logger.warning(f"No processed features for product_id={product_id} period={latest_period}")
                continue

            features = {
                "active_user_rate":             pf.active_user_rate,
                "txn_success_rate":             pf.transaction_success_rate,
                "transaction_success_rate":     pf.transaction_success_rate,
                "failed_txn_rate":              pf.failed_txn_rate_pct,
                "revenue_per_txn":              pf.revenue_per_transaction,
                "revenue_per_active_user":      pf.revenue_per_active_user,
                "operational_efficiency_score": pf.operational_efficiency_score,
                "downtime_impact_score":        pf.downtime_impact_score,
                "complaint_growth_rate":        pf.complaint_growth_rate,
                "complaint_resolution_rate":    pf.complaint_resolution_rate,
                "fraud_incidents":              pf.fraud_event_count,
                "api_error_rate":               pf.api_error_rate,
                "user_engagement_index":        pf.user_engagement_index,
                "avg_session_duration_sec":     pf.avg_session_duration_sec,
                "csat_score":                   pf.csat_score,
            }

            # Get previous score for this product
            previous_score_obj = (
                db.query(Score)
                .filter(Score.product_id == product_id)
                .order_by(Score.period_date.desc())
                .first()
            )
            previous_score = previous_score_obj.performance_score if previous_score_obj else None

            score_obj = ml_service.score_product(db, product_id, latest_period)
            recommendation_service.generate_for_product(db, product_id, latest_period, score_obj, features)
            recommendation_service.generate_alerts(db, product_id, latest_period, score_obj, features)

            # Calculate score change
            score_change = None
            if previous_score is not None:
                score_change = round(score_obj.performance_score - previous_score, 2)

            scored.append({
                "product_id":  product_id,
                "period_date": str(latest_period),
                "score":       round(score_obj.performance_score, 2),
                "tier":        score_obj.performance_tier,
                "previous_score": round(previous_score, 2) if previous_score else None,
                "score_change": score_change,
            })

        except Exception as e:
            db.rollback()
            logger.warning(f"Scoring failed for product_id={product_id}: {e}", exc_info=True)

    return scored


@router.post("/upload")
@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("super_admin", "data_engineer", "ml_engineer")),
):
    content = await file.read()

    # 1 — Parse file
    try:
        df = data_service.read_file(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2 — Validate
    validation = data_service.validate_dataframe(df, db)
    if not validation.is_valid:
        return {"status": "validation_failed", "validation": validation.model_dump()}

    # 3 — Bulk ingest
    success, errors, batch_id, newly_uploaded_product_ids = data_service.ingest_dataframe(
        df, db, source="upload", uploaded_by=current_user.id
    )
    if success == 0:
        return {
            "status": "no_rows_imported",
            "rows_imported": 0,
            "rows_failed": errors,
            "warnings": validation.warnings,
        }

    # 4 — AUTOMATICALLY run feature engineering + scoring + alerts + recommendations
    try:
        # Step 1: Process ALL validated raw data into features
        feature_count = feature_engineering_service.reprocess_all(db, product_id=None)
        logger.info(f"Auto-processing: Computed {feature_count} feature records")
        
        # Step 2: Score ALL products with processed features
        latest_q = (
            db.query(
                ProcessedFeatures.product_id,
                func.max(ProcessedFeatures.period_date).label("latest"),
            )
            .group_by(ProcessedFeatures.product_id)
        )
        
        latest_rows = latest_q.all()
        logger.info(f"Auto-processing: Found {len(latest_rows)} products with processed features")
        
        if latest_rows:
            product_ids_list = [r.product_id for r in latest_rows]
            period_dates = [r.latest for r in latest_rows]
            
            # Step 3: Score + alerts + recommendations
            scored_products = _run_scoring_pipeline(db, product_ids_list, period_dates)
            logger.info(f"Auto-processing: Scored {len(scored_products)} products")
        else:
            scored_products = []
            logger.warning("Auto-processing: No processed features found to score")
        
        return {
            "status":        "success",
            "filename":      file.filename,
            "rows_imported": success,
            "rows_failed":   errors,
            "batch_id":      batch_id,
            "newly_uploaded_product_ids": newly_uploaded_product_ids,
            "features_computed": feature_count,
            "products_scored": scored_products,
            "warnings":      validation.warnings,
            "message": (
                f"✓ Imported {success} row(s), computed features for {feature_count} record(s), "
                f"scored {len(scored_products)} product(s), generated alerts & recommendations. "
                f"Dashboard updated automatically!"
            ),
        }
    except Exception as e:
        logger.error(f"Auto-processing failed: {e}", exc_info=True)
        return {
            "status":        "uploaded_but_processing_failed",
            "filename":      file.filename,
            "rows_imported": success,
            "rows_failed":   errors,
            "batch_id":      batch_id,
            "newly_uploaded_product_ids": newly_uploaded_product_ids,
            "warnings":      validation.warnings,
            "message": (
                f"✓ Imported {success} row(s), but auto-processing failed. "
                f"Please run Feature Engineering manually from Settings page."
            ),
            "processing_error": str(e),
        }


@router.post("/validate")
@router.post("/validate/")
async def validate_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("super_admin", "data_engineer", "ml_engineer")),
):
    content = await file.read()
    try:
        df = data_service.read_file(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return data_service.validate_dataframe(df, db)


@router.post("/manual", response_model=RawDataResponse)
@router.post("/manual/", response_model=RawDataResponse)
async def create_manual_entry(
    payload: RawDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("super_admin", "data_engineer")),
):
    raw = RawData(
        **payload.model_dump(),
        source="manual",
        uploaded_by=current_user.id,
        is_validated=True,
    )
    db.add(raw)
    db.commit()
    db.refresh(raw)

    # Feature engineering + scoring for this single record
    feature_engineering_service.process_and_store(raw, db)
    _run_scoring_pipeline(db, [raw.product_id], [raw.period_date])
    return raw


@router.get("/raw", response_model=List[RawDataResponse])
@router.get("/raw/", response_model=List[RawDataResponse])
async def list_raw_data(
    product_id: Optional[int] = None,
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(RawData)
    if product_id:
        q = q.filter(RawData.product_id == product_id)
    return q.order_by(RawData.period_date.desc()).limit(limit).all()


@router.get("/features", response_model=List[ProcessedFeaturesResponse])
@router.get("/features/", response_model=List[ProcessedFeaturesResponse])
async def list_features(
    product_id: Optional[int] = None,
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(ProcessedFeatures)
    if product_id:
        q = q.filter(ProcessedFeatures.product_id == product_id)
    return q.order_by(ProcessedFeatures.period_date.desc()).limit(limit).all()


@router.post("/engineer")
@router.post("/engineer/")
async def run_feature_engineering(
    payload: Optional[dict] = None,
    product_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("super_admin", "data_engineer", "ml_engineer")),
):
    """Feature engineering endpoint - processes features, scores, generates alerts and recommendations."""
    
    # Step 1: Process features for ALL validated raw data
    try:
        count = feature_engineering_service.reprocess_all(db, product_id=None)
        logger.info(f"Feature engineering: Processed {count} feature records")
    except Exception as e:
        db.rollback()
        logger.error(f"Feature engineering failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Feature engineering failed: {e}")

    # Step 2: Find ALL products with processed features to score
    latest_q = (
        db.query(
            ProcessedFeatures.product_id,
            func.max(ProcessedFeatures.period_date).label("latest"),
        )
        .group_by(ProcessedFeatures.product_id)
    )
    
    latest_rows = latest_q.all()
    logger.info(f"Scoring: Found {len(latest_rows)} products with processed features")

    if not latest_rows:
        return {
            "message": "No processed features found. Upload data first.",
            "features_computed": 0,
            "products_scored": [],
        }

    product_ids_list = [r.product_id for r in latest_rows]
    period_dates = [r.latest for r in latest_rows]

    # Step 3: Score + generate recommendations + alerts
    scored_products = _run_scoring_pipeline(db, product_ids_list, period_dates)

    return {
        "message": f"Feature engineering completed. Scored {len(scored_products)} product(s).",
        "features_computed": count,
        "products_scored": scored_products,
    }
