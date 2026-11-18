
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Online Shopping" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json) == 3


def test_single_product(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json["name"] == "Laptop"


def test_missing_product(client):
    response = client.get("/products/999")
    assert response.status_code == 404
