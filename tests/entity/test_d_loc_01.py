"""
Track B — D-LOC-01 EmptyCellLocator / find_blank_coords Full RED.

Domain Mock prohibited.
"""

from __future__ import annotations

from src.entity.services.empty_cell_locator import find_blank_coords
from tests.conftest import G1


class TestDLoc01:
    """D-LOC-01 — row-major blank coordinates on G1."""

    def test_d_loc_01_find_blank_coords_row_major_on_g1(self) -> None:
        """D-LOC-01 — first (1,2), second (3,4) 1-index."""
        # D-LOC-01
        # Given
        grid = [row[:] for row in G1]

        # When
        first, second = find_blank_coords(grid)

        # Then
        assert first == (1, 2)
        assert second == (3, 4)
