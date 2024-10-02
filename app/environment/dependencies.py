from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.environment.models import CodeDefinition, Environment
from app.environment.service import try_find_definition, try_find_environment


async def get_environment(
    environment_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Environment:
    environment = await try_find_environment(session=session, environment_id=environment_id)

    if environment is None:
        raise HTTPException(status_code=404, detail=f'Environment "{environment_id}" not found')

    return environment


async def get_definition(
    definition_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CodeDefinition:
    definition = await try_find_definition(session=session, definition_id=definition_id)

    if definition is None:
        raise HTTPException(status_code=404, detail=f'Definition "{definition_id}" not found')

    return definition
