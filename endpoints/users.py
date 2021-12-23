from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from repositories.users import UserRepository
from models.users import User, UserIn
from endpoints.depends import get_user_repository, get_current_users
from schemas.users import ViewUser

router = APIRouter()


@router.get('/', response_model=List[ViewUser])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0
):
    return await users.get_all(limit=limit, skip=skip)


@router.post('/', response_model=ViewUser)
async def create(
        user: UserIn,
        users: UserRepository = Depends(get_user_repository)
):
    return await users.create(u=user)


@router.put('/', response_model=ViewUser)
async def update(
        id: int,
        user: UserIn,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_users)
):
    old_user = await users.get_by_id(id_=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    return await users.update(id_=id, u=user)
