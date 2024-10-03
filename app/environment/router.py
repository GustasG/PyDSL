from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.environment.dependencies import get_definition, get_environment
from app.environment.models import CodeDefinition, Environment
from app.environment.service import (
    find_all_code_definitions,
    find_all_environments,
)

router = APIRouter(prefix="/environment", tags=["environment"])


@router.get(path="/", response_model=list[Environment], status_code=status.HTTP_200_OK)
async def read_all_environments(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: int = Query(default=1, ge=1, description="Page number"),
):
    environments = await find_all_environments(session=session, page=page)

    return environments


@router.get(
    path="/{environment_id}",
    response_model=Environment,
    status_code=status.HTTP_200_OK,
)
async def read_environment(
    environment: Annotated[Environment, Depends(get_environment)],
):
    return environment


@router.get(
    path="/{environment_id}/definition",
    response_model=list[CodeDefinition],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_environment)],
)
async def read_all_definitions(
    environment_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    page: int = Query(default=1, ge=1, description="Page number"),
):
    definitions = await find_all_code_definitions(session=session, environment_id=environment_id, page=page)

    return definitions


@router.get(path="/{environment_id}/definition/{definition_id}")
async def read_definition(
    definition: Annotated[CodeDefinition, Depends(get_definition)],
):
    return definition
