"""
Pydantic schema models for environment data validation and serialization.
"""

from typing import Any

from pydantic import BaseModel, Field


class EnvironmentCreate(BaseModel):
    """
    Schema for creating a new environment.
    """

    title: str | None = Field(
        description="Optional environment title",
        default=None,
        max_length=32,
        examples=["Testing alpha feature", "Production", "Feature v3 rollout"],
    )
    description: str | None = Field(
        default=None, max_length=128, examples=["Environment for testing unreleased feature in alpha"]
    )


class EnvironmentUpdate(BaseModel):
    """
    Schema for updating an existing environment's properties.
    """

    title: str | None = Field(default=None, max_length=32)
    description: str | None = Field(default=None, max_length=128)


class ExecuteEnvironment(BaseModel):
    """
    Schema for executing an environment.
    """

    callable: str = Field(description="Name of the callable to execute")
    args: list[Any] = Field(default=[], description="List of arguments to pass to the callable")
    kwargs: dict[str, Any] = Field(default={}, description="Dictionary of keyword arguments to pass to the callable")


class ExecutionResult(BaseModel):
    """
    Schema for the result of executing an environment.
    """

    result: Any = Field(description="The result of the execution")


class DefinitionCreate(BaseModel):
    """
    Schema for creating a new code definition.
    """

    code: str


class DefinitionUpdate(BaseModel):
    """
    Schema for updating an existing code definition.
    """

    code: str
