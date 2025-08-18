from fastapi import Depends, FastAPI

from api.rest.app import app
from app_globals import AppGlobals, PostgreControllers


def get_app() -> FastAPI:
    return app


def get_app_globals(app: FastAPI = Depends(get_app)) -> AppGlobals:
    return app.state.globals


def get_database_controllers(
    globals: AppGlobals = Depends(get_app_globals),
) -> PostgreControllers:
    return globals.postgre_controllers
