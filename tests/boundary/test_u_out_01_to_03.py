"""
Track A — U-OUT-01~03 output contract RED skeletons.

Mock/spy on Control Domain port only; G1 fixture commented until GREEN.
"""

from __future__ import annotations

import pytest

from boundary.ui_boundary import UIBoundary

# G1 valid partial grid (see tests/conftest.py)
# _G1: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 6, 0, 12],
#     [4, 14, 15, 1],
# ]

# Mock SolvePartialMagicSquare.execute → [2, 2, 7, 3, 3, 10]


@pytest.fixture
def ui_boundary() -> UIBoundary:
    """Boundary entry with injectable Control port (mock in GREEN)."""
    # return UIBoundary(solver_port=mock_execute)
    return UIBoundary()


class TestUOut01To03:
    """U-OUT-01~03 — success output envelope RED skeletons."""

    def test_u_out_01_success_result_length_six(self, ui_boundary: UIBoundary) -> None:
        """U-OUT-01 — Success.result is int[6]."""
        # Given
        # grid = _G1
        # mock_execute.return_value = [2, 2, 7, 3, 3, 10]
        # When
        # result = ui_boundary.solve(grid)
        # Then — GREEN: len(result)==6
        pytest.fail("RED: U-OUT-01 — success tuple length 6")

    def test_u_out_02_success_coordinates_one_indexed(
        self, ui_boundary: UIBoundary
    ) -> None:
        """U-OUT-02 — r,c ∈ [1,4]; n ∈ [1,16]."""
        # Given
        # grid = _G1
        # mock_execute.return_value = [2, 2, 7, 3, 3, 10]
        # When
        # result = ui_boundary.solve(grid)
        pytest.fail("RED: U-OUT-02 — coordinates 1-index in [1,4]")

    def test_u_out_03_success_missing_numbers_ascending_in_tuple(
        self, ui_boundary: UIBoundary
    ) -> None:
        """U-OUT-03 — n1 < n2 in [r1,c1,n1,r2,c2,n2] (OUT-03)."""
        # Given
        # grid = _G1
        # mock_execute.return_value = [2, 2, 7, 3, 3, 10]
        # When
        # result = ui_boundary.solve(grid)
        pytest.fail("RED: U-OUT-03 — missing numbers n1 < n2 in output tuple")
