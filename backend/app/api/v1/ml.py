from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User
from app.models.ml_models import ModelRegistry
from app.models.product import Product
from app.schemas.ml import (
    PredictRequest, PredictResponse, SimilarProductResponse,
)
from app.services.ml_service import ml_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ml", tags=["ML / Predictions"])


@router.post("/predict", response_model=PredictResponse)
@router.post("/predict/", response_model=PredictResponse)
async def predict(
    payload: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("super_admin", "ml_engineer", "product_manager", "executive_management")),
):
    """Predict score for a product using trained models."""
    try:
        result = ml_service.predict(db, payload.product_id, payload.features)
        return PredictResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/similar/{product_id}", response_model=List[SimilarProductResponse])
@router.get("/similar/{product_id}/", response_model=List[SimilarProductResponse])
async def get_similar_products(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(
        "super_admin", "ml_engineer", "product_manager", "executive_management"
    )),
):
    """Get similar products based on KNN similarity model."""
    from app.models.ml_models import SimilarProduct
    from app.models.product import Product

    similar = (
        db.query(SimilarProduct)
        .filter(SimilarProduct.product_id == product_id)
        .order_by(SimilarProduct.similarity_score.desc())
        .all()
    )
    result = []
    for s in similar:
        sp = db.query(Product).filter(Product.id == s.similar_product_id).first()
        result.append(SimilarProductResponse(
            product_id=s.product_id,
            similar_product_id=s.similar_product_id,
            similar_product_name=sp.name if sp else "N/A",
            similarity_score=s.similarity_score,
            cluster_id=s.cluster_id,
        ))
    return result


@router.get("/predictions/bulk")
@router.get("/predictions/bulk/")
async def get_bulk_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and return 3-month forward predictions for all products.
    """
    try:
        all_products = db.query(Product).all()
        product_ids = [p.id for p in all_products]
        
        if not product_ids:
            return []
        
        results = []
        for product_id in product_ids:
            try:
                predictions = ml_service.predict_3months(db, product_id)
                results.extend(predictions)
            except Exception as e:
                logger.warning(f"Prediction failed for product {product_id}: {e}")
                continue
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/{product_id}")
@router.get("/predictions/{product_id}/")
async def get_3month_predictions(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and return 3-month forward predictions for a product.
    Uses momentum-based projection on the latest feature vector.
    """
    try:
        predictions = ml_service.predict_3months(db, product_id)
        return {"product_id": product_id, "predictions": predictions}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
