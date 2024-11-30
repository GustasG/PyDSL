from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel

from app import create_app


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield {"engine": engine}

    await engine.dispose()


@pytest.fixture
def test_client():
    app = create_app(lifespan=_lifespan)

    with TestClient(app) as client:
        yield client
