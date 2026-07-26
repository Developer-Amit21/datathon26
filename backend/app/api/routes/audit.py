from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.services.security_service import SecurityGovernanceService

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/logs")
def get_audit_logs(db: Session = Depends(get_db)) -> dict:
    service = SecurityGovernanceService(db)
    return {"audit_trail": service.get_audit_trail()}
