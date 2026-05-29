"""Boundary-facing ports (Control entry points)."""

from typing import Protocol

from src.control.constants import GRID_SIZE

_GRID_LABEL = f"{GRID_SIZE}x{GRID_SIZE}"


class CompletionResolverPort(Protocol):
    """Control completion resolver — must not run on invalid grid."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        f"""
        Resolve puzzle for a validated {_GRID_LABEL} grid.

        May raise ``UnsolvableDomainError`` when no valid completion exists.
        """
        ...
