from fastapi import FastAPI
from app.db.session import Base, engine
from app.routes import client_routes

app = FastAPI(title="Client Service API")

Base.metadata.create_all(bind=engine)

app.include_router(client_routes.router, prefix="/clients", tags=["Clients"])
