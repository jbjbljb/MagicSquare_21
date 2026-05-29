"""
Track B — D-VAL-01~06 MagicSquareValidator / is_magic_square Full RED.

Domain Mock prohibited.
"""

from __future__ import annotations

from src.entity.services.magic_square_validator import is_magic_square
from tests.conftest import G0

_GRID_DUPLICATE_SEVEN: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 7, 1],
]


class TestDVal01To06:
    """D-VAL-01~06 — is_magic_square invariant."""

    def test_d_val_01_is_magic_square_true_on_g0(self) -> None:
        """D-VAL-01 — G0 complete grid → True."""
        # D-VAL-01
        # Given
        grid = [row[:] for row in G0]

        # When
        result = is_magic_square(grid)

        # Then
        assert result is True

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        """D-VAL-02 — G0 with row sum broken → False."""
        # D-VAL-02
        # Given
        grid = [row[:] for row in G0]
        grid[0][0] = 15

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_03_column_sum_mismatch_returns_false(self) -> None:
        """D-VAL-03 — G0 with column sum broken → False."""
        # D-VAL-03
        # Given
        grid = [row[:] for row in G0]
        grid[0][1] = 20

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_04_diagonal_sum_mismatch_returns_false(self) -> None:
        """D-VAL-04 — G0 with main diagonal broken → False."""
        # D-VAL-04
        # Given
        grid = [row[:] for row in G0]
        grid[0][0] = 1
        grid[3][3] = 16

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_05_duplicate_values_returns_false(self) -> None:
        """D-VAL-05 — full grid with duplicate 7, no zeros → False."""
        # D-VAL-05
        # Given
        grid = [row[:] for row in _GRID_DUPLICATE_SEVEN]

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_06_contains_zero_returns_false(self) -> None:
        """D-VAL-06 — G0 with one cell set to 0 → False."""
        # D-VAL-06
        # Given
        grid = [row[:] for row in G0]
        grid[1][2] = 0

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False
