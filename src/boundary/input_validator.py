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
        Validate grid; return FailureResult on failure, None if valid.

        Checks shape, blank count, cell range, and non-zero uniqueness in order.
        """
        shape_failure = self._validate_shape(grid)
        if shape_failure is not None:
            return shape_failure
        assert grid is not None

        blank_failure = self._validate_blank_count(grid)
        if blank_failure is not None:
            return blank_failure

        range_failure = self._validate_cell_range(grid)
        if range_failure is not None:
            return range_failure

        return self._validate_no_duplicates(grid)

    def _invalid_size(self) -> FailureResult:
        """Return standard INVALID_SIZE failure (PRD §8.1)."""
        return FailureResult(
            code=INVALID_SIZE_CODE,
            message=INVALID_SIZE_MESSAGE,
        )

    def _validate_shape(
        self, grid: list[list[int]] | None
    ) -> FailureResult | None:
        """Verify grid is GRID_SIZE x GRID_SIZE."""
        if grid is None:
            return self._invalid_size()
        if len(grid) != GRID_SIZE:
            return self._invalid_size()
        for row in grid:
            if len(row) != GRID_SIZE:
                return self._invalid_size()
        return None

    def _validate_blank_count(
        self, grid: list[list[int]]
    ) -> FailureResult | None:
        """Verify exactly REQUIRED_BLANK_COUNT blank cells."""
        blank_count = sum(
            cell == BLANK_CELL_VALUE for row in grid for cell in row
        )
        if blank_count != REQUIRED_BLANK_COUNT:
            return FailureResult(
                code=EMPTY_COUNT_CODE,
                message=EMPTY_COUNT_MESSAGE,
            )
        return None

    def _validate_cell_range(
        self, grid: list[list[int]]
    ) -> FailureResult | None:
        """Verify non-blank cells are within CELL_VALUE_MIN..CELL_VALUE_MAX."""
        for row in grid:
            for cell in row:
                if cell == BLANK_CELL_VALUE:
                    continue
                if cell < CELL_VALUE_MIN or cell > CELL_VALUE_MAX:
                    return FailureResult(
                        code=CELL_RANGE_CODE,
                        message=CELL_RANGE_MESSAGE,
                    )
        return None

    def _validate_no_duplicates(
        self, grid: list[list[int]]
    ) -> FailureResult | None:
        """Verify non-blank cell values are unique."""
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
