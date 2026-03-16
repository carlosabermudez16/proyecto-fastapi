from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies.session_dep import SessionDep
from app.models.user import User
from app.repositories.user_repository import get_user_by_email, get_user_by_id
from app.schemas.users import UserCreate, UserPublicScheme, UserScheme
from app.services.user_service import create_user_service, read_users_service

router = APIRouter(prefix="/api/v1", tags=["User V1"])

@router.get("/users/", response_model=list[UserScheme], status_code=status.HTTP_200_OK)
async def read_users(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return read_users_service(
        model_type=User,
        session=session,
        offset=offset,
        limit=limit
    )

@router.get("/user/public/{user_id}", response_model=UserPublicScheme, status_code=status.HTTP_200_OK)
async def read_user(
    user_id:int,
    session: SessionDep,
):
    return get_user_by_id(model_type=User, session=session,user_id=user_id)

@router.post("/user/", response_model=UserScheme, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: SessionDep
):
    db_user = get_user_by_email(model_type=User,session=session,email=user_data.email)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email already registered"
        )

    return create_user_service(model_type=User,session=session,user_data=user_data)

