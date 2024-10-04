import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel
from uuid_extensions import uuid7


class Environment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    title: str | None = Field(default=None, max_length=32)
    description: str | None = Field(default=None, max_length=128)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))

    definitions: list["CodeDefinition"] = Relationship(back_populates="environment")


class CodeDefinition(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    environment_id: UUID = Field(foreign_key="environment.id")
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    code: str

    environment: Environment = Relationship(back_populates="definitions")
