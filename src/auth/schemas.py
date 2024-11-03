import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    username: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe123@co.com",
                "username": "johndoe",
                "password": "testpass123",
            }
        }
    }


class UserModel(BaseModel):
    uid: uuid.UUID
    email: str
    username: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
