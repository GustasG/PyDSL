"""
Main module for the FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel

from app import create_app


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    """
    Context manager that creates and disposes the database
    """
    engine = create_async_engine(url="sqlite+aiosqlite:///database.db", connect_args={"check_same_thread": False})

    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield {
            "engine": engine,
        }
    finally:
        await engine.dispose()


app = create_app(lifespan=_lifespan)
