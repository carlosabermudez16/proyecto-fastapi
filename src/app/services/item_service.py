from fastapi.exceptions import ValidationException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ModelSerializationError,
    RegisterNotFoundError,
    UpdateModelError,
)
from app.database.session import base
from app.repositories.item_repository import (
    create_item,
    delete_item,
    get_item_by_id,
    get_items,
    update_item,
)
from app.schemas.items import ItemCreate


def read_items_service(
    model_type: base,
    session: Session,
    offset: int,
    limit: int,
):
    return get_items(
        model_type=model_type, session=session, skip=offset, limit=limit
    )

def create_item_service(model_type:base,session:Session, item_data:ItemCreate):
    try:
        item_dict = item_data.model_dump()
        db_item = model_type(**item_dict)
    except (ValidationError, TypeError, ValueError) as e:
        raise ModelSerializationError("Error converting schema to model") from e

    return create_item(session=session,db_data=db_item)

def update_item_service(
    model_type: base, session: Session, item_id: int, data: dict[str,any]
):
    db_item = get_item_by_id(model_type=model_type,session=session,item_id=item_id)
    if not db_item:
        raise RegisterNotFoundError()

    try:
        for key, value in data.items():
            setattr(db_item, key, value)
    except ValidationException as e:
        raise UpdateModelError("Error update to serialize model") from e

    return update_item(session=session,db_data=db_item)

def delete_item_service(model_type: base, session: Session, item_id: int):
    db_item = get_item_by_id(model_type=model_type,session=session,item_id=item_id)
    if not db_item:
        raise RegisterNotFoundError()

    return delete_item(model_type=db_item, session=session)

