import pytest
from api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_successful_exchange(client):
    response = client.get("/api/exchange?source=USD&target=JPY&amount=$1,525")
    data = response.get_json()
    assert response.status_code == 200
    assert data["msg"] == "success"
    assert data["amount"] == "$170,496.53"


def test_invalid_amount_format_wo_dollar_sign(client):
    response = client.get("/api/exchange?source=USD&target=JPY&amount=123")
    data = response.get_json()
    assert response.status_code == 400
    assert data["msg"] == "bad"
    assert data["error_msg"] == "Invalid format for amount."


def test_invalid_amount_format_wo_comma(client):
    response = client.get("/api/exchange?source=USD&target=JPY&amount=$1123")
    data = response.get_json()
    assert response.status_code == 400
    assert data["msg"] == "bad"
    assert data["error_msg"] == "Invalid format for amount."


def test_invalid_currency_code_target(client):
    response = client.get("/api/exchange?source=USD&target=None&amount=$1,525")
    data = response.get_json()
    assert response.status_code == 400
    assert data["msg"] == "bad"
    assert data["error_msg"] == "Invalid currency code."


def test_invalid_currency_code_source(client):
    response = client.get("/api/exchange?source=None&target=JPY&amount=$1,525")
    data = response.get_json()
    assert response.status_code == 400
    assert data["msg"] == "bad"
    assert data["error_msg"] == "Invalid currency code."
