"""
Track B — D-SOL-01~04 TwoCellSolver / solution RED skeletons.

Control-layer solver; tests live under tests/entity per Dual-Track layout.
Domain Mock prohibited.
"""

from __future__ import annotations

import pytest

from control.two_cell_solver import solution

# G1 — Step A success → [2,2,7,3,3,10]
# _G1: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 6, 0, 12],
#     [4, 14, 15, 1],
# ]

# G2 — Step B success → [2,3,10,4,1,4]
# _G2: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 7, 6, 12],
#     [0, 14, 15, 1],
# ]


class TestDSol01To04:
    """D-SOL-01~04 — solution() contract RED skeletons."""

    def test_d_sol_01_step_a_success_on_g1(self) -> None:
        """D-SOL-01 — G1 small-first → [2,2,7,3,3,10]."""
        # Given
        # grid = _G1
        # When
        # result = solution(grid)
        pytest.fail("RED: D-SOL-01 — G1 Step A → [2,2,7,3,3,10]")

    def test_d_sol_02_step_b_success_on_g2(self) -> None:
        """D-SOL-02 — G2 reverse success → [2,3,10,4,1,4]."""
        # Given
        # grid = _G2  # TBD: confirm G2 fixture before GREEN
        # When
        # result = solution(grid)
        pytest.fail("RED: D-SOL-02 — G2 TBD")

    def test_d_sol_03_both_steps_fail_on_g3(self) -> None:
        """D-SOL-03 — G3 placeholder → UnsolvableDomainError."""
        # Given
        # grid = G3 from conftest (placeholder)
        # When
        # with pytest.raises(UnsolvableDomainError):
        #     solution(grid)
        pytest.fail("RED: D-SOL-03 — G3 both attempts fail → UnsolvableDomainError")

    def test_d_sol_04_result_shape_and_one_index_policy_on_g1(self) -> None:
        """D-SOL-04 — len 6; r,c ∈ [1,4]; n ∈ [1,16]."""
        # Given
        # grid = _G1
        # When
        # result = solution(grid)
        pytest.fail("RED: D-SOL-04 — int[6] length and 1-index coordinate policy")
