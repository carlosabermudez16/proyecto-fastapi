
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

from app.core.exceptions import (
    CreateModelError,
    DuplicateRegisterError,
    PersistenceError,
)


def get_user_by_id(model_type:DeclarativeBase, session:Session, user_id:int):
    try:
        statement = select(model_type).where(model_type.id == user_id)
        return session.execute(statement).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e

def get_user_by_email(model_type:DeclarativeBase, session:Session, email:str):
    try:
        statement = select(model_type).where(model_type.email == email)
        return session.execute(statement).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e

def get_users(model_type:DeclarativeBase, session:Session, skip:int=0, limit:int=100) -> list:
    try:
        statement = select(model_type).offset(skip).limit(limit)
        return session.execute(statement).scalars().all()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e



def create_user(session:Session, db_data: DeclarativeBase):
    try:
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    except IntegrityError as e:
        session.rollback()
        raise DuplicateRegisterError("Database error") from e
    except SQLAlchemyError as e:
        session.rollback()
        raise PersistenceError("Database error") from e
    except Exception as e:
        raise CreateModelError("Error creating user") from e

