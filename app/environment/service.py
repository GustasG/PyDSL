from collections.abc import Sequence
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.environment.models import CodeDefinition, Environment


async def find_all_environments(session: AsyncSession) -> Sequence[Environment]:
    result = await session.exec(select(Environment))
    return result.all()


async def try_find_environment(session: AsyncSession, environment_id: UUID) -> Environment | None:
    result = await session.get(Environment, environment_id)
    return result


async def find_all_code_definitions(session: AsyncSession, environment_id: UUID) -> Sequence[CodeDefinition]:
    statement = select(CodeDefinition).where(CodeDefinition.environment_id == environment_id)

    result = await session.exec(statement)
    return result.all()


async def try_find_definition(session: AsyncSession, definition_id: UUID) -> CodeDefinition | None:
    result = await session.get(CodeDefinition, definition_id)
    return result
