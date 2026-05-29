"""
Shared pytest fixtures — G0~G3 grids for entity/control GREEN tests.
"""

from __future__ import annotations

import os

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register Golden Master approve CLI flag."""
    parser.addoption(
        "--approve-golden",
        action="store_true",
        default=False,
        help="Regenerate tests/golden_master_expected.txt from current solver output.",
    )


@pytest.fixture
def golden_approve(request: pytest.FixtureRequest) -> bool:
    """True when Golden Master baseline should be regenerated."""
    cli_approve = request.config.getoption("--approve-golden")
    env_approve = os.environ.get("GOLDEN_MASTER_APPROVE", "") == "1"
    return cli_approve or env_approve

G0: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

G1: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 0],
    [4, 14, 15, 1],
]

G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 6, 12],
    [0, 14, 15, 1],
]

G3: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 0],
    [9, 10, 0, 12],
    [13, 14, 15, 16],
]


@pytest.fixture
def grid_g0() -> list[list[int]]:
    """Complete valid 4×4 magic square."""
    return [row[:] for row in G0]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 partial grid — PRD RD-01; blanks (1,2),(3,4); missing {2,12}."""
    return [row[:] for row in G1]


@pytest.fixture
def grid_g2() -> list[list[int]]:
    """G2 partial grid — Step A fail, Step B success."""
    return [row[:] for row in G2]


@pytest.fixture
def grid_g3() -> list[list[int]]:
    """G3 placeholder — both attempts fail."""
    return [row[:] for row in G3]
