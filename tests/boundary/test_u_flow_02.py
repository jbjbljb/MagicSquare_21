"""
Track A — U-FLOW-02 (extended) Domain isolation Full RED.

Invalid inputs must keep CompletionResolverPort.resolve call_count == 0.
"""

from __future__ import annotations

from unittest.mock import create_autospec

import pytest

from src.boundary.ports import CompletionResolverPort
from src.boundary.schemas import FailureResult
from src.boundary.ui_boundary import UIBoundary

_MATRIX_THREE_BLANKS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [0, 14, 15, 1],
]

_MATRIX_CELL_17: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 17],
]

_MATRIX_DUPLICATE: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 0, 12],
    [4, 14, 7, 7],
]

_MATRIX_ONE_BLANK: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [0, 14, 15, 1],
]


@pytest.fixture
def mock_resolver() -> CompletionResolverPort:
    """Spy-ready Domain resolver mock (resolve must stay uncalled on failure)."""
    return create_autospec(CompletionResolverPort, instance=True)


@pytest.fixture
def ui_boundary_with_spy(mock_resolver: CompletionResolverPort) -> UIBoundary:
    """UIBoundary with resolve spy."""
    return UIBoundary(completion_resolver=mock_resolver)


class TestUFlow02Extended:
    """U-FLOW-02 — invalid input never calls Domain resolve."""

    def test_u_flow_02_null_matrix_execute_never_called(
        self,
        ui_boundary_with_spy: UIBoundary,
        mock_resolver: CompletionResolverPort,
    ) -> None:
        """U-FLOW-02 — matrix=null → resolve.call_count == 0."""
        # U-FLOW-02
        # Given
        matrix = None

        # When
        result = ui_boundary_with_spy.solve(matrix)

        # Then
        assert isinstance(result, FailureResult)
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_u_flow_02_three_blanks_execute_never_called(
        self,
        ui_boundary_with_spy: UIBoundary,
        mock_resolver: CompletionResolverPort,
    ) -> None:
        """U-FLOW-02 ext — E002 path (3 blanks) → resolve 0 calls."""
        # U-FLOW-02
        # Given
        matrix = _MATRIX_THREE_BLANKS

        # When
        result = ui_boundary_with_spy.solve(matrix)

        # Then
        assert isinstance(result, FailureResult)
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_u_flow_02_out_of_range_execute_never_called(
        self,
        ui_boundary_with_spy: UIBoundary,
        mock_resolver: CompletionResolverPort,
    ) -> None:
        """U-FLOW-02 ext — E004 path → resolve 0 calls."""
        # U-FLOW-02
        # Given
        matrix = _MATRIX_CELL_17

        # When
        result = ui_boundary_with_spy.solve(matrix)

        # Then
        assert isinstance(result, FailureResult)
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_u_flow_02_duplicate_execute_never_called(
        self,
        ui_boundary_with_spy: UIBoundary,
        mock_resolver: CompletionResolverPort,
    ) -> None:
        """U-FLOW-02 ext — E005 path → resolve 0 calls."""
        # U-FLOW-02
        # Given
        matrix = _MATRIX_DUPLICATE

        # When
        result = ui_boundary_with_spy.solve(matrix)

        # Then
        assert isinstance(result, FailureResult)
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]

    def test_u_flow_02_one_blank_execute_never_called(
        self,
        ui_boundary_with_spy: UIBoundary,
        mock_resolver: CompletionResolverPort,
    ) -> None:
        """U-FLOW-02 ext — U-IN-07 RD-04 → resolve 0 calls."""
        # U-FLOW-02
        # Given
        matrix = _MATRIX_ONE_BLANK

        # When
        result = ui_boundary_with_spy.solve(matrix)

        # Then
        assert isinstance(result, FailureResult)
        mock_resolver.resolve.assert_not_called()  # type: ignore[attr-defined]
