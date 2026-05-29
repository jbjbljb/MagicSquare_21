"""
Track B — D-MIS-01 MissingNumberFinder / find_not_exist_nums Full RED.

Domain Mock prohibited.
"""

from __future__ import annotations

from src.entity.services.missing_number_finder import find_not_exist_nums
from tests.conftest import G1


class TestDMis01:
    """D-MIS-01 — missing numbers ascending on G1."""

    def test_d_mis_01_find_not_exist_nums_ascending_on_g1(self) -> None:
        """D-MIS-01 — missing {2, 12} ascending."""
        # D-MIS-01
        # Given
        grid = [row[:] for row in G1]

        # When
        missing = find_not_exist_nums(grid)

        # Then
        assert missing == (2, 12)
