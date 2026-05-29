"""
Shared pytest fixtures — G0~G3 grid placeholders (RED Skeleton).

Uncomment and return when GREEN phase wires entity/boundary fixtures.
"""

from __future__ import annotations

# import pytest

# G0 — complete valid 4×4 magic square (0 blanks)
# _G0: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 15, 1],
# ]

# G1 — blanks at (2,2),(3,3) 1-index; missing {7,10}; Step A success
# _G1: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 6, 0, 12],
#     [4, 14, 15, 1],
# ]

# G2 — PRD RD-02; Step A fail, Step B success
# _G2: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 7, 6, 12],
#     [0, 14, 15, 1],
# ]

# G3 — placeholder; Step A·B both fail (confirm before GREEN)
# _G3: list[list[int]] = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 0],
#     [9, 10, 0, 12],
#     [13, 14, 15, 16],
# ]

# @pytest.fixture
# def grid_g0() -> list[list[int]]:
#     return [row[:] for row in _G0]

# @pytest.fixture
# def grid_g1() -> list[list[int]]:
#     return [row[:] for row in _G1]

# @pytest.fixture
# def grid_g2() -> list[list[int]]:
#     return [row[:] for row in _G2]

# @pytest.fixture
# def grid_g3() -> list[list[int]]:
#     return [row[:] for row in _G3]
