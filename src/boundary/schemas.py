"""Boundary response schemas."""

from pydantic import BaseModel, ConfigDict


class FailureResult(BaseModel):
    """Standard failure response: code + message."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str
