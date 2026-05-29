"""Find missing numbers from 1..CELL_VALUE_MAX not present in the grid."""

from __future__ import annotations

from src.entity.constants import BLANK_CELL_VALUE, CELL_VALUE_MAX, CELL_VALUE_MIN


def find_not_exist_nums(grid: list[list[int]]) -> tuple[int, int]:
    """Return the two missing values in ascending order."""
    present = {
        cell
        for row in grid
        for cell in row
        if cell != BLANK_CELL_VALUE
    }
    missing = [
        value
        for value in range(CELL_VALUE_MIN, CELL_VALUE_MAX + 1)
        if value not in present
    ]
    return missing[0], missing[1]
