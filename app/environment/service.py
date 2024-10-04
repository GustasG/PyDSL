import datetime
from collections.abc import Sequence
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.environment.constants import DEFINITIONS_PER_PAGE, ENVIRONMENTS_PER_PAGE
from app.environment.models import CodeDefinition, Environment
from app.environment.schemas import EnvironmentCreate, EnvironmentUpdate


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
        .order_by(Environment.id)
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
        .order_by(CodeDefinition.id)
    )

    result = await session.exec(statement)
    return result.all()


async def try_find_definition(session: AsyncSession, definition_id: UUID) -> CodeDefinition | None:
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
    environment = Environment(title=creation_data.title, description=creation_data.description)

    session.add(environment)
    await session.commit()
    await session.refresh(environment)

    return environment


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
    if update_data.title is not None:
        environment.title = update_data.title
    if update_data.description is not None:
        environment.description = update_data.description
    environment.updated_at = datetime.datetime.now(datetime.UTC)

    session.add(environment)
    await session.commit()

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
