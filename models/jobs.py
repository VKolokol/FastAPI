from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseJobs(BaseModel):
    email: EmailStr
    title: str
    description: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool = True


class JobIn(BaseJobs):
    pass


class Jobs(BaseJobs):
    id: Optional[int]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime
    owner_id: int
