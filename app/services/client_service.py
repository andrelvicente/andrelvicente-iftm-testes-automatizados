from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.repositories.client_repository import ClientRepository

class ClientService:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return ClientRepository.find_all(self.db)

    def get_by_id(self, id: int):
        client = ClientRepository.find_by_id(self.db, id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    def get_by_income(self, income: float):
        return ClientRepository.find_by_income(self.db, income)

    def create(self, client_data: ClientCreate):
        existing_client = ClientRepository.find_by_cpf(self.db, client_data.cpf)
        if existing_client:
            raise HTTPException(status_code=400, detail="CPF already exists")
        client = Client(**client_data.dict())
        return ClientRepository.save(self.db, client)

    def update(self, id: int, client_data: ClientUpdate):
        client = ClientRepository.find_by_id(self.db, id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        for attr, value in client_data.dict().items():
            setattr(client, attr, value)
        return ClientRepository.save(self.db, client)

    def delete(self, id: int):
        client = ClientRepository.find_by_id(self.db, id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        ClientRepository.delete(self.db, client)
        
    def find_by_cpf(self, cpf: str):
        client = ClientRepository.find_by_cpf(self.db, cpf)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client