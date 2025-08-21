import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app_globals import AppGlobals
from api.consumer import consume_events


@asynccontextmanager
async def handle_api_startup(app: FastAPI):
    globals = await AppGlobals.create()
    app.state.globals = globals
    consumer_task = asyncio.create_task(consume_events(globals))

    try:
        yield
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass

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
