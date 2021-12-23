import datetime

from typing import Optional

from pydantic import BaseModel, EmailStr


class ViewUser(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    is_company: bool
    created_at: datetime.datetime
