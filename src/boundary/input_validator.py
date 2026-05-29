"""Boundary input validation."""

from __future__ import annotations

from src.boundary.contracts import (
    BLANK_CELL_VALUE,
    CELL_RANGE_CODE,
    CELL_RANGE_MESSAGE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    DUPLICATE_CODE,
    DUPLICATE_MESSAGE,
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
        GREEN (U-IN-05~05b): cell values must be BLANK_CELL_VALUE or CELL_VALUE_MIN..MAX.
        GREEN (U-IN-06): non-zero values must be unique.
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
        for row in grid:
            for cell in row:
                if cell == BLANK_CELL_VALUE:
                    continue
                if cell < CELL_VALUE_MIN or cell > CELL_VALUE_MAX:
                    return FailureResult(
                        code=CELL_RANGE_CODE,
                        message=CELL_RANGE_MESSAGE,
                    )
        seen: set[int] = set()
        for row in grid:
            for cell in row:
                if cell == BLANK_CELL_VALUE:
                    continue
                if cell in seen:
                    return FailureResult(
                        code=DUPLICATE_CODE,
                        message=DUPLICATE_MESSAGE,
                    )
                seen.add(cell)
        return None
