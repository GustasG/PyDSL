from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.environment import service
from app.environment.dependencies import get_definition, get_environment
from app.environment.models import CodeDefinition, Environment
from app.environment.schemas import EnvironmentCreate, EnvironmentUpdate

router = APIRouter(prefix="/environment", tags=["environment"])


@router.post(
    path="/",
    response_model=Environment,
    status_code=201,
)
async def create_environment(
    creation_data: EnvironmentCreate, response: Response, session: Annotated[AsyncSession, Depends(get_session)]
):
    environment = await service.create_new_environment(session=session, creation_data=creation_data)

    response.headers["Location"] = f"/environment/{environment.id}"

    return environment


@router.get(
    path="/{environment_id}",
    response_model=Environment,
    status_code=status.HTTP_200_OK,
)
async def read_environment(
    environment: Annotated[Environment, Depends(get_environment)],
):
    return environment


@router.patch(
    path="/{environment_id}",
    response_model=Environment,
    status_code=status.HTTP_200_OK,
)
async def update_environment(
    update_data: EnvironmentUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    environment: Annotated[Environment, Depends(get_environment)],
):
    updated_environment = await service.update_existing_environment(
        session=session, environment=environment, update_data=update_data
    )

    return updated_environment


@router.delete(path="/{environment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_environment(
    session: Annotated[AsyncSession, Depends(get_session)],
    environment: Annotated[Environment, Depends(get_environment)],
):
    await service.delete_existing_environment(session=session, environment=environment)


@router.get(path="/", response_model=list[Environment], status_code=status.HTTP_200_OK)
async def read_all_environments(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: int = Query(default=1, ge=1, description="Page number"),
):
    environments = await service.find_all_environments(session=session, page=page)

    return environments


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
    definitions = await service.find_all_code_definitions(session=session, environment_id=environment_id, page=page)

    return definitions


@router.get(
    path="/{environment_id}/definition/{definition_id}",
    response_model=CodeDefinition,
    status_code=status.HTTP_200_OK,
)
async def read_definition(
    definition: Annotated[CodeDefinition, Depends(get_definition)],
):
    return definition
