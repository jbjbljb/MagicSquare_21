"""Boundary entry: validate input then delegate to Domain resolver."""

from __future__ import annotations

from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult


def solve_puzzle(
    grid: list[list[int]] | None,
    resolver: CompletionResolverPort | None = None,
) -> FailureResult:
    """
    Validate grid at Boundary; on failure return FailureResult without calling resolver.

    RED: not implemented — tests must fail until GREEN.
    """
    raise NotImplementedError(
        "RED: implement Boundary validation and INVALID_SIZE failure response"
    )
