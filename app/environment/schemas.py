from pydantic import BaseModel, Field


class EnvironmentCreate(BaseModel):
    title: str | None = Field(default=None, max_length=32)
    description: str | None = Field(default=None, max_length=128)


class EnvironmentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=32)
    description: str | None = Field(default=None, max_length=128)
