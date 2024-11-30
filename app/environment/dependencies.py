"""
FastAPI dependency injection functions for environment dependency retrieval.
"""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_session
from app.environment.exceptions import DefinitionNotFoundError, EnvironmentNotFoundError
from app.environment.models import CodeDefinition, Environment
from app.environment.service import find_all_code_definitions_unpaged, try_find_code_definition, try_find_environment


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
        EnvironmentNotFoundException: If the environment is not found.
    """
    environment = await try_find_environment(session=session, environment_id=environment_id)

    if environment is None:
        raise EnvironmentNotFoundError(environment_id=environment_id)

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
        DefinitionNotFoundException: If the code definition is not found.
    """
    definition = await try_find_code_definition(session=session, definition_id=definition_id)

    if definition is None:
        raise DefinitionNotFoundError(definition_id=definition_id)

    return definition


async def get_all_environment_definitions(
    environment_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[CodeDefinition]:
    """
    Retrieve all code definitions for a given environment.

    Args:
        environment_id (UUID): The UUID of the environment to retrieve code definitions for.
        session (AsyncSession): The database session dependency.

    Returns:
        Sequence[CodeDefinition]: A sequence of code definition objects.
    """
    return await find_all_code_definitions_unpaged(session=session, environment_id=environment_id)
