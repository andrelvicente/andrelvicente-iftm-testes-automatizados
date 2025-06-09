from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.client import Client


class ClientRepository:
    """
    Repository class for managing Client entities in the database.
    """

    @staticmethod
    def find_all(db: Session):
        """
        Retrieve all clients from the database.

        :param db: Database session.
        :return: List of Client objects.
        """
        try:
            return db.query(Client).all()
        except SQLAlchemyError as e:
            # Log the error or handle it appropriately
            print(f"Error retrieving all clients: {e}")
            return []

    @staticmethod
    def find_by_id(db: Session, client_id: int):
        """
        Retrieve a client by its ID.

        :param db: Database session.
        :param client_id: ID of the client.
        :return: Client object or None if not found.
        """
        try:
            return db.query(Client).filter(Client.id == client_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving client by ID: {e}")
            return None

    @staticmethod
    def find_by_income(db: Session, income: float):
        """
        Retrieve clients by their income.

        :param db: Database session.
        :param income: Income value to filter clients.
        :return: List of Client objects.
        """
        try:
            return db.query(Client).filter(Client.income == income).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving clients by income: {e}")
            return []

    @staticmethod
    def save(db: Session, client: Client):
        """
        Save a new client or update an existing client in the database.

        :param db: Database session.
        :param client: Client object to be saved.
        :return: Saved Client object.
        """
        try:
            db.add(client)
            db.commit()
            db.refresh(client)
            return client
        except SQLAlchemyError as e:
            db.rollback()  # Rollback in case of error
            print(f"Error saving client: {e}")
            return None

    @staticmethod
    def delete(db: Session, client: Client):
        """
        Delete a client from the database.

        :param db: Database session.
        :param client: Client object to be deleted.
        """
        try:
            db.delete(client)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error deleting client: {e}")
            
    @staticmethod
    def find_by_cpf(db: Session, cpf: str):
        """
        Retrieve a client by its CPF.

        :param db: Database session.
        :param cpf: CPF of the client.
        :return: Client object or None if not found.
        """
        try:
            return db.query(Client).filter(Client.cpf == cpf).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving client by CPF: {e}")
            return None