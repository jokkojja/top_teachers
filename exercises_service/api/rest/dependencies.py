from fastapi import Depends, FastAPI

from api.rest.app import app
from app_globals import AppGlobals, DatabaseSession


def get_app() -> FastAPI:
    return app


def get_app_globals(app: FastAPI = Depends(get_app)) -> AppGlobals:
    return app.state.globals


def get_database_session(
    globals: AppGlobals = Depends(get_app_globals),
) -> DatabaseSession:
    return globals.database_session
