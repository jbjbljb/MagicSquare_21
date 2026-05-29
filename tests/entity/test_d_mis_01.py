"""
Track B — D-MIS-01 MissingNumberFinder / find_not_exist_nums RED skeleton.

Domain Mock prohibited.
"""

from __future__ import annotations

import pytest

from entity.services.missing_number_finder import find_not_exist_nums

# G1 — missing {7, 10}
# _G1: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 6, 0, 12],
#     [4, 14, 15, 1],
# ]


class TestDMis01:
    """D-MIS-01 — missing numbers ascending on G1."""

    def test_d_mis_01_find_not_exist_nums_ascending_on_g1(self) -> None:
        """D-MIS-01 — missing {7, 10} ascending."""
        # Given
        # grid = _G1
        # When
        # missing = find_not_exist_nums(grid)
        # Then — GREEN: (7, 10) or {7, 10} sorted
        pytest.fail("RED: D-MIS-01 — G1 missing numbers {7, 10} ascending")
