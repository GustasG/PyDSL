"""
Global model schemas for the application.
"""

from pydantic import BaseModel


class GenericErrorData(BaseModel):
    detail: str
