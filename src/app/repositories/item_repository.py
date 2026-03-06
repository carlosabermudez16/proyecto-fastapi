
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

from app.core.exceptions import (
    CreateModelError,
    DeleteModelError,
    PersistenceError,
    UpdateModelError,
)


def get_item_by_id(model_type:DeclarativeBase, session:Session, item_id:int):
    try:
        statement = select(model_type).where(model_type.id == item_id)
        return session.execute(statement).first()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e

def get_item_by_title(model_type:DeclarativeBase, session:Session, title:str):
    try:
        statement = select(model_type).where(model_type.title == title)
        return session.execute(statement).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e

def get_items(model_type:DeclarativeBase, session:Session, user_id:int, skip:int=0, limit:int=100) -> list:
    try:
        statement = select(model_type).where(model_type.user_id==user_id).offset(skip).limit(limit)
        return session.execute(statement).scalars().all()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e


def create_item(session:Session, db_data: dict[str,any]):
    try:
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    except SQLAlchemyError as e:
        session.rollback()
        raise PersistenceError("Error to create new item") from e
    except Exception as e:
        raise CreateModelError("Error creating item") from e

def update_item(session: Session, db_data: dict[str,any]):
    try:
        session.commit()
        session.refresh(db_data)
        return db_data
    except Exception as e:
        raise UpdateModelError("Error update item") from e

def delete_item(model_type:DeclarativeBase, session: Session):
    try:
        session.delete(model_type)
        session.commit()
    except SQLAlchemyError as e:
        raise PersistenceError(f"Error delete register {model_type.id} to {model_type}") from e
    except Exception as e:
        raise DeleteModelError("Error deleting item") from e



