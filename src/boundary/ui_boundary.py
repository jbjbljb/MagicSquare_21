"""Boundary UI entry — validate input then delegate to Control resolver."""

from __future__ import annotations

from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.boundary.solve_puzzle import solve_puzzle
from src.control.completion_resolver import TwoCellCompletionResolver


class UIBoundary:
    """Boundary facade for puzzle solve requests."""

    def __init__(
        self,
        completion_resolver: CompletionResolverPort | None = None,
    ) -> None:
        """Wire Control resolver port; defaults to ``TwoCellCompletionResolver``."""
        self._completion_resolver = (
            completion_resolver
            if completion_resolver is not None
            else TwoCellCompletionResolver()
        )

    def solve(
        self, grid: list[list[int]] | None
    ) -> FailureResult | list[int]:
        """
        Validate grid at Boundary; on failure return FailureResult.

        On success delegate to completion_resolver and return int[6] result.
        """
        return solve_puzzle(grid, resolver=self._completion_resolver)
