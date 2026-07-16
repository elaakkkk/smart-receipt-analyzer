from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_analytics_summary():
    response = client.get("/api/analytics/summary")

    assert response.status_code == 200

    data = response.json()
    assert "total_receipts" in data
    assert "valid_receipts" in data
    assert "invalid_receipts" in data
    assert "unknown_documents" in data
    assert "receipt_documents" in data
    assert "invoice_documents" in data


def test_get_document_types_stats():
    response = client.get("/api/analytics/document-types")

    assert response.status_code == 200

    data = response.json()
    assert "unknown" in data
    assert "receipt" in data
    assert "invoice" in data


def test_get_validation_stats():
    response = client.get("/api/analytics/validation")

    assert response.status_code == 200

    data = response.json()
    assert "valid" in data
    assert "invalid" in data
    assert "with_warnings" in data
    assert "without_warnings" in data


def test_get_charts_data():
    response = client.get("/api/analytics/charts")

    assert response.status_code == 200

    data = response.json()
    assert "document_types" in data
    assert "validation_status" in data
    assert isinstance(data["document_types"], list)
    assert isinstance(data["validation_status"], list)

def test_get_receipts_list():
    response = client.get("/api/receipts/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_analytics_insights():
    response = client.get("/api/analytics/insights")

    assert response.status_code == 200

    data = response.json()

    assert "kpis" in data
    assert "monthly_spending" in data
    assert "merchant_spending" in data
    assert "category_spending" in data
    assert "top_products" in data
    assert "data_quality" in data
    assert "filter_options" in data

    assert "total_spent" in data["kpis"]
    assert "receipt_count" in data["kpis"]
    assert "average_basket" in data["kpis"]

    assert "score" in data["data_quality"]
    assert "label" in data["data_quality"]

    assert "merchants" in data["filter_options"]
    assert "categories" in data["filter_options"]

def test_upload_invalid_file_type():
    files = {
        "file": (
            "test.txt",
            b"This is not a valid receipt file.",
            "text/plain",
        )
    }

    response = client.post("/api/receipts/upload", files=files)

    assert response.status_code == 400