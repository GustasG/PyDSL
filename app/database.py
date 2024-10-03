from typing import cast

from fastapi import Request
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(request: Request):
    """
    Dependency that provides an asynchronous SQLAlchemy session.

    This function extracts the SQLAlchemy engine from the request state,
    creates an asynchronous session, and yields it. The session is used
    to interact with the database in an asynchronous context.

    Args:
        request (Request): The FastAPI request object which contains the
                           state with the SQLAlchemy engine.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session to interact with
                      the database.
    """
    engine = cast(AsyncEngine, request.state.engine)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
