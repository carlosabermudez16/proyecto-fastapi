from pydantic import ValidationError
from sqlalchemy.orm import DeclarativeBase, Session

from app.core.exceptions import ModelSerializationError
from app.core.security import hash_password
from app.database.session import base
from app.repositories.user_repository import create_user, get_users
from app.schemas.users import UserCreate


def read_users_service(
    model_type: base,
    session: Session,
    offset: int,
    limit: int,
):
    return get_users(
        model_type=model_type, session=session, skip=offset, limit=limit
    )

def create_user_service(model_type:DeclarativeBase,session:Session,user_data:UserCreate):
    try:
        user_dict = user_data.model_dump()
        user_dict["password"] = hash_password(user_data.password)
        db_user = model_type(**user_dict)
    except (ValidationError, TypeError, ValueError,AttributeError) as e:
        raise ModelSerializationError("Error converting schema to model") from e
    
    return create_user(session=session,db_data=db_user)


