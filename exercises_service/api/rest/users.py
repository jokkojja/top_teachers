from api.models.user import User
from api.models.user import Users
from app_globals import DatabaseSession
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response


from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from api.rest.dependencies import get_database_session


user_router = APIRouter(prefix="/api/v1/user")


@user_router.get("/")
def get_users(
    database_session: DatabaseSession = Depends(get_database_session),
) -> Users:
    users = database_session.postgres.get_users()
    if len(users.users) == 0:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return Users(
        users=[User(name=user.name, role=user.role, hash=user.hash)
               for user in users]
    )


@user_router.get("/{user_id}")
def get_user(
    user_id: int,
    database_session: DatabaseSession = Depends(get_database_session),
) -> User:
    user = database_session.postgres.get_user(user_id)
    if user is None:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return User(name=user.name, role=user.role, hash=user.hash)


@user_router.put("/")
def create_user(
    user: User, database_session: DatabaseSession = Depends(get_database_session)
) -> JSONResponse:
    user_id = database_session.postgres.create_user(user.name, user.role.value)

    return JSONResponse(
        status_code=HTTP_200_OK, content=f"User was created with id {user_id}"
    )
