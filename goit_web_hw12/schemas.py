import re

from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field, validator


class ContactModel(BaseModel):
    name: str = Field(max_length=25)
    surname: str = Field(max_length=25)
    email: EmailStr
    phone: str = Field(example="+380(xx)xxx-xx-xx or +380(xx)xxx-x-xxx")
    bithday: date
    # user_id: int
    information: str = Field('', max_length=250)

    @validator("phone")
    def phone_number(cls, v):
        match = re.match(r"\+380\(\d{2}\)\d{3}-\d-\d{3}|\+380\(\d{2}\)\d{3}-\d{2}-\d{2}", v)
        if (match is None) or (len(v) != 17):
            raise ValueError("Phone number must be in the format '+380(хх)ххх-х-ххх' or '+380(хх)ххх-хх-хх'")
        return v

class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
