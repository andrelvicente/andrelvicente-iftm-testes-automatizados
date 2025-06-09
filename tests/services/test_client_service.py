from unittest.mock import MagicMock
from fastapi import HTTPException
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService
from app.schemas.client import ClientCreate, ClientUpdate
from app.models.client import Client
import pytest

# Helper function to set up mocks
def setup_mocks():
    mock_db = MagicMock()
    mock_repository = MagicMock()
    ClientService.db = mock_db
    return mock_db, mock_repository

# Test file: tests/services/test_client_service.py

def test_get_all():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_all.return_value = ["client1", "client2"]
    ClientRepository.find_all = mock_repository.find_all

    service = ClientService(mock_db)
    result = service.get_all()

    assert result == ["client1", "client2"]
    mock_repository.find_all.assert_called_once_with(mock_db)

def test_get_by_id():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_id.return_value = {"id": 1, "name": "John Doe"}
    ClientRepository.find_by_id = mock_repository.find_by_id

    service = ClientService(mock_db)
    result = service.get_by_id(1)

    assert result == {"id": 1, "name": "John Doe"}
    mock_repository.find_by_id.assert_called_once_with(mock_db, 1)

def test_get_by_id_not_found():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_id.return_value = None
    ClientRepository.find_by_id = mock_repository.find_by_id

    service = ClientService(mock_db)

    with pytest.raises(HTTPException) as exc_info:
        service.get_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Client not found"
    mock_repository.find_by_id.assert_called_once_with(mock_db, 1)

def test_create():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_cpf.return_value = None
    mock_repository.save.return_value = {"id": 1, "name": "John Doe"}
    ClientRepository.find_by_cpf = mock_repository.find_by_cpf
    ClientRepository.save = mock_repository.save

    service = ClientService(mock_db)
    client_data = ClientCreate(
        cpf="12345678900",
        name="John Doe",
        income=5000,
        birth_date="1990-01-01",
        children=2
    )
    result = service.create(client_data)

    assert result == {"id": 1, "name": "John Doe"}
    mock_repository.find_by_cpf.assert_called_once_with(mock_db, "12345678900")
    mock_repository.save.assert_called_once()

def test_create_existing_client():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_cpf.return_value = {"id": 1, "name": "John Doe"}
    ClientRepository.find_by_cpf = mock_repository.find_by_cpf

    service = ClientService(mock_db)
    client_data = ClientCreate(
        cpf="12345678900",
        name="John Doe",
        income=5000,
        birth_date="1990-01-01",
        children=2
    )

    with pytest.raises(HTTPException) as exc_info:
        service.create(client_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "CPF already exists"
    mock_repository.find_by_cpf.assert_called_once_with(mock_db, "12345678900")

def test_update():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_id.return_value = Client(id=1, name="John Doe", cpf="12345678900", income=5000, birth_date="1990-01-01", children=2)
    mock_repository.save.return_value = {"id": 1, "name": "John Smith"}
    ClientRepository.find_by_id = mock_repository.find_by_id
    ClientRepository.save = mock_repository.save

    service = ClientService(mock_db)
    client_data = ClientUpdate(
        name="John Smith",
        income=6000,
        cpf="12345678900",
        birth_date="1990-01-01",
        children=2
    )
    result = service.update(1, client_data)

    assert result == {"id": 1, "name": "John Smith"}
    mock_repository.find_by_id.assert_called_once_with(mock_db, 1)
    mock_repository.save.assert_called_once()

def test_update_not_found():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_id.return_value = None
    ClientRepository.find_by_id = mock_repository.find_by_id

    service = ClientService(mock_db)
    client_data = ClientUpdate(
        name="John Smith",
        income=6000,
        cpf="12345678900",
        birth_date="1990-01-01",
        children=2
    )

    with pytest.raises(HTTPException) as exc_info:
        service.update(1, client_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Client not found"
    mock_repository.find_by_id.assert_called_once_with(mock_db, 1)

def test_delete():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_id.return_value = Client(id=1, name="John Doe", cpf="12345678900", income=5000)
    mock_repository.delete.return_value = None
    ClientRepository.find_by_id = mock_repository.find_by_id
    ClientRepository.delete = mock_repository.delete

    service = ClientService(mock_db)
    service.delete(1)

    mock_repository.find_by_id.assert_called_once_with(mock_db, 1)
    mock_repository.delete.assert_called_once_with(mock_db, mock_repository.find_by_id.return_value)

def test_delete_not_found():
    mock_db, mock_repository = setup_mocks()
    mock_repository.find_by_id.return_value = None
    ClientRepository.find_by_id = mock_repository.find_by_id

    service = ClientService(mock_db)

    with pytest.raises(HTTPException) as exc_info:
        service.delete(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Client not found"
    mock_repository.find_by_id.assert_called_once_with(mock_db, 1)