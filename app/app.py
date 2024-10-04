from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.types import Lifespan

from app.environment.router import router as environment_router


def create_app(lifespan: Lifespan[FastAPI] | None = None) -> FastAPI:
    app = FastAPI(
        title="PyDSL",
        version="0.0.1",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    app.include_router(environment_router)

    return app
