from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies.session_dep import SessionDep
from app.models.item import Item
from app.repositories.item_repository import get_item_by_title
from app.schemas.items import ItemCreate, ItemScheme
from app.services.item_service import create_item_service, get_items

router = APIRouter(prefix="/api/v1", tags=["Items V1"])

@router.get("/items/{user_id}", response_model=list[ItemScheme], status_code=status.HTTP_200_OK)
async def read_items(
    user_id: int,
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_items(
        user_id=user_id,
        model_type=Item,
        session=session,
        skip=offset,
        limit=limit
    )

@router.post("/item/", response_model=ItemScheme, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    session: SessionDep
):
    db_item = get_item_by_title(model_type=Item,session=session,title=item_data.title)
    
    if db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Title already registered"
        )

    return create_item_service(model_type=Item,session=session,item_data=item_data)