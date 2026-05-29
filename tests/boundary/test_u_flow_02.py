"""
Track A — U-FLOW-02 (extended) Domain isolation RED skeletons.

Invalid inputs must keep SolvePartialMagicSquare.execute call_count == 0.
Mock/spy on Control port — comments only in RED Skeleton phase.
"""

from __future__ import annotations

import pytest

from boundary.ui_boundary import UIBoundary

# from control.ports import SolvePartialMagicSquare


@pytest.fixture
def ui_boundary_with_spy() -> UIBoundary:
    """UIBoundary with execute spy — wire in GREEN."""
    # execute_spy = create_autospec(SolvePartialMagicSquare, instance=True)
    # return UIBoundary(solver_port=execute_spy)
    return UIBoundary()


class TestUFlow02Extended:
    """U-FLOW-02 — invalid input never calls Domain execute."""

    def test_u_flow_02_null_matrix_execute_never_called(
        self, ui_boundary_with_spy: UIBoundary
    ) -> None:
        """U-FLOW-02 — matrix=null → execute.call_count == 0."""
        # Given
        # matrix = None
        # When
        # result = ui_boundary_with_spy.solve(matrix)
        # Then — GREEN: execute_spy.execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 — null input → execute 0 calls")

    def test_u_flow_02_three_blanks_execute_never_called(
        self, ui_boundary_with_spy: UIBoundary
    ) -> None:
        """U-FLOW-02 ext — E002 path (3 blanks) → execute 0 calls."""
        # Given
        # matrix = [[16,2,3,13],[5,11,0,8],[9,7,0,12],[0,14,15,1]]
        # When
        # result = ui_boundary_with_spy.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — three blanks → execute 0 calls")

    def test_u_flow_02_out_of_range_execute_never_called(
        self, ui_boundary_with_spy: UIBoundary
    ) -> None:
        """U-FLOW-02 ext — E004 path → execute 0 calls."""
        # Given
        # matrix with cell 17 and exactly 2 blanks
        # When
        # result = ui_boundary_with_spy.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — range violation → execute 0 calls")

    def test_u_flow_02_duplicate_execute_never_called(
        self, ui_boundary_with_spy: UIBoundary
    ) -> None:
        """U-FLOW-02 ext — E005 path → execute 0 calls."""
        # Given
        # matrix with non-zero duplicate and exactly 2 blanks
        # When
        # result = ui_boundary_with_spy.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — duplicate non-zero → execute 0 calls")

    def test_u_flow_02_one_blank_execute_never_called(
        self, ui_boundary_with_spy: UIBoundary
    ) -> None:
        """U-FLOW-02 ext — U-IN-07 RD-04 → execute 0 calls."""
        # Given
        # matrix = PRD RD-04 (one blank)
        # When
        # result = ui_boundary_with_spy.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — one blank → execute 0 calls")
