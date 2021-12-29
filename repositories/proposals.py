from typing import List

from fastapi import Query, HTTPException, status
from asyncpg.exceptions import UniqueViolationError

from repositories.base import BaseRepository
from db.proposals import proposals
from models.proposals import Proposal, ProposalUpdateIn, Status
from interfaces.repository import CRUDRepository


class ProposalRepository(BaseRepository, CRUDRepository):

    async def create(self, user_id: int, job_id: int):
        obj = self.get_value(user_id, job_id)

        try:
            query = proposals.insert().values(**obj.dict())
            await self.database.execute(query)
        except UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Proposal already exists")

        return obj

    async def get_object(self, user_id: int, job_id: int):
        query = proposals.select().where(proposals.c.user_id == user_id, proposals.c.job_id == job_id)
        obj = await self.database.fetch_one(query)
        if obj is None:
            return None
        return Proposal.parse_obj(obj)

    async def update(self, update: ProposalUpdateIn):
        obj = self.get_value(*update.dict().values())

        del obj.created_at

        query = proposals.update().where(
            proposals.c.user_id == update.user_id, proposals.c.job_id == update.job_id
        ).values(**obj.dict())

        await self.database.execute(query)
        return await self.get_object(obj.user_id, obj.job_id)

    async def get_all(self, user_id: int) -> List[Query]:
        query = proposals.select().where(
            proposals.c.user_id == user_id)
        result = await self.database.fetch_all(query)
        return result

    async def get_all_candidates(self, job_id: int) -> List[Query]:
        query = proposals.select().where(proposals.c.job_id == job_id)
        result = await self.database.fetch_all(query)
        return result

    async def remove(self, user_id: int, job_id: int):
        query = proposals.update().where(
            proposals.c.user_id == user_id,
            proposals.c.job_id == job_id
        ).values({'in_archive': True})
        await self.database.execute(query)

    @staticmethod
    def get_value(user_id, job_id, status=Status.send):
        proposal = Proposal(
            user_id=user_id,
            job_id=job_id,
            status=status
        )
        return proposal
