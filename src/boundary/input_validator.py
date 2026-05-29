"""Boundary input validation."""

from __future__ import annotations

from src.boundary.contracts import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from src.boundary.schemas import FailureResult


class InputValidator:
    """Validates puzzle grid input at Boundary."""

    def validate(
        self, grid: list[list[int]] | None
    ) -> FailureResult | None:
        """
        Validate grid; return FailureResult on failure, None if valid so far.

        GREEN (AC-FR-01-01): grid is None only.
        """
        if grid is None:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return None
