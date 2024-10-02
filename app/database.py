from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_engine(request: Request) -> AsyncEngine:
    return request.state.engine


async def get_session(engine: Annotated[AsyncEngine, Depends(get_engine)]):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
