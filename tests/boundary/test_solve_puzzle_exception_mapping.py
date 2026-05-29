"""Boundary exception mapping tests (RF-3-04)."""

from __future__ import annotations

from unittest.mock import create_autospec

from src.boundary.contracts import NO_SOLUTION_CODE, NO_SOLUTION_MESSAGE
from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.boundary.solve_puzzle import solve_puzzle
from src.control.exceptions import UnsolvableDomainError
from tests.conftest import G1, G3


class TestSolvePuzzleExceptionMapping:
    """UnsolvableDomainError is mapped to Boundary FailureResult at solve_puzzle."""

    def test_g3_returns_e_no_solution_failure_result(self) -> None:
        """Valid grid with no completion maps to E_NO_SOLUTION."""
        grid = [row[:] for row in G3]

        result = solve_puzzle(grid)

        assert isinstance(result, FailureResult)
        assert result.code == NO_SOLUTION_CODE
        assert result.message == NO_SOLUTION_MESSAGE

    def test_custom_resolver_unsolvable_maps_to_e_no_solution(self) -> None:
        """Injected resolver raising UnsolvableDomainError maps to E_NO_SOLUTION."""
        grid = [row[:] for row in G1]
        resolver = create_autospec(CompletionResolverPort, instance=True)
        resolver.resolve.side_effect = UnsolvableDomainError("no completion")

        result = solve_puzzle(grid, resolver=resolver)

        assert isinstance(result, FailureResult)
        assert result.code == NO_SOLUTION_CODE
        assert result.message == NO_SOLUTION_MESSAGE
        resolver.resolve.assert_called_once_with(grid)

    def test_invalid_grid_never_calls_resolver(self) -> None:
        """Validation failure returns before resolver; no exception mapping needed."""
        resolver = create_autospec(CompletionResolverPort, instance=True)

        result = solve_puzzle(None, resolver=resolver)

        assert isinstance(result, FailureResult)
        resolver.resolve.assert_not_called()
