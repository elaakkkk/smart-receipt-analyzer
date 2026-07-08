from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.repositories.analytics_repository import get_analytics_summary, get_document_types_stats, get_validation_stats
from app.schemas.analytics_schema import AnalyticsSummaryResponse, DocumentTypesStatsResponse, ValidationStatsResponse

router = APIRouter()
@router.get("/summary", response_model=AnalyticsSummaryResponse)
def read_analytics_summary(db: Session = Depends(get_db)):
    return get_analytics_summary(db)

@router.get("/document-types", response_model=DocumentTypesStatsResponse)
def read_document_types_stats(db: Session = Depends(get_db)):
    return get_document_types_stats(db)

@router.get("/validation", response_model=ValidationStatsResponse)
def read_validation_stats(db: Session = Depends(get_db)):
    return get_validation_stats(db)