from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.receipts import router as receipts_router
from app.db.database import engine, Base
from app.models.receipt import Receipt
from app.api.routes.analytics import router as analytics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Receipt Analyzer",
    description="A FastAPI application for analyzing receipts using OCR and AI models.",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(receipts_router, prefix="/api/receipts", tags=["Receipts"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
