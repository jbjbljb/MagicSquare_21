"""
Track B — D-VAL-01~06 MagicSquareValidator / is_magic_square RED skeletons.

Domain Mock prohibited. G0 and derived matrices commented until GREEN.
"""

from __future__ import annotations

import pytest

from entity.services.magic_square_validator import is_magic_square

# G0 — complete magic square (no zeros)
# _G0: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 15, 1],
# ]


class TestDVal01To06:
    """D-VAL-01~06 — is_magic_square invariant RED skeletons."""

    def test_d_val_01_is_magic_square_true_on_g0(self) -> None:
        """D-VAL-01 — G0 complete grid → True."""
        # Given
        # grid = _G0
        # When
        # result = is_magic_square(grid)
        pytest.fail("RED: D-VAL-01 — G0 complete magic square → True")

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        """D-VAL-02 — G0 with row sum broken → False."""
        # Given
        # grid = copy G0; grid[0][0] = 15  # was 16
        # When
        # result = is_magic_square(grid)
        pytest.fail("RED: D-VAL-02 — row sum mismatch → False")

    def test_d_val_03_column_sum_mismatch_returns_false(self) -> None:
        """D-VAL-03 — G0 with column sum broken → False."""
        # Given
        # grid = copy G0; grid[0][1] = 20  # was 2
        # When
        # result = is_magic_square(grid)
        pytest.fail("RED: D-VAL-03 — column sum mismatch → False")

    def test_d_val_04_diagonal_sum_mismatch_returns_false(self) -> None:
        """D-VAL-04 — G0 with main diagonal broken → False."""
        # Given
        # grid = modified G0 breaking D1 only (no zeros)
        # When
        # result = is_magic_square(grid)
        pytest.fail("RED: D-VAL-04 — diagonal sum mismatch → False")

    def test_d_val_05_duplicate_values_returns_false(self) -> None:
        """D-VAL-05 — full grid with duplicate 7, no zeros → False."""
        # Given
        # grid = 4×4 complete with 7 appearing twice
        # When
        # result = is_magic_square(grid)
        pytest.fail("RED: D-VAL-05 — duplicate in 1..16 → False")

    def test_d_val_06_contains_zero_returns_false(self) -> None:
        """D-VAL-06 — G0 with one cell set to 0 → False."""
        # Given
        # grid = copy G0; grid[1][2] = 0
        # When
        # result = is_magic_square(grid)
        pytest.fail("RED: D-VAL-06 — grid contains 0 → False")
