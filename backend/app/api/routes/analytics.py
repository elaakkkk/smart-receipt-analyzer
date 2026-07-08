from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.repositories.analytics_repository import get_analytics_summary
from app.schemas.analytics_schema import AnalyticsSummaryResponse

router = APIRouter()
@router.get("/summary", response_model=AnalyticsSummaryResponse)
def read_analytics_summary(db: Session = Depends(get_db)):
    return get_analytics_summary(db)