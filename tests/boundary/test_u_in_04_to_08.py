"""
Track A — U-IN-03~08 input validation RED skeletons.

Report/08·09 design: empty count, range, duplicate; U-IN-07/08 extensions.
Domain execute must not run (U-FLOW-02); U-IN-03~08 Full RED.
"""

from __future__ import annotations

import pytest

from src.boundary.contracts import (
    CELL_RANGE_CODE,
    CELL_RANGE_MESSAGE,
    DUPLICATE_CODE,
    DUPLICATE_MESSAGE,
    EMPTY_COUNT_CODE,
    EMPTY_COUNT_MESSAGE,
)
from src.boundary.input_validator import InputValidator
from src.boundary.schemas import FailureResult

# U-IN-03 matrix: G0 complete 4×4 magic square (0 blanks)
_MATRIX_G0: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

# U-IN-04 matrix: 4×4, three blanks (0 count == 3)
_MATRIX_THREE_BLANKS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [0, 14, 15, 1],
]

# U-IN-05 matrix: 4×4, two blanks, cell value 17
_MATRIX_CELL_17: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 17],
]

# U-IN-05b matrix: 4×4, two blanks, cell value -1
_MATRIX_CELL_NEG1: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [4, 14, 15, -1],
]

# U-IN-06 matrix: 4×4, two blanks, non-zero duplicate 7
_MATRIX_DUPLICATE: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [4, 14, 7, 7],
]

# U-IN-07 matrix: PRD RD-04, one blank
_MATRIX_ONE_BLANK: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [0, 14, 15, 1],
]

# U-IN-08 matrix: three blanks + out-of-range (short-circuit → E002 before E004)
_MATRIX_ORDER_PROBE: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 17],
    [0, 14, 15, 1],
]


@pytest.fixture
def input_validator() -> InputValidator:
    """Boundary input validator under test."""
    return InputValidator()


class TestUIn04To08:
    """U-IN-03~08 — Boundary input contract."""

    def test_u_in_03_zero_blanks_g0_returns_e002(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-03 — G0 complete grid, blank count 0 → Failure E002."""
        # U-IN-03
        # Given
        matrix = _MATRIX_G0

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == EMPTY_COUNT_CODE
        assert result.message == EMPTY_COUNT_MESSAGE

    def test_u_in_04_three_blanks_returns_e002(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-04 — blank count 3 → Failure E002."""
        # U-IN-04
        # Given
        matrix = _MATRIX_THREE_BLANKS

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == EMPTY_COUNT_CODE
        assert result.message == EMPTY_COUNT_MESSAGE

    def test_u_in_05_cell_value_17_returns_e004(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-05 — cell 17 → Failure E004."""
        # U-IN-05
        # Given
        matrix = _MATRIX_CELL_17

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == CELL_RANGE_CODE
        assert result.message == CELL_RANGE_MESSAGE

    def test_u_in_05b_negative_cell_returns_e004(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-05b — cell -1 → Failure E004."""
        # U-IN-05b
        # Given
        matrix = _MATRIX_CELL_NEG1

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == CELL_RANGE_CODE
        assert result.message == CELL_RANGE_MESSAGE

    def test_u_in_06_duplicate_non_zero_returns_e005(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-06 — non-zero duplicate → Failure E005."""
        # U-IN-06
        # Given
        matrix = _MATRIX_DUPLICATE

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == DUPLICATE_CODE
        assert result.message == DUPLICATE_MESSAGE

    def test_u_in_07_one_blank_returns_e002(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-07 — PRD RD-04 single blank → Failure E002."""
        # U-IN-07
        # Given
        matrix = _MATRIX_ONE_BLANK

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == EMPTY_COUNT_CODE
        assert result.message == EMPTY_COUNT_MESSAGE

    def test_u_in_08_empty_count_short_circuits_before_range(
        self, input_validator: InputValidator
    ) -> None:
        """U-IN-08 — 3 blanks + range violation → E002 (not E004/E005)."""
        # U-IN-08
        # Given
        matrix = _MATRIX_ORDER_PROBE

        # When
        result = input_validator.validate(matrix)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == EMPTY_COUNT_CODE
        assert result.message == EMPTY_COUNT_MESSAGE
        assert result.code != CELL_RANGE_CODE
