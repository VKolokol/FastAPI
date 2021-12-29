from typing import List

from fastapi import APIRouter, Depends, Response, status

from repositories.users import UserRepository
from permissions.get_permissions import Permissions
from models.users import User, UserIn
from endpoints.depends import get_user_repository, get_current_user, get_permissions
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
async def create_user(
        user: UserIn,
        users: UserRepository = Depends(get_user_repository)
):
    return await users.create(u=user)


@router.patch('/{user_id}', response_model=ViewUser)
async def update_user(
        user_id: int,
        user_data: UserIn,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user),
        permissions: Permissions = Depends(get_permissions)
):
    user = await users.get_object(user_id=user_id)

    permissions.get_permission(obj=user, user=current_user, user_id=user_id)

    return await users.update(user_id=user_id, u=user_data)


@router.delete('/{user_id}')
async def deactivate_user(
        user_id: int,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user),
        permissions: Permissions = Depends(get_permissions)
):
    user = await users.get_object(user_id=user_id)

    permissions.get_permission(obj=user, user=current_user, user_id=user_id)

    await users.remove(user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
