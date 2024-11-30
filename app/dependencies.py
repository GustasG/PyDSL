"""
Global dependency module for FastAPI application.
"""

from typing import cast

from fastapi.requests import HTTPConnection
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(connection: HTTPConnection):
    """
    Dependency that provides an asynchronous sqlmodel session.

    This function extracts the sqlmodel engine from the app state,
    creates an asynchronous session, and yields it. The session is used
    to interact with the database in an asynchronous context.

    Args:
        connection (HTTPConnection): The FastAPI connection object which contains the
                           state with the sqlmodel engine.

    Yields:
        AsyncSession: An asynchronous sqlmodel session to interact with
                      the database.
    """
    engine = cast(AsyncEngine, connection.state.engine)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
