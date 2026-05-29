"""Two-cell magic square solver (Attempt 1 small-first, Attempt 2 reverse)."""

from __future__ import annotations

from src.control.exceptions import UnsolvableDomainError
from src.entity.services.empty_cell_locator import find_blank_coords
from src.entity.services.magic_square_validator import is_magic_square
from src.entity.services.missing_number_finder import find_not_exist_nums


def solution(grid: list[list[int]]) -> list[int]:
    """
    Solve a partial 4×4 grid with exactly two blanks.

    Returns int[6] = [r1, c1, n1, r2, c2, n2] with 1-index coordinates.
    """
    (row1, col1), (row2, col2) = find_blank_coords(grid)
    small, large = find_not_exist_nums(grid)
    attempts = (
        [row1, col1, small, row2, col2, large],
        [row1, col1, large, row2, col2, small],
    )
    for candidate in attempts:
        if _is_valid_completion(grid, candidate):
            return candidate
    raise UnsolvableDomainError("No valid completion for the given grid")


def _is_valid_completion(grid: list[list[int]], result: list[int]) -> bool:
    row1, col1, num1, row2, col2, num2 = result
    filled = [row[:] for row in grid]
    filled[row1 - 1][col1 - 1] = num1
    filled[row2 - 1][col2 - 1] = num2
    return is_magic_square(filled)
