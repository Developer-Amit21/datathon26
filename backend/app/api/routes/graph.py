from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.services.graph_service import GraphAnalyticsService

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/network")
def get_network(db: Session = Depends(get_db)) -> dict:
    service = GraphAnalyticsService(db)
    return service.get_criminal_network()
