"""Boundary layer — input validation and puzzle solve port."""

from src.boundary.contracts import (
    DUPLICATE_CODE,
    EMPTY_COUNT_CODE,
    INVALID_SIZE_CODE,
    NO_SOLUTION_CODE,
)
from src.boundary.input_validator import InputValidator
from src.boundary.schemas import FailureResult
from src.boundary.solve_puzzle import solve_puzzle
from src.boundary.ui_boundary import UIBoundary

__all__ = [
    "DUPLICATE_CODE",
    "EMPTY_COUNT_CODE",
    "FailureResult",
    "INVALID_SIZE_CODE",
    "InputValidator",
    "NO_SOLUTION_CODE",
    "UIBoundary",
    "solve_puzzle",
]
