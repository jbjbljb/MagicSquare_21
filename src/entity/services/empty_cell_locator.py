"""Locate blank cells in row-major order (1-index coordinates)."""

from __future__ import annotations

from src.entity.constants import BLANK_CELL_VALUE, REQUIRED_BLANK_COUNT


def find_blank_coords(
    grid: list[list[int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Return the first two blank cells in row-major scan order.

    Coordinates are 1-indexed (row, col).
    """
    blanks: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == BLANK_CELL_VALUE:
                blanks.append((row_index + 1, col_index + 1))
    if len(blanks) != REQUIRED_BLANK_COUNT:
        raise ValueError(
            f"Expected exactly {REQUIRED_BLANK_COUNT} blank cells, found {len(blanks)}"
        )
    first, second = blanks[0], blanks[1]
    return first, second
