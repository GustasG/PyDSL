from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Environment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(min_length=4, max_length=32)
    description: str | None = Field(default=None, max_length=128)


class CodeDefinition(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    environment_id: UUID = Field(foreign_key="environment.id")
    code: str
