"""Boundary entry: validate input then delegate to Domain resolver."""

from __future__ import annotations

from src.boundary.input_validator import InputValidator
from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult

_validator = InputValidator()


def solve_puzzle(
    grid: list[list[int]] | None,
    resolver: CompletionResolverPort | None = None,
) -> FailureResult | list[int]:
    """
    Validate grid at Boundary; on failure return FailureResult without calling resolver.

    On success delegate to resolver and return int[6] solution.
    """
    failure = _validator.validate(grid)
    if failure is not None:
        return failure
    if resolver is None:
        raise NotImplementedError(
            "RED: Domain resolver required for valid grid"
        )
    return resolver.resolve(grid)
