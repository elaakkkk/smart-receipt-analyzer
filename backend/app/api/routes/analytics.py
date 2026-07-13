from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.repositories.analytics_repository import get_analytics_summary, get_charts_data, get_document_types_stats, get_validation_stats
from app.schemas.analytics_schema import AnalyticsChartsResponse, AnalyticsSummaryResponse, DocumentTypesStatsResponse, ValidationStatsResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.receipt_repository import get_receipts
from app.schemas.analytics_schema import (
    MerchantSpendingItem,
    MonthlySpendingItem,
    TopProductItem,
    CategorySpendingItem,
)
from app.services.analytics_service import (
    get_merchant_spending,
    get_monthly_spending,
    get_top_products,
    get_category_spending,
)

router = APIRouter()


@router.get("/merchant-spending", response_model=list[MerchantSpendingItem])
def merchant_spending(db: Session = Depends(get_db)):
    receipts = get_receipts(db, limit=1000)
    return get_merchant_spending(receipts)


@router.get("/monthly-spending", response_model=list[MonthlySpendingItem])
def monthly_spending(db: Session = Depends(get_db)):
    receipts = get_receipts(db, limit=1000)
    return get_monthly_spending(receipts)


@router.get("/top-products", response_model=list[TopProductItem])
def top_products(db: Session = Depends(get_db), limit: int = 10):
    receipts = get_receipts(db, limit=1000)
    return get_top_products(receipts, limit=limit)


@router.get("/category-spending", response_model=list[CategorySpendingItem])
def category_spending(db: Session = Depends(get_db)):
    receipts = get_receipts(db, limit=1000)
    return get_category_spending(receipts)

@router.get("/summary", response_model=AnalyticsSummaryResponse)
def read_analytics_summary(db: Session = Depends(get_db)):
    return get_analytics_summary(db)

@router.get("/document-types", response_model=DocumentTypesStatsResponse)
def read_document_types_stats(db: Session = Depends(get_db)):
    return get_document_types_stats(db)

@router.get("/validation", response_model=ValidationStatsResponse)
def read_validation_stats(db: Session = Depends(get_db)):
    return get_validation_stats(db)

@router.get("/charts", response_model=AnalyticsChartsResponse)
def read_analytics_charts(db: Session = Depends(get_db)):
    return get_charts_data(db)