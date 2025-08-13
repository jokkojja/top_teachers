from api.models.roles import Role
from pydantic import BaseModel


class UserResponse(BaseModel):
    name: str
    role: Role
    hash: str


class Users(BaseModel):
    users: list[UserResponse]


class UserCreate(BaseModel):
    name: str
    role: Role
