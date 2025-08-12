from api.models.user import Users
from app_globals import DatabaseSession
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from starlette.status import (
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.rest.dependencies import get_database_session


user_router = APIRouter(prefix="/api/v1/user")


@user_router.get("/")
def get_users(
    database_session: DatabaseSession = Depends(get_database_session),
) -> Users:
    return database_session.postgres.get_users()
