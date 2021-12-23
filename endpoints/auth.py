from fastapi import APIRouter, Depends, HTTPException, status

from repositories.users import UserRepository
from models.token import Token, Login
from core.security import verify_password, create_access_token
from endpoints.depends import get_user_repository

router = APIRouter()


@router.post('/', response_model=Token)
async def login_user(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)

    if user is None or verify_password(login.password, user.hash_password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect email or password')

    return Token(
        access_token=create_access_token({'sub': user.email}),
        token_type='Bearer'
    )
