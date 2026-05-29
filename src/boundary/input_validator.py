"""Boundary input validation."""

from __future__ import annotations

from src.boundary.contracts import (
    BLANK_CELL_VALUE,
    EMPTY_COUNT_CODE,
    EMPTY_COUNT_MESSAGE,
    GRID_SIZE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    REQUIRED_BLANK_COUNT,
)
from src.boundary.schemas import FailureResult


class InputValidator:
    """Validates puzzle grid input at Boundary."""

    def validate(
        self, grid: list[list[int]] | None
    ) -> FailureResult | None:
        """
        Validate grid; return FailureResult on failure, None if valid so far.

        GREEN (AC-FR-01-01): grid is None; shape must be GRID_SIZE x GRID_SIZE.
        GREEN (U-IN-03~04): blank count must be REQUIRED_BLANK_COUNT.
        """
        if grid is None:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        if len(grid) != GRID_SIZE:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        for row in grid:
            if len(row) != GRID_SIZE:
                return FailureResult(
                    code=INVALID_SIZE_CODE,
                    message=INVALID_SIZE_MESSAGE,
                )
        blank_count = sum(
            cell == BLANK_CELL_VALUE for row in grid for cell in row
        )
        if blank_count != REQUIRED_BLANK_COUNT:
            return FailureResult(
                code=EMPTY_COUNT_CODE,
                message=EMPTY_COUNT_MESSAGE,
            )
        return None
