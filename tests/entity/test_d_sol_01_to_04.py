"""
Track B — D-SOL-01~04 TwoCellSolver / solution Full RED.

Control-layer solver; tests live under tests/entity per Dual-Track layout.
Domain Mock prohibited.
"""

from __future__ import annotations

import pytest

from src.entity.constants import CELL_VALUE_MAX, CELL_VALUE_MIN, GRID_SIZE
from src.control.exceptions import UnsolvableDomainError
from src.control.two_cell_solver import solution
from tests.conftest import G1, G2, G3


class TestDSol01To04:
    """D-SOL-01~04 — solution() contract."""

    def test_d_sol_01_step_a_success_on_g1(self) -> None:
        """D-SOL-01 — G1 small-first → [1,2,2,3,4,12]."""
        # D-SOL-01
        # Given
        grid = [row[:] for row in G1]

        # When
        result = solution(grid)

        # Then
        assert result == [1, 2, 2, 3, 4, 12]

    def test_d_sol_02_step_b_success_on_g2(self) -> None:
        """D-SOL-02 — G2 reverse success → [2,3,10,4,1,4]."""
        # D-SOL-02
        # Given
        grid = [row[:] for row in G2]

        # When
        result = solution(grid)

        # Then
        assert result == [2, 3, 10, 4, 1, 4]

    def test_d_sol_03_both_steps_fail_on_g3(self) -> None:
        """D-SOL-03 — G3 placeholder → UnsolvableDomainError."""
        # D-SOL-03
        # Given
        grid = [row[:] for row in G3]

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solution(grid)

    def test_d_sol_04_result_shape_and_one_index_policy_on_g1(self) -> None:
        """D-SOL-04 — len 6; r,c ∈ [1,4]; n ∈ [1,16]."""
        # D-SOL-04
        # Given
        grid = [row[:] for row in G1]

        # When
        result = solution(grid)

        # Then
        assert len(result) == 6
        row1, col1, num1, row2, col2, num2 = result
        assert CELL_VALUE_MIN <= row1 <= GRID_SIZE
        assert CELL_VALUE_MIN <= col1 <= GRID_SIZE
        assert CELL_VALUE_MIN <= row2 <= GRID_SIZE
        assert CELL_VALUE_MIN <= col2 <= GRID_SIZE
        assert CELL_VALUE_MIN <= num1 <= CELL_VALUE_MAX
        assert CELL_VALUE_MIN <= num2 <= CELL_VALUE_MAX
