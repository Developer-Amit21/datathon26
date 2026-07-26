from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.domain import CaseRecord

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def summary(db: Session = Depends(get_db)) -> dict:
    records = db.query(CaseRecord).all()
    return {
        "total_cases": len(records),
        "high_risk_cases": sum(1 for item in records if item.risk_score >= 0.8),
        "repeat_offenders": sum(1 for item in records if item.is_repeat_offender),
        "districts": sorted({item.district for item in records}),
    }
