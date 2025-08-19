from api.models.user import UserCreate, Users, UserResponse
from app_globals import PostgreControllers
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response


from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from api.rest.dependencies import get_database_controllers


user_router = APIRouter(prefix="/api/v1/user")


@user_router.get("/")
def get_users(
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> Users:
    users = database_controllers.users_controller.get_users()
    if len(users.users) == 0:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return Users(users=[UserResponse(name=user.name, role=user.role) for user in users])


@user_router.get("/{user_id}")
def get_user(
    user_id: int,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> UserResponse:
    user = database_controllers.users_controller.get_user(user_id)
    if user is None:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return UserResponse(name=user.name, role=user.role)


@user_router.put("/")
def create_user(
    user: UserCreate,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> JSONResponse:
    user_id = database_controllers.users_controller.create_user(
        user.name, user.role.value
    )

    return JSONResponse(
        status_code=HTTP_200_OK, content=f"User was created with id {user_id}"
    )
