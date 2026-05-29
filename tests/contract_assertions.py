"""Shared contract assertion helpers for Boundary and Golden Master tests."""

from __future__ import annotations

from src.boundary.contracts import GRID_SIZE, SOLUTION_VECTOR_LENGTH
from src.entity.constants import CELL_VALUE_MAX, CELL_VALUE_MIN
from src.entity.services.empty_cell_locator import find_blank_coords
from src.entity.services.missing_number_finder import find_not_exist_nums


def assert_contract_int6(result: list[int]) -> None:
    """Verify int[6] envelope, 1-index coordinates, and value range."""
    assert len(result) == SOLUTION_VECTOR_LENGTH
    row1, col1, num1, row2, col2, num2 = result
    for row, col in ((row1, col1), (row2, col2)):
        assert CELL_VALUE_MIN <= row <= GRID_SIZE
        assert CELL_VALUE_MIN <= col <= GRID_SIZE
    for num in (num1, num2):
        assert CELL_VALUE_MIN <= num <= CELL_VALUE_MAX


def assert_contract_row_major(grid: list[list[int]], result: list[int]) -> None:
    """Verify blank coordinates follow row-major 1-index order."""
    (expected_r1, expected_c1), (expected_r2, expected_c2) = find_blank_coords(grid)
    row1, col1, _, row2, col2, _ = result
    assert (row1, col1) == (expected_r1, expected_c1)
    assert (row2, col2) == (expected_r2, expected_c2)


def assert_contract_small_first(grid: list[list[int]], result: list[int]) -> None:
    """Verify small-first attempt: smaller missing number placed first."""
    small, large = find_not_exist_nums(grid)
    _, _, num1, _, _, num2 = result
    assert num1 == small
    assert num2 == large
    assert num1 < num2


def assert_contract_reverse_fallback(grid: list[list[int]], result: list[int]) -> None:
    """Verify reverse fallback: larger missing number placed first."""
    small, large = find_not_exist_nums(grid)
    _, _, num1, _, _, num2 = result
    assert num1 == large
    assert num2 == small
    assert num1 > num2


def assert_contract_error_code(actual_code: str, expected_code: str) -> None:
    """Verify Error Contract code matches Boundary/Domain policy."""
    assert actual_code == expected_code
