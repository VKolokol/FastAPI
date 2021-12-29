from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    hash_password: str
    is_company: bool = False
    is_stuff: bool = False
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @validator("password2")
    def password_match(cls, password2, values, **kwargs):
        if 'password' in values and password2 != values["password"]:
            raise ValueError("passwords don't match")
        return password2
