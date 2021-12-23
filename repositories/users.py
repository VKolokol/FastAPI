import datetime
from typing import List

from fastapi import Query

from db.users import users
from models.users import User, UserIn
from repositories.base import BaseRepository
from core.security import hash_password


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Query]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id_: int) -> Query:
        query = users.select().where(users.c.id == id_)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        values, user = self.get_values(u)
        values.pop('id', None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def update(self, id_: int, u: UserIn):
        values, user = self.get_values(u)
        values.pop('id', None)
        values.pop('created_at', None)
        query = users.update().where(users.c.id == id_).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(id_)

    async def get_by_email(self,  email: str):
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    @staticmethod
    def get_values(u):
        user = User(
            name=u.name,
            email=u.email,
            hash_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        return {**user.dict()}, user
