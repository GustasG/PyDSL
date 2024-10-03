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
    """
    Retrieve an environment by its ID.

    Args:
        environment_id (UUID): The UUID of the environment to retrieve.
        session (AsyncSession): The database session dependency.

    Returns:
        Environment: The retrieved environment object.

    Raises:
        HTTPException: If the environment is not found, raises a 404 HTTP exception.
    """
    environment = await try_find_environment(session=session, environment_id=environment_id)

    if environment is None:
        raise HTTPException(status_code=404, detail=f'Environment "{environment_id}" not found')

    return environment


async def get_definition(
    definition_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CodeDefinition:
    """
    Retrieve a code definition by its ID.

    Args:
        definition_id (UUID): The UUID of the code definition to retrieve.
        session (AsyncSession): The database session dependency.

    Returns:
        CodeDefinition: The retrieved code definition object.

    Raises:
        HTTPException: If the code definition is not found, raises a 404 HTTP exception.
    """
    definition = await try_find_definition(session=session, definition_id=definition_id)

    if definition is None:
        raise HTTPException(status_code=404, detail=f'Definition "{definition_id}" not found')

    return definition
