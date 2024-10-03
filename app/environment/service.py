from collections.abc import Sequence
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.environment.constants import DEFINITIONS_PER_PAGE, ENVIRONMENTS_PER_PAGE
from app.environment.models import CodeDefinition, Environment


async def find_all_environments(session: AsyncSession, page: int) -> Sequence[Environment]:
    """
    Retrieve a paginated list of all environments from the database.

    This function constructs a SQL query to select environments, applying
    pagination based on the provided page number. The results are ordered
    by the environment ID.

    Args:
        session (AsyncSession): The asynchronous SQLAlchemy session used to
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
        session (AsyncSession): The asynchronous SQLAlchemy session used to
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
    environment ID, applying pagination based on the provided page number. The results are
    ordered by the code definition ID.

    Args:
        session (AsyncSession): The asynchronous SQLAlchemy session used to
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
        session (AsyncSession): The asynchronous SQLAlchemy session used to
                                interact with the database.
        definition_id (UUID): The unique identifier of the code definition to
                              be retrieved.

    Returns:
        CodeDefinition | None: The CodeDefinition object if found, otherwise None.
    """
    result = await session.get(CodeDefinition, definition_id)
    return result
