"""Boundary UI entry — validate input then delegate to Domain resolver."""

from __future__ import annotations

from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.boundary.solve_puzzle import solve_puzzle


class UIBoundary:
    """Boundary facade for puzzle solve requests."""

    def __init__(self, solver_port: CompletionResolverPort | None = None) -> None:
        """Wire optional Domain resolver port for solve delegation."""
        self._solver_port = solver_port

    def solve(
        self, grid: list[list[int]] | None
    ) -> FailureResult | list[int]:
        """
        Validate grid at Boundary; on failure return FailureResult.

        On success delegate to solver_port and return int[6] result.
        """
        return solve_puzzle(grid, resolver=self._solver_port)
