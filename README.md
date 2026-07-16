# Smart Receipt Analyzer

Smart Receipt Analyzer is a full-stack AI and data analytics project that extracts, structures, validates and analyzes receipt data from uploaded documents.

The goal of this project is to demonstrate a complete engineering workflow:

- OCR document processing
- Structured JSON extraction
- Business validation
- Backend API with FastAPI
- Frontend dashboard with Angular
- Analytics and data visualization
- Unit testing
- Clean project architecture

---

## Project overview

Users can upload a receipt image or PDF. The backend extracts the raw text, classifies the document, converts the content into structured JSON, validates the extracted data, stores the result, and exposes analytics endpoints.

The frontend displays the processed receipts and provides an analytics workspace with KPIs, spending trends, category distribution, merchant ranking, product analysis and data quality indicators.

---

## Main features

### Receipt processing

- Upload receipt image or PDF
- Validate uploaded file format
- Extract raw text with OCR
- Classify document type
- Extract structured receipt data
- Validate extracted JSON
- Store receipt data in database
- Review and correct extracted information

### Analytics

- Total spending
- Number of receipts
- Average basket
- Top merchant
- Top category
- Monthly spending trend
- Category distribution
- Merchant ranking
- Product-level analysis
- Data quality score
- Dynamic filter options

### Frontend

- Modern Angular interface
- Dashboard page
- Receipts list
- Receipt detail page
- Human review page
- Analytics workspace
- Responsive UI

### Backend

- FastAPI REST API
- SQLAlchemy models
- Repository/service architecture
- OCR service layer
- Business validation layer
- Analytics service layer
- Unit tests with pytest

---

## Tech stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL or SQLite
- Pytest
- OCR engine: Tesseract / future OCR engines

### Frontend

- Angular
- TypeScript
- HTML
- CSS
- Standalone components

---

## Architecture

```text
smart-receipt-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ocr/
│   │   │   ├── analytics_service.py
│   │   │   ├── business_validation_service.py
│   │   │   ├── classification_service.py
│   │   │   └── extraction_service.py
│   │   └── main.py
│   │
│   └── app/tests/
│
├── frontend/
│   └── src/app/
│       ├── core/
│       ├── pages/
│       └── shared/
│
└── README.md

---

## Data Pipeline
Upload document
      ↓
File validation
      ↓
OCR text extraction
      ↓
Document classification
      ↓
Structured JSON extraction
      ↓
JSON schema validation
      ↓
Business validation
      ↓
Database storage
      ↓
Analytics aggregation
      ↓
Angular dashboard

--- 

## Backend API 

### Endpoints

**Health**

- `GET /api/health`: Health check

**Receipt endpoints**

- `POST /api/receipts/upload`: Upload a receipt image or PDF
- `GET /api/receipts`: Get all receipts
- `GET /api/receipts/{id}`: Get a specific receipt
- `PATCH /api/receipts/{receipt_id}/structured-data`: Update structured data
- `DELETE /api/receipts/{id}`: Delete a receipt

**Analytics endpoints**

- `GET /api/analytics/summary`: Get overall analytics summary
- `GET /api/analytics/document-types`: Get document type distribution
- `GET /api/analytics/validation`: Get validation statistics
- `GET /api/analytics/charts`: Get chart data for visualizations
- `GET /api/analytics/merchant-spending`: Get merchant spending
- `GET /api/analytics/monthly-spending`: Get monthly spending
- `GET /api/analytics/top-products`: Get top products
- `GET /api/analytics/category-spending`: Get category spending
- `GET /api/analytics/insights`: Get detailed analytics insights

## Analytics layer
The project includes a dedicated analytics layer that transforms OCR-extracted receipt data into business insights.
Tested analytics features :
- Merchant spending aggregation
- Monthly spending trends
- Category-level spending distribution
- Product ranking by total spending
- Filter option generation
- Data quality scoring

---

Run analytics tests:
``` bash
cd backend
pytest app/tests/test_services_analytics.py -v 
```

## Run the project locally
1. Backend
``` bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on:
- `http://127.0.0.1:8000`
API documentation:
- `http://127.0.0.1:8000/docs`

2. Frontend
``` bash
cd frontend
npm install 
ng serve 
```

Frontend runs on:
```http://localhost:4200```

---

## Why this project matters
This project demonstrates practical full-stack engineering skills:
- Building a REST API with FastAPI
- Structuring a backend with services, repositories and schemas
- Processing real-world unstructured documents
- Transforming OCR output into structured data
- Validating data quality
- Creating analytics-ready endpoints
- Building a modern Angular frontend
- Writing unit tests for business logic

It combines software engineering, AI document processing and data analytics in one complete portfolio project.

---
## Continuous integration

The backend test suite is automatically executed with GitHub Actions on every push and pull request.

The CI pipeline checks:

- Python dependency installation
- OCR system dependency installation
- Backend unit tests
- Analytics service tests

Workflow file:

```text
.github/workflows/backend-ci.yml

The frontend build is also checked automatically with GitHub Actions.

Frontend CI checks:

- Node.js dependency installation
- Angular production build

Workflow file:

```text
.github/workflows/frontend-ci.yml