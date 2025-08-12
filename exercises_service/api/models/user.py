from api.models.roles import Role
from pydantic import BaseModel


class User(BaseModel):
    name: str
    role: Role


class Users(BaseModel):
    users: list[User]
