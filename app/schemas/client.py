from pydantic import BaseModel
from datetime import date

class ClientBase(BaseModel):
    name: str
    cpf: str
    income: float
    birth_date: date
    children: int

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
