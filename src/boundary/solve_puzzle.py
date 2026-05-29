"""Boundary entry: validate input then delegate to Control resolver."""

from __future__ import annotations

from src.boundary.contracts import NO_SOLUTION_CODE, NO_SOLUTION_MESSAGE
from src.boundary.input_validator import InputValidator
from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.control.completion_resolver import TwoCellCompletionResolver
from src.control.exceptions import UnsolvableDomainError

_validator = InputValidator()
_default_resolver = TwoCellCompletionResolver()


def solve_puzzle(
    grid: list[list[int]] | None,
    resolver: CompletionResolverPort | None = None,
) -> FailureResult | list[int]:
    """
    Validate grid at Boundary; on failure return FailureResult without calling resolver.

    On success delegate to Control resolver and return int[6] solution.
    Maps ``UnsolvableDomainError`` to ``FailureResult(E_NO_SOLUTION)``.
    """
    failure = _validator.validate(grid)
    if failure is not None:
        return failure
    active_resolver = resolver if resolver is not None else _default_resolver
    assert grid is not None
    try:
        return active_resolver.resolve(grid)
    except UnsolvableDomainError:
        return FailureResult(
            code=NO_SOLUTION_CODE,
            message=NO_SOLUTION_MESSAGE,
        )
