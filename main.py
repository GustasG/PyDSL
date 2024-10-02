from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel

from app.environment.router import router as environment_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    engine = create_async_engine("sqlite+aiosqlite:///database.db", echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield {"engine": engine}

    await engine.dispose()


app = FastAPI(
    title="PyDSL",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(environment_router)
