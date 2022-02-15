from fastapi import Depends, HTTPException, status

from repositories.users import UserRepository
from repositories.jobs import JobRepository
from repositories.proposals import ProposalRepository
from models.users import User
from db.base import database
from core.security import JWTBearer, decode_access_token
from permissions import get_permissions as permission, get_auth as auth


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_job_repository() -> JobRepository:
    return JobRepository(database)


def get_proposal_repository() -> ProposalRepository:
    return ProposalRepository(database)


def get_permissions() -> permission.Permissions:
    return permission.Permissions()


def get_authentication() -> auth.Authentication:
    return auth.Authentication()


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer())
) -> User:
    cred_exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    not_user = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exp

    email: str = payload.get('sub')
    if email is None:
        raise cred_exp

    user = await users.get_by_email(email=email)

    if user is None:
        raise cred_exp

    if user.is_active:
        return user
    else:
        raise not_user
