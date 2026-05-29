"""Validate whether a 4×4 grid is a complete magic square."""

from __future__ import annotations

from src.entity.constants import (
    BLANK_CELL_VALUE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    GRID_SIZE,
    MAGIC_SUM,
)


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when grid is a complete 4×4 magic square (no blanks)."""
    values = [cell for row in grid for cell in row]
    if BLANK_CELL_VALUE in values:
        return False
    if len(values) != GRID_SIZE * GRID_SIZE:
        return False
    if any(value < CELL_VALUE_MIN or value > CELL_VALUE_MAX for value in values):
        return False
    if len(set(values)) != len(values):
        return False
    for row in grid:
        if sum(row) != MAGIC_SUM:
            return False
    for col_index in range(GRID_SIZE):
        if sum(grid[row_index][col_index] for row_index in range(GRID_SIZE)) != MAGIC_SUM:
            return False
    if sum(grid[index][index] for index in range(GRID_SIZE)) != MAGIC_SUM:
        return False
    if sum(
        grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)
    ) != MAGIC_SUM:
        return False
    return True
