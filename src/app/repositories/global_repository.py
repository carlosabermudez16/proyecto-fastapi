
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import PersistenceError
from app.database.session import base


def get_register_by_id(model_type:base, session:Session, table_id:int):
    try:
        return session.query(model_type).filter(model_type.id == table_id).one_or_none()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e


def get_all_register(model_type:base, session:Session, skip:int=0, limit:int=100) -> list:
    try:
        return session.query(model_type).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e



def create_register(session:Session, data: dict[str,any]):
    try:
        session.add(data)
        session.commit()
        session.refresh()
        return data
    except SQLAlchemyError as e:
        raise PersistenceError("Error to create new register") from e

