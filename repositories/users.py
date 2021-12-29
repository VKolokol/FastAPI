from typing import List

from fastapi import Query

from db.users import users
from models.users import User, UserIn
from repositories.base import BaseRepository
from interfaces.repository import CRUDRepository
from core.security import hash_password


class UserRepository(BaseRepository, CRUDRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Query]:
        query = users.select().where(users.c.is_active == True).limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_object(self, user_id: int) -> Query:
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        obj = self.get_value(u)

        query = users.insert().values(**obj.dict())
        obj.id = await self.database.execute(query)

        return obj

    async def update(self, user_id: int, u: UserIn):
        obj = self.get_value(u, update=True)

        query = users.update().where(users.c.id == user_id).values(**obj.dict())
        await self.database.execute(query)

        return await self.get_object(user_id)

    async def remove(self, user_id):
        query = users.update().where(users.c.id == user_id).values({'is_active': False})
        return await self.database.execute(query)

    async def get_by_email(self, email: str):
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)

        if user is None:
            return None

        return User.parse_obj(user)

    @staticmethod
    def get_value(u, update=False):
        user = User(
            **u.dict(),
            hash_password=hash_password(u.password)
        )
        del user.id

        if update:
            del user.created_at
        return user
