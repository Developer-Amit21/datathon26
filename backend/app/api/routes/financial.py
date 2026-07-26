from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.services.financial_service import FinancialCrimeService

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics")
def get_financial_analytics(db: Session = Depends(get_db)) -> dict:
    service = FinancialCrimeService(db)
    return service.get_financial_analytics()
