"""
Track A — U-OUT-01~03 output contract Full RED.

Mock CompletionResolverPort; G1 valid partial grid with two blanks.
"""

from __future__ import annotations

from unittest.mock import create_autospec

import pytest

from src.boundary.contracts import CELL_VALUE_MAX, CELL_VALUE_MIN, GRID_SIZE
from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.boundary.ui_boundary import UIBoundary
from src.control.completion_resolver import TwoCellCompletionResolver
from src.entity.services.missing_number_finder import find_not_exist_nums

from tests.conftest import G1, G2

_MOCK_SOLUTION: list[int] = [1, 2, 2, 3, 4, 12]


@pytest.fixture
def mock_resolver() -> CompletionResolverPort:
    """Mock Domain resolver returning fixed int[6] success envelope."""
    resolver = create_autospec(CompletionResolverPort, instance=True)
    resolver.resolve.return_value = _MOCK_SOLUTION
    return resolver


@pytest.fixture
def ui_boundary(mock_resolver: CompletionResolverPort) -> UIBoundary:
    """Boundary entry with injectable Control port mock."""
    return UIBoundary(solver_port=mock_resolver)


class TestUOut01To03:
    """U-OUT-01~03 — success output envelope."""

    def test_u_out_01_success_result_length_six(
        self, ui_boundary: UIBoundary
    ) -> None:
        """U-OUT-01 — Success.result is int[6]."""
        # U-OUT-01
        # Given
        grid = [row[:] for row in G1]

        # When
        result = ui_boundary.solve(grid)

        # Then
        assert isinstance(result, list)
        assert len(result) == 6

    def test_u_out_02_success_coordinates_one_indexed(
        self, ui_boundary: UIBoundary
    ) -> None:
        """U-OUT-02 — r,c ∈ [1,4]; n ∈ [1,16]."""
        # U-OUT-02
        # Given
        grid = [row[:] for row in G1]

        # When
        result = ui_boundary.solve(grid)

        # Then
        assert isinstance(result, list)
        r1, c1, n1, r2, c2, n2 = result
        assert CELL_VALUE_MIN <= r1 <= GRID_SIZE
        assert CELL_VALUE_MIN <= c1 <= GRID_SIZE
        assert CELL_VALUE_MIN <= r2 <= GRID_SIZE
        assert CELL_VALUE_MIN <= c2 <= GRID_SIZE
        assert CELL_VALUE_MIN <= n1 <= CELL_VALUE_MAX
        assert CELL_VALUE_MIN <= n2 <= CELL_VALUE_MAX

    def test_u_out_03_success_missing_numbers_match_domain_pair(
        self, ui_boundary: UIBoundary
    ) -> None:
        """U-OUT-03 — n1,n2 are the two missing numbers (small-first or reverse)."""
        # U-OUT-03
        # Given
        grid = [row[:] for row in G1]

        # When
        result = ui_boundary.solve(grid)

        # Then
        assert isinstance(result, list)
        small, large = find_not_exist_nums(grid)
        assert {result[2], result[5]} == {small, large}

    def test_u_out_03_reverse_path_allows_descending_numbers_in_tuple(
        self,
    ) -> None:
        """U-OUT-03 — reverse success may return n1 > n2 (D-SOL-02 alignment)."""
        # Given
        grid = [row[:] for row in G2]
        ui_boundary = UIBoundary(solver_port=TwoCellCompletionResolver())

        # When
        result = ui_boundary.solve(grid)

        # Then
        assert isinstance(result, list)
        small, large = find_not_exist_nums(grid)
        assert {result[2], result[5]} == {small, large}
        assert result[2] == large
        assert result[5] == small
