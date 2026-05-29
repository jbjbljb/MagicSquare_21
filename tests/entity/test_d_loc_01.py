"""
Track B — D-LOC-01 EmptyCellLocator / find_blank_coords RED skeleton.

Domain Mock prohibited. G1 fixture commented until GREEN.
"""

from __future__ import annotations

import pytest

from entity.services.empty_cell_locator import find_blank_coords

# G1 — blanks (2,2),(3,3) 1-index row-major
# _G1: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 6, 0, 12],
#     [4, 14, 15, 1],
# ]


class TestDLoc01:
    """D-LOC-01 — row-major blank coordinates on G1."""

    def test_d_loc_01_find_blank_coords_row_major_on_g1(self) -> None:
        """D-LOC-01 — first (2,2), second (3,3) 1-index."""
        # Given
        # grid = _G1
        # When
        # first, second = find_blank_coords(grid)
        # Then — GREEN: (2,2), (3,3) row-major
        pytest.fail("RED: D-LOC-01 — G1 blanks (2,2) then (3,3) 1-index")
