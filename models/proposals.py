from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator


class Status(str, Enum):
    rejected = 'rejected'
    accepted = 'accepted'


class ProposalIn(BaseModel):
    user_id: int
    job_id: int


class ProposalUpdateIn(ProposalIn):
    status: Status


class Proposal(ProposalIn):
    in_process: bool = True
    status: Status = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @validator('in_process')
    def close_process(cls, v, values, **kwargs):
        if values['status'] is not None:
            v = False
        return v
