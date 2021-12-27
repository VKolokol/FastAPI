import datetime

from typing import List
from fastapi import Query
from sqlalchemy import select

from models.jobs import Jobs, JobIn
from db.jobs import jobs
from db.users import users
from repositories.base import BaseRepository


class JobRepository(BaseRepository):
    async def create_job(self, user_id: int, job: JobIn):
        values, obj = self.get_values(user_id, job)
        values.pop('id', None)
        query = jobs.insert().values(**values)
        obj.id = await self.database.execute(query)
        return obj

    async def update(self, job_id: int, job: JobIn):
        values = self.get_values(job_id, job)
        values.pop('id', None)
        values.pop('created_at', None)
        query = jobs.update().where(jobs.c.id == job_id).values(**values)
        await self.database.execute(query)
        return await self.get_object(job_id)

    async def get_object(self, job_id: int, ):
        query = jobs.select().where(jobs.c.id == job_id)
        obj = await self.database.fetch_one(query)

        return Jobs.parse_obj(obj) if obj else None

    async def get_list(self, limit: int = 100, skip: int = 0) -> List[Query]:
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

    @staticmethod
    def get_values(user_id: int, job: JobIn):
        obj = Jobs(
            title=job.title,
            email=job.email,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active,
            owner_id=user_id,
            updated_at=datetime.datetime.utcnow()
        )
        return {**obj.dict()}
