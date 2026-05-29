"""
AC-FR-01-01; PRD §8.1 INVALID_SIZE — Boundary null/shape 선행 실패 RED tests.

Scope: grid=None and shape-related boundary inputs only.
Excluded: AC-FR-01-02~05 detail codes, FR-02~05 Domain logic.
"""

from __future__ import annotations

from unittest.mock import create_autospec

import pytest

from src.boundary.contracts import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.boundary.solve_puzzle import solve_puzzle

# PRD §8.1 — INVALID_SIZE contract (byte-exact message for assertions)
_EXPECTED_CODE = INVALID_SIZE_CODE
_EXPECTED_MESSAGE = INVALID_SIZE_MESSAGE

# AC-FR-01-02~05 / FR-02~05 — must not appear in this module's assertions
_FORBIDDEN_AC_SCOPE_CODES = frozenset(
    {
        "E_NULL_INPUT",
        "E_DIM_ROWS",
        "E_DIM_COLS",
        "E_CELL_RANGE",
        "E_EMPTY_COUNT",
        "E_DUPLICATE",
        "E_NO_SOLUTION",
    }
)


@pytest.fixture
def mock_resolver() -> CompletionResolverPort:
    """Spy-ready Domain resolver mock (resolve must stay uncalled on failure)."""
    return create_autospec(CompletionResolverPort, instance=True)


def _grid_3x4() -> list[list[int]]:
    return [[0] * 4 for _ in range(3)]


class TestAcFr0101InvalidSize:
    """AC-FR-01-01; PRD §8.1 INVALID_SIZE."""

    def test_none_grid_returns_invalid_size_failure_result(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — Happy Path of Failure."""
        # AC-FR-01-01
        # Given
        grid = None

        # When
        result = solve_puzzle(grid, resolver=mock_resolver)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == _EXPECTED_CODE
        assert result.message == _EXPECTED_MESSAGE

    def test_none_grid_code_is_exactly_invalid_size_string(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — code field exact match."""
        # AC-FR-01-01
        # Given
        grid = None

        # When
        result = solve_puzzle(grid, resolver=mock_resolver)

        # Then
        assert result.code == "INVALID_SIZE"
        assert type(result.code) is str

    def test_none_grid_message_matches_prd_section_8_1_byte_for_byte(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — message byte-exact."""
        # AC-FR-01-01
        # Given
        grid = None
        expected_message = "Grid must be 4x4."

        # When
        result = solve_puzzle(grid, resolver=mock_resolver)

        # Then
        assert result.message == expected_message
        assert len(result.message) == len(expected_message)
        assert result.message == _EXPECTED_MESSAGE

    def test_none_grid_resolve_called_zero_times_isolation(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — Domain resolve() not invoked."""
        # AC-FR-01-01
        # Given
        grid = None

        # When
        solve_puzzle(grid, resolver=mock_resolver)

        # Then
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]
        assert mock_resolver.resolve.call_count == 0  # type: ignore[attr-defined]

    def test_empty_list_grid_returns_invalid_size_failure(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — boundary grid=[]."""
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []

        # When
        result = solve_puzzle(grid, resolver=mock_resolver)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == _EXPECTED_CODE
        assert result.message == _EXPECTED_MESSAGE
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_four_empty_rows_grid_returns_invalid_size_failure(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — boundary grid=[[]]*4."""
        # AC-FR-01-01
        # Given
        grid = [[]] * 4

        # When
        result = solve_puzzle(grid, resolver=mock_resolver)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == _EXPECTED_CODE
        assert result.message == _EXPECTED_MESSAGE
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_3x4_grid_returns_invalid_size_failure(
        self, mock_resolver: CompletionResolverPort
    ) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — boundary 3×4 shape."""
        # AC-FR-01-01
        # Given
        grid = _grid_3x4()

        # When
        result = solve_puzzle(grid, resolver=mock_resolver)

        # Then
        assert isinstance(result, FailureResult)
        assert result.code == _EXPECTED_CODE
        assert result.message == _EXPECTED_MESSAGE
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_scope_contract_is_invalid_size_not_other_ac_codes(self) -> None:
        """AC-FR-01-01; PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 codes excluded from module."""
        # AC-FR-01-01
        # Given / When / Then — scope guard for this RED commit
        assert _EXPECTED_CODE == "INVALID_SIZE"
        assert _EXPECTED_CODE not in _FORBIDDEN_AC_SCOPE_CODES
        assert _EXPECTED_MESSAGE == "Grid must be 4x4."
