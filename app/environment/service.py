"""
Service layer for managing environment operations.
"""

import datetime
from collections.abc import Mapping, Sequence
from typing import Any
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.environment.constants import DEFINITIONS_PER_PAGE, ENVIRONMENTS_PER_PAGE
from app.environment.exceptions import ExecutionError
from app.environment.models import CodeDefinition, Environment
from app.environment.schemas import (
    DefinitionCreate,
    DefinitionUpdate,
    EnvironmentCreate,
    EnvironmentUpdate,
    ExecuteEnvironment,
)


async def create_new_environment(session: AsyncSession, creation_data: EnvironmentCreate) -> Environment:
    """
    Create a new environment in the database.

    This function creates a new environment using the provided creation data
    and adds it to the database. The environment is then committed and refreshed
    to ensure it is up-to-date with the database state.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        creation_data (EnvironmentCreate): The data required to create a new
                                           environment, including title and
                                           description.

    Returns:
        Environment: The newly created Environment object.
    """
    environment = Environment.model_validate(creation_data)

    session.add(environment)
    await session.commit()
    await session.refresh(environment)

    return environment


async def find_all_environments(session: AsyncSession, page: int) -> Sequence[Environment]:
    """
    Retrieve a paginated list of all environments from the database.

    This function constructs a SQL query to select environments, applying
    pagination based on the provided page number.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        page (int): The page number for pagination. Determines the offset
                    for the query.

    Returns:
        Sequence[Environment]: A sequence of Environment objects representing
                               the environments retrieved from the database.
    """
    statement = (
        select(Environment)
        .offset((page - 1) * ENVIRONMENTS_PER_PAGE)
        .limit(ENVIRONMENTS_PER_PAGE)
        .order_by(str(Environment.id))
    )

    result = await session.exec(statement)
    return result.all()


async def try_find_environment(session: AsyncSession, environment_id: UUID) -> Environment | None:
    """
    Retrieve an environment by its ID from the database.

    This function attempts to find an environment in the database using
    the provided environment ID. If the environment is found, it is returned;
    otherwise, None is returned.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        environment_id (UUID): The unique identifier of the environment to
                               be retrieved.

    Returns:
        Environment | None: The Environment object if found, otherwise None.
    """
    result = await session.get(Environment, environment_id)
    return result


async def update_existing_environment(
    session: AsyncSession, environment: Environment, update_data: EnvironmentUpdate
) -> Environment:
    """
    Update an existing environment with new data.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        environment (Environment): The environment instance to update.
        update_data (EnvironmentUpdate): The data to update the environment with.

    Returns:
        Environment: The updated environment instance.
    """
    environment_data = update_data.model_dump(exclude_unset=True)
    environment_data["updated_at"] = datetime.datetime.now(datetime.UTC)

    environment.sqlmodel_update(environment_data)
    await session.commit()
    await session.refresh(environment)

    return environment


async def delete_existing_environment(session: AsyncSession, environment: Environment):
    """
    Delete an existing environment from the database.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        environment (Environment): The environment instance to delete.

    Returns:
        None
    """
    await session.delete(environment)
    await session.commit()


async def create_new_code_definition(
    session: AsyncSession, environment_id: UUID, create_data: DefinitionCreate
) -> CodeDefinition:
    """Create and persist a new code definition in the database.

    Args:
        session (AsyncSession): The database session for performing database operations
        environment_id (UUID): The unique identifier of the environment
        create_data (DefinitionCreate): The data object containing the code to be stored

    Returns:
        CodeDefinition: The newly created code definition object with populated database fields
    """
    definition = CodeDefinition(environment_id=environment_id, code=create_data.code.strip())

    session.add(definition)
    await session.commit()
    await session.refresh(definition)

    return definition


async def find_all_code_definitions(session: AsyncSession, environment_id: UUID, page: int) -> Sequence[CodeDefinition]:
    """
    Retrieve a paginated list of code definitions for a specific environment from the database.

    This function constructs a SQL query to select code definitions associated with a given
    environment ID, applying pagination based on the provided page number.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        environment_id (UUID): The unique identifier of the environment whose
                               code definitions are to be retrieved.
        page (int): The page number for pagination. Determines the offset
                    for the query.

    Returns:
        Sequence[CodeDefinition]: A sequence of CodeDefinition objects representing
                                  the code definitions retrieved from the database.
    """
    statement = (
        select(CodeDefinition)
        .where(CodeDefinition.environment_id == environment_id)
        .offset((page - 1) * DEFINITIONS_PER_PAGE)
        .limit(DEFINITIONS_PER_PAGE)
        .order_by(str(CodeDefinition.id))
    )

    result = await session.exec(statement)
    return result.all()


async def find_all_code_definitions_unpaged(session: AsyncSession, environment_id: UUID) -> Sequence[CodeDefinition]:
    """
    Retrieve all code definitions for a specific environment from the database.

    This function constructs a SQL query to select code definitions associated with a given
    environment ID.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        environment_id (UUID): The unique identifier of the environment whose
                               code definitions are to be retrieved.

    Returns:
        Sequence[CodeDefinition]: A sequence of CodeDefinition objects representing
                                  the code definitions retrieved from the database.
    """
    statement = select(CodeDefinition).where(CodeDefinition.environment_id == environment_id)

    result = await session.exec(statement)
    return result.all()


async def try_find_code_definition(session: AsyncSession, definition_id: UUID) -> CodeDefinition | None:
    """
    Retrieve a code definition by its ID from the database.

    This function attempts to find a code definition in the database using
    the provided definition ID. If the code definition is found, it is returned;
    otherwise, None is returned.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to
                                interact with the database.
        definition_id (UUID): The unique identifier of the code definition to
                              be retrieved.

    Returns:
        CodeDefinition | None: The CodeDefinition object if found, otherwise None.
    """
    result = await session.get(CodeDefinition, definition_id)
    return result


async def update_existing_code_definition(
    session: AsyncSession, definition: CodeDefinition, update_data: DefinitionUpdate
) -> CodeDefinition:
    """
    Update an existing code definition with new data.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to interact with the database.
        definition (CodeDefinition): The code definition instance to update.
        update_data (DefinitionUpdate): The data to update the code definition with.

    Returns:
        CodeDefinition: The updated code definition instance.
    """
    definition_data = update_data.model_dump(exclude_unset=True)
    definition_data["updated_at"] = datetime.datetime.now(datetime.UTC)

    definition.sqlmodel_update(definition_data)
    await session.commit()
    await session.refresh(definition)

    return definition


async def delete_existing_code_definition(session: AsyncSession, definition: CodeDefinition):
    """
    Delete an existing code definition from the database.

    Args:
        session (AsyncSession): The asynchronous sqlmodel session used to interact with the database.
        definition (CodeDefinition): The code definition instance to delete.

    Returns:
        None
    """
    await session.delete(definition)
    await session.commit()


def execute_environment(definitions: Sequence[CodeDefinition], execute_data: ExecuteEnvironment) -> Any:
    """
    Execute the provided code definitions with the provided execution data.

    Args:
        definitions (Sequence[CodeDefinition]): The code definitions to execute.
        execute_data (ExecuteEnvironment): The data required to execute the code.

    Returns:
        Any: The result of executing the code.
    """
    code = "\n\n".join(definition.code for definition in definitions)
    code += f"""
        __INTERNAL__RETURN__ = {execute_data.callable}(*{execute_data.args}, **{execute_data.kwargs})
    """.strip()

    try:
        result = _run_code(code)
    except Exception as e:
        raise ExecutionError(callable_=execute_data.callable) from e

    return result


def _run_code(code: str) -> Any:
    """
    Execute the provided code and return the result.

    Args:
        code (str): The code to execute.

    Returns:
        Any: The result of the executed code.
    """
    loc: Mapping[str, object] = {}
    exec(code, {}, loc)  # noqa: S102, pylint: disable=W0122

    return loc["__INTERNAL__RETURN__"]
