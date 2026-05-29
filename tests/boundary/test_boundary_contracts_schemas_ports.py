"""Dedicated unit tests for Boundary contracts, schemas, and ports (RF-3-03)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.boundary.contracts import (
    BLANK_CELL_VALUE,
    CELL_RANGE_MESSAGE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    DUPLICATE_CODE,
    EMPTY_COUNT_CODE,
    GRID_SIZE,
    GRID_SIZE_LABEL,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    NO_SOLUTION_CODE,
    NO_SOLUTION_MESSAGE,
    REQUIRED_BLANK_COUNT,
    SOLUTION_VECTOR_LENGTH,
)
from src.boundary.schemas import FailureResult
from src.control.completion_resolver import TwoCellCompletionResolver
from tests.conftest import G1


class TestBoundaryContracts:
    """contracts.py — derived labels and PRD-aligned messages."""

    def test_grid_size_label_matches_grid_size(self) -> None:
        """GRID_SIZE_LABEL reflects GRID_SIZE without hard-coded drift."""
        assert GRID_SIZE_LABEL == f"{GRID_SIZE}x{GRID_SIZE}"

    def test_invalid_size_message_uses_grid_size_label(self) -> None:
        """INVALID_SIZE message is derived from GRID_SIZE_LABEL."""
        assert INVALID_SIZE_MESSAGE == f"Grid must be {GRID_SIZE_LABEL}."
        assert INVALID_SIZE_CODE == "INVALID_SIZE"

    def test_cell_range_message_uses_blank_and_value_range(self) -> None:
        """E004 message references BLANK_CELL_VALUE and min/max cell values."""
        assert str(BLANK_CELL_VALUE) in CELL_RANGE_MESSAGE
        assert str(CELL_VALUE_MIN) in CELL_RANGE_MESSAGE
        assert str(CELL_VALUE_MAX) in CELL_RANGE_MESSAGE

    def test_required_blank_count_is_two(self) -> None:
        """REQUIRED_BLANK_COUNT matches PRD BR-02."""
        assert REQUIRED_BLANK_COUNT == 2

    def test_no_solution_contract_constants(self) -> None:
        """E_NO_SOLUTION code and message are fixed Boundary contract strings."""
        assert NO_SOLUTION_CODE == "E_NO_SOLUTION"
        assert NO_SOLUTION_MESSAGE == "두 빈칸을 채워도 마방진이 되지 않습니다."

    def test_error_codes_are_distinct(self) -> None:
        """Boundary failure codes do not collide."""
        codes = {
            INVALID_SIZE_CODE,
            EMPTY_COUNT_CODE,
            "E004",
            DUPLICATE_CODE,
            NO_SOLUTION_CODE,
        }
        assert len(codes) == 5


class TestBoundarySchemas:
    """schemas.py — FailureResult envelope."""

    def test_failure_result_stores_code_and_message(self) -> None:
        """FailureResult exposes immutable code and message fields."""
        result = FailureResult(code=EMPTY_COUNT_CODE, message="test message")

        assert result.code == EMPTY_COUNT_CODE
        assert result.message == "test message"

    def test_failure_result_is_frozen(self) -> None:
        """FailureResult rejects attribute mutation."""
        result = FailureResult(code=DUPLICATE_CODE, message="dup")

        with pytest.raises(ValidationError):
            result.code = "E999"  # type: ignore[misc]

    def test_failure_result_requires_code_and_message(self) -> None:
        """FailureResult rejects missing required fields."""
        with pytest.raises(ValidationError):
            FailureResult(code=INVALID_SIZE_CODE)  # type: ignore[call-arg]


class TestBoundaryPorts:
    """ports.py — CompletionResolverPort structural contract."""

    def test_two_cell_completion_resolver_exposes_resolve(self) -> None:
        """Default Control adapter implements resolve(grid) -> list[int]."""
        resolver = TwoCellCompletionResolver()
        grid = [row[:] for row in G1]

        result = resolver.resolve(grid)

        assert isinstance(result, list)
        assert len(result) == SOLUTION_VECTOR_LENGTH
