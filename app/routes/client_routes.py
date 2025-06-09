from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.client import ClientOut, ClientCreate, ClientUpdate
from app.services.client_service import ClientService
from app.db.session import SessionLocal

router = APIRouter()

# Constants for messages
CLIENT_DELETED_MESSAGE = {"detail": "Client deleted"}
CLIENT_NOT_FOUND_MESSAGE = {"detail": "Client not found"}

def get_db():
    """
    Dependency to get the database session.
    Ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ClientOut])
def get_all_clients(db: Session = Depends(get_db)):
    """
    Retrieve all clients from the database.
    """
    return ClientService(db).get_all()

@router.get("/{id}", response_model=ClientOut)
def get_client_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a client by its ID.
    """
    client = ClientService(db).get_by_id(id)
    if not client:
        raise HTTPException(status_code=404, detail=CLIENT_NOT_FOUND_MESSAGE)
    return client

@router.get("/income/", response_model=List[ClientOut])
def get_clients_by_income(income: float = Query(...), db: Session = Depends(get_db)):
    """
    Retrieve clients filtered by income.
    """
    return ClientService(db).get_by_income(income)

@router.post("/", response_model=ClientOut, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """
    Create a new client in the database.
    """
    return ClientService(db).create(client)

@router.put("/{id}", response_model=ClientOut)
def update_client(id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    """
    Update an existing client by its ID.
    """
    updated_client = ClientService(db).update(id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail=CLIENT_NOT_FOUND_MESSAGE)
    return updated_client

@router.delete("/{id}", status_code=204)
def delete_client(id: int, db: Session = Depends(get_db)):
    """
    Delete a client by its ID.
    """
    if not ClientService(db).delete(id):
        raise HTTPException(status_code=404, detail=CLIENT_NOT_FOUND_MESSAGE)
    return CLIENT_DELETED_MESSAGE