from api.models.roles import Role
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    role: Role


class Users(BaseModel):
    users: list[UserResponse]


class UserCreate(BaseModel):
    id: int
    name: str
    role: Role
