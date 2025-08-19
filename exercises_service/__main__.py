import uvicorn
from fastapi import FastAPI

from api.config import ApiConfig
from api.rest.app import app
from api.rest.users import user_router
from api.rest.exercises import exercise_router


def run_api(app: FastAPI) -> None:
    routers = [user_router, exercise_router]
    for router in routers:
        app.include_router(router)

    api_config = ApiConfig.from_env()
    server_config = uvicorn.Config(
        app, host="0.0.0.0", port=api_config.port, log_level=api_config.log_level
    )
    server = uvicorn.Server(server_config)
    server.run()


def main() -> None:
    run_api(app)


if __name__ == "__main__":
    main()
