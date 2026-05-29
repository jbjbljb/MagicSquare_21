"""Boundary-facing ports (Domain entry points)."""

from typing import Protocol


class CompletionResolverPort(Protocol):
    """Domain completion resolver — must not run on invalid grid."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Resolve puzzle for a validated 4x4 grid."""
        ...
