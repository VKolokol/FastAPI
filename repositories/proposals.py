from typing import List

from fastapi import Query, HTTPException, status
from asyncpg.exceptions import UniqueViolationError

from repositories.base import BaseRepository
from db.proposals import proposals
from models.proposals import Proposal, ProposalUpdateIn


class ProposalRepository(BaseRepository):

    async def send_proposal(self, user_id: int, job_id: int):
        values, proposal = self.get_values(user_id, job_id)

        try:
            query = proposals.insert().values(**values)
            await self.database.execute(query)
        except UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Proposal already exists")

        return proposal

    async def get_proposal(self, user_id: int, job_id: int):
        query = proposals.select().where(proposals.c.user_id == user_id, proposals.c.job_id == job_id)
        obj = await self.database.fetch_one(query)
        return Proposal.parse_obj(obj) if obj is not None else None

    async def reply_to_proposal(self, update: ProposalUpdateIn):
        values, proposal = self.get_values(*update.dict().values())
        values.pop('created_at', None)

        query = proposals.update().where(
            proposals.c.user_id == update.user_id, proposals.c.job_id == update.job_id
        ).values(**values)

        await self.database.execute(query)
        return await self.get_proposal(proposal.user_id, proposal.job_id)

    async def get_all_user_proposal(self, user_id: int) -> List[Query]:
        query = proposals.select().where(proposals.c.user_id == user_id)
        result = await self.database.fetch_all(query)
        return result

    async def get_all_candidates(self, job_id: int) -> List[Query]:
        query = proposals.select().where(proposals.c.job_id == job_id)
        result = await self.database.fetch_all(query)
        return result

    @staticmethod
    def get_values(user_id, job_id, status_proposal=None):
        proposal = Proposal(
            user_id=user_id,
            job_id=job_id,
            status=status_proposal
        )
        proposal.dict().pop('id', None)
        return {**proposal.dict()}, proposal
