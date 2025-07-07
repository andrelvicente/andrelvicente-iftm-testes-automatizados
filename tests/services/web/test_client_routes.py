import pytest
from fastapi.testclient import TestClient
from datetime import date
from unittest.mock import patch
from app.main import app
from app.routes.client_routes import get_db
from app.schemas.client import ClientOut

client = TestClient(app)

# Fixture para sobrescrever a dependência do banco
@pytest.fixture(autouse=True, scope="module")
def override_db():
    class DummyDB:
        pass
    app.dependency_overrides[get_db] = lambda: (yield DummyDB())
    yield
    app.dependency_overrides.clear()

# Fixtures para dados de clientes
@pytest.fixture
def client_out():
    return ClientOut(
        id=1, name="Mocked Client", cpf="11111111111",
        income=5000.0, birth_date=date.today(), children=2
    )

@pytest.fixture
def client_create_data():
    return {
        "name": "Carlos Teste",
        "cpf": "12345678901",
        "income": 3000.0,
        "birth_date": "1990-01-01T00:00:00Z",
        "children": 2
    }

@pytest.fixture
def client_update_data():
    return {
        "name": "Updated",
        "cpf": "98765432100",
        "income": 9999.0,
        "birth_date": "1995-05-05T00:00:00Z",
        "children": 3
    }

def test_get_all_clients_returns_clients(client_out):
    with patch("app.services.client_service.ClientService.get_all", return_value=[client_out]):
        response = client.get("/clients/")
    assert response.status_code == 200
    assert response.json()[0]["name"] == client_out.name

def test_get_client_by_id_found(client_out):
    with patch("app.services.client_service.ClientService.get_by_id", return_value=client_out):
        response = client.get("/clients/1")
    assert response.status_code == 200
    assert response.json()["name"] == client_out.name

def test_get_client_by_id_not_found():
    with patch("app.services.client_service.ClientService.get_by_id", return_value=None):
        response = client.get("/clients/999")
    assert response.status_code == 404
    assert response.json()["detail"]["detail"] == "Client not found"

def test_create_client_success(client_create_data):
    client_out = ClientOut(
        id=3, name=client_create_data["name"], cpf=client_create_data["cpf"],
        income=client_create_data["income"], birth_date=date.today(), children=client_create_data["children"]
    )
    with patch("app.services.client_service.ClientService.create", return_value=client_out):
        response = client.post("/clients/", json=client_create_data)
    assert response.status_code == 201
    assert response.json()["name"] == client_create_data["name"]

def test_update_client_success(client_update_data):
    client_out = ClientOut(
        id=1, name=client_update_data["name"], cpf=client_update_data["cpf"],
        income=client_update_data["income"], birth_date=date.today(), children=client_update_data["children"]
    )
    with patch("app.services.client_service.ClientService.update", return_value=client_out):
        response = client.put("/clients/1", json=client_update_data)
    assert response.status_code == 200
    assert response.json()["name"] == client_update_data["name"]

def test_update_client_not_found(client_update_data):
    with patch("app.services.client_service.ClientService.update", return_value=None):
        response = client.put("/clients/999", json=client_update_data)
    assert response.status_code == 404

def test_delete_client_success():
    with patch("app.services.client_service.ClientService.delete", return_value=True):
        response = client.delete("/clients/1")
    assert response.status_code == 204

def test_delete_client_not_found():
    with patch("app.services.client_service.ClientService.delete", return_value=False):
        response = client.delete("/clients/999")
    assert response.status_code == 404

def test_get_clients_by_income():
    income = 5000.0
    client_out = ClientOut(
        id=10, name="Salary Guy", cpf="123", income=income, birth_date=date.today(), children=0
    )
    with patch("app.services.client_service.ClientService.get_by_income", return_value=[client_out]):
        response = client.get(f"/clients/income/?income={income}")
    assert response.status_code == 200
    assert response.json()[0]["income"] == income
    
def test_find_client_by_cpf(client_out):
    cpf = client_out.cpf
    with patch("app.services.client_service.ClientService.find_by_cpf", return_value=client_out):
        response = client.get(f"/clients/cpf/{cpf}")
    assert response.status_code == 200
    assert response.json()["cpf"] == cpf

def test_find_client_by_cpf_not_found():
    cpf = "00000000000"
    with patch("app.services.client_service.ClientService.find_by_cpf", return_value=None):
        response = client.get(f"/clients/cpf/{cpf}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"
