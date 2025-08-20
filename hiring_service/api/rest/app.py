from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app_globals import AppGlobals


@asynccontextmanager
async def handle_api_startup(app: FastAPI):
    globals = await AppGlobals.create()
    app.state.globals = globals
    yield

    # fix to process CanceledError correct
    await app.state.globals.shutdown()


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(
    lifespan=handle_api_startup,
    middleware=middleware,
)
