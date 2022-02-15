from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator


class Status(str, Enum):
    rejected = 'rejected'
    accepted = 'accepted'
    send = 'send'


class ProposalIn(BaseModel):
    user_id: int
    job_id: int


class ProposalUpdateIn(ProposalIn):
    status: Status


class Proposal(ProposalUpdateIn):
    in_process: bool = True
    status: Status = Status.send
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @validator('in_process')
    def close_process(cls, in_process, values, **kwargs):
        if values.get('status', None) and values['status'] != Status.send:
            in_process = False
        return in_process
