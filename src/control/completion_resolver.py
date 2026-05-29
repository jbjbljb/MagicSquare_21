"""Control adapter implementing Boundary CompletionResolverPort."""

from __future__ import annotations

from src.control.two_cell_solver import solution


class TwoCellCompletionResolver:
    """Delegates validated grids to the two-cell Control solver."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Return int[6] solution; may raise ``UnsolvableDomainError``."""
        return solution(grid)
