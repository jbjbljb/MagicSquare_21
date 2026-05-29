"""Control re-exports of entity domain constants for Boundary contract alignment."""

from src.entity.constants import (
    BLANK_CELL_VALUE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    GRID_SIZE,
    MAGIC_SUM,
    REQUIRED_BLANK_COUNT,
    SOLUTION_VECTOR_LENGTH,
)

__all__ = [
    "BLANK_CELL_VALUE",
    "CELL_VALUE_MAX",
    "CELL_VALUE_MIN",
    "GRID_SIZE",
    "MAGIC_SUM",
    "REQUIRED_BLANK_COUNT",
    "SOLUTION_VECTOR_LENGTH",
]
