from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.services.ml_service import MLAnalyticsService

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/hotspots")
def forecast_hotspots(
    district: str = Query("Bangalore", description="District name"),
    db: Session = Depends(get_db)
) -> dict:
    service = MLAnalyticsService(db)
    return service.forecast_hotspots(district=district)


@router.get("/risk/{offender_id}")
def predict_offender_risk(
    offender_id: int,
    db: Session = Depends(get_db)
) -> dict:
    service = MLAnalyticsService(db)
    return service.predict_recidivism_risk(offender_id=offender_id)
