from fastapi import APIRouter, Depends, HTTPException, status

from repositories.users import UserRepository
from models.token import Token, Login
from core.security import verify_password, create_access_token
from endpoints.depends import get_user_repository, get_permissions, get_authentication
from permissions.get_permissions import Permissions
from permissions.get_auth import Authentication


router = APIRouter()


@router.post('/', response_model=Token)
async def login_user(
        login: Login,
        users: UserRepository = Depends(get_user_repository),
        permissions: Permissions = Depends(get_permissions),
        auth: Authentication = Depends(get_authentication)
):
    user = await users.get_by_email(login.email)

    permissions.get_object(obj=user)
    auth.login_user(user, login.password)

    return Token(
        access_token=create_access_token({'sub': user.email}),
        token_type='Bearer'
    )
