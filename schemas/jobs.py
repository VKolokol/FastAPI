import datetime

from typing import Optional
from pydantic import BaseModel, EmailStr


class Owner(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_email: EmailStr
    is_company: bool
    user_create: datetime.datetime


class ViewJob(BaseModel):
    id: Optional[int]
    title: str
    email: EmailStr
    description: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ViewJobsWithUsers(ViewJob, Owner):
    pass
