"""Golden Master regression tests for Magic Square Solver (GM-2)."""

from __future__ import annotations

import pytest

from src.boundary.contracts import DUPLICATE_CODE, EMPTY_COUNT_CODE
from src.control.exceptions import UnsolvableDomainError
from src.control.two_cell_solver import solution
from tests.conftest import G1, G2, G3
from tests.golden_master import (
    NO_VALID_MAGIC_SQUARE_CODE,
    assert_contract_error_code,
    assert_contract_int6,
    assert_contract_reverse_fallback,
    assert_contract_row_major,
    assert_contract_small_first,
    assert_scenario_golden,
    capture_scenario_output,
    format_error,
)

pytestmark = pytest.mark.golden_master


class TestGoldenMasterMagicSquare:
    """GM-2 — Magic Square Solver Golden Master regression suite."""

    @pytest.mark.golden_master
    def test_gm_tc_01_normal_success(
        self, golden_approve: bool
    ) -> None:
        """GM-TC-01 — small-first 정상 조합 성공."""
        grid = [row[:] for row in G1]

        result = solution(grid)
        assert_contract_int6(result)
        assert_contract_row_major(grid, result)
        assert_contract_small_first(grid, result)

        assert_scenario_golden("GM-TC-01", approve=golden_approve)

    @pytest.mark.golden_master
    def test_gm_tc_02_reverse_success(
        self, golden_approve: bool
    ) -> None:
        """GM-TC-02 — small-first 실패 후 reverse 조합 성공."""
        grid = [row[:] for row in G2]

        result = solution(grid)
        assert_contract_int6(result)
        assert_contract_row_major(grid, result)
        assert_contract_reverse_fallback(grid, result)

        assert_scenario_golden("GM-TC-02", approve=golden_approve)

    @pytest.mark.golden_master
    def test_gm_tc_03_invalid_blank_count(
        self, golden_approve: bool
    ) -> None:
        """GM-TC-03 — INVALID_BLANK_COUNT (Boundary E002)."""
        grid = [
            [16, 2, 3, 13],
            [5, 11, 0, 8],
            [9, 7, 0, 12],
            [0, 14, 15, 1],
        ]

        output = capture_scenario_output(grid)
        assert output == format_error(EMPTY_COUNT_CODE)
        assert_contract_error_code(EMPTY_COUNT_CODE, EMPTY_COUNT_CODE)

        assert_scenario_golden("GM-TC-03", approve=golden_approve)

    @pytest.mark.golden_master
    def test_gm_tc_04_duplicate_number(
        self, golden_approve: bool
    ) -> None:
        """GM-TC-04 — DUPLICATE_NUMBER (Boundary E005)."""
        grid = [
            [16, 2, 3, 13],
            [5, 11, 0, 8],
            [9, 7, 0, 12],
            [4, 14, 7, 7],
        ]

        output = capture_scenario_output(grid)
        assert output == format_error(DUPLICATE_CODE)
        assert_contract_error_code(DUPLICATE_CODE, DUPLICATE_CODE)

        assert_scenario_golden("GM-TC-04", approve=golden_approve)

    @pytest.mark.golden_master
    def test_gm_tc_05_no_valid_magic_square(
        self, golden_approve: bool
    ) -> None:
        """GM-TC-05 — NO_VALID_MAGIC_SQUARE (Domain UnsolvableDomainError)."""
        grid = [row[:] for row in G3]

        with pytest.raises(UnsolvableDomainError):
            solution(grid)

        output = capture_scenario_output(grid)
        assert output == format_error(NO_VALID_MAGIC_SQUARE_CODE)

        assert_scenario_golden("GM-TC-05", approve=golden_approve)
