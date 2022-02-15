import datetime

from typing import List
from fastapi import Query
from sqlalchemy import select

from models.jobs import Jobs, JobIn
from db.jobs import jobs
from db.users import users
from repositories.base import BaseRepository
from interfaces.repository import CRUDRepository


class JobRepository(BaseRepository, CRUDRepository):
    async def create(self, user_id: int, job: JobIn):
        obj = self.get_value(job=job, user_id=user_id)

        query = jobs.insert().values(**obj.dict())
        obj.id = await self.database.execute(query)

        return obj

    async def update(self, job_id: int, job: JobIn):
        obj = self.get_value(job=job)

        del obj.created_at
        del obj.owner_id

        query = jobs.update().where(jobs.c.id == job_id).values(**obj.dict())
        await self.database.execute(query)

        return await self.get_object(job_id)

    async def get_object(self, job_id: int, ):
        query = jobs.select().where(jobs.c.id == job_id)
        obj = await self.database.fetch_one(query)

        return Jobs.parse_obj(obj) if obj else None

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Query]:
        join_users = jobs.join(users, jobs.c.owner_id == users.c.id)

        user_column = (
            users.c.id.label('user_id'),
            users.c.email.label('user_email'),
            users.c.name.label('user_name'),
            users.c.is_company,
            users.c.created_at.label('user_create')
        )

        query = select(jobs, *user_column).select_from(join_users).limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def remove(self, job_id: int):
        query = jobs.update().where(jobs.c.id == job_id).values({'is_active': False})
        return await self.database.execute(query)

    @staticmethod
    def get_value(job: JobIn, **kwargs):
        obj = Jobs(
            **job.dict(),
            owner_id=kwargs.get('user_id', 0),
            updated_at=datetime.datetime.utcnow()
        )
        del obj.id
        return obj
