from sqlalchemy import Column, Integer, String, Float, Date
from app.db.session import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    income = Column(Float, nullable=False)
    birth_date = Column(Date, nullable=False)
    children = Column(Integer, nullable=False)
