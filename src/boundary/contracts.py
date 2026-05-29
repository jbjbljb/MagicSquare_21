"""Boundary failure contract constants (PRD §8.1 INVALID_SIZE)."""

from src.control.constants import (
    BLANK_CELL_VALUE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    GRID_SIZE,
    REQUIRED_BLANK_COUNT,
)

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

EMPTY_COUNT_CODE = "E002"
EMPTY_COUNT_MESSAGE = "빈칸(0)은 정확히 2개여야 합니다."

CELL_RANGE_CODE = "E004"
CELL_RANGE_MESSAGE = "셀 값은 0 또는 1~16이어야 합니다."

DUPLICATE_CODE = "E005"
DUPLICATE_MESSAGE = "0을 제외한 값은 중복될 수 없습니다."

NO_SOLUTION_CODE = "E_NO_SOLUTION"
NO_SOLUTION_MESSAGE = "두 빈칸을 채워도 마방진이 되지 않습니다."
