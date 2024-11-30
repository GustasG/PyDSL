"""
FastAPI Application Module for Python Function Execution API
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.types import Lifespan

from app.environment.exceptions import DefinitionNotFoundError, EnvironmentNotFoundError, ExecutionError
from app.environment.router import router as environment_router

DESCRIPTION = """
The Python Function Execution API allows users to submit, store, and execute Python functions via API calls.
Users can define and send Python functions to the API, where the functions are stored in a database.
Once saved, the functions can be invoked at any time by making an API request to the execution endpoint.

## Key features

* **Function Submission**: Send Python functions to the API, which are stored for later use.
* **Function Invocation**: Execute stored functions by calling a dedicated API endpoint, passing necessary parameters.
* **Function Management**: Retrieve details, update, or delete stored functions via additional API endpoints.
* **Environment Management**: Control execution environments. Environment is a set that stores all the related functions
for execution.
"""


def create_app(lifespan: Lifespan[FastAPI] | None = None) -> FastAPI:
    """
    Create a FastAPI application instance with the provided lifespan.

    Args:
        lifespan (Lifespan[FastAPI] | None): Lifespan instance to manage the application lifecycle.

    Returns:
        FastAPI: FastAPI application instance.
    """
    app = FastAPI(
        title="PyDSL",
        version="0.0.1",
        summary="A python interpreter running thought HTTP using API calls",
        description=DESCRIPTION,
        openapi_tags=[
            {
                "name": "environment",
                "description": "Operations related to the execution environment",
            },
            {"name": "definition", "description": "Operations related to code definitions"},
        ],
        servers=[{"url": "http://localhost:8000", "description": "Local development server"}],
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    @app.exception_handler(EnvironmentNotFoundError)
    def environment_not_found_exception_handler(_request: Request, exc: EnvironmentNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": f'Environment "{exc.id}" not found'},
        )

    @app.exception_handler(DefinitionNotFoundError)
    def definition_not_found_exception_handler(_request: Request, exc: DefinitionNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": f'Definition "{exc.id}" not found'},
        )

    @app.exception_handler(ExecutionError)
    def execution_error_exception_handler(_request: Request, exc: ExecutionError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": f'Error occurred while executing "{exc.callable}"',
                "message": str(exc.__cause__),
                "type": type(exc.__cause__).__name__,
            },
        )

    app.include_router(environment_router)

    return app
