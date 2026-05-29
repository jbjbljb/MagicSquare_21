"""Golden Master capture, serialization, and approve-pattern comparison (GM-2)."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

from src.boundary.schemas import FailureResult
from src.boundary.solve_puzzle import solve_puzzle
from src.boundary.ui_boundary import UIBoundary
from tests.conftest import G1, G2, G3

EXPECTED_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"
SECTION_SEPARATOR = "\n\n" + ("_" * 40) + "\n\n"
SECTION_HEADER_PATTERN = re.compile(r"^\[(GM-TC-\d{2})\]$", re.MULTILINE)


@dataclass(frozen=True)
class GoldenScenario:
    """Single Golden Master scenario definition."""

    test_id: str
    name: str
    grid: list[list[int]]


SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario("GM-TC-01", "normal_success", [row[:] for row in G1]),
    GoldenScenario("GM-TC-02", "reverse_success", [row[:] for row in G2]),
    GoldenScenario(
        "GM-TC-03",
        "INVALID_BLANK_COUNT",
        [
            [16, 2, 3, 13],
            [5, 11, 0, 8],
            [9, 7, 0, 12],
            [0, 14, 15, 1],
        ],
    ),
    GoldenScenario(
        "GM-TC-04",
        "DUPLICATE_NUMBER",
        [
            [16, 2, 3, 13],
            [5, 11, 0, 8],
            [9, 7, 0, 12],
            [4, 14, 7, 7],
        ],
    ),
    GoldenScenario(
        "GM-TC-05",
        "NO_VALID_MAGIC_SQUARE",
        [row[:] for row in G3],
    ),
)

SCENARIO_BY_ID: dict[str, GoldenScenario] = {
    scenario.test_id: scenario for scenario in SCENARIOS
}


def format_grid(grid: list[list[int]]) -> str:
    """Render grid rows as space-separated integers."""
    lines = ["Input:"]
    lines.extend(" ".join(str(cell) for cell in row) for row in grid)
    return "\n".join(lines)


def format_output(result: list[int]) -> str:
    """Serialize success API result as compact int[6] list."""
    compact = ",".join(str(value) for value in result)
    return f"Output:\n[{compact}]"


def format_error(code: str) -> str:
    """Serialize failure API result for Golden Master comparison."""
    return f"Error:\n{code}"


def _format_boundary_result(result: FailureResult | list[int]) -> str:
    """Serialize Boundary solve result for Golden Master comparison."""
    if isinstance(result, FailureResult):
        return format_error(result.code)
    return format_output(result)


def capture_scenario_output(grid: list[list[int]]) -> str:
    """
    Capture Boundary solve result for one grid via ``solve_puzzle``.

    Validation failures return Error code; unsolvable grids return ``E_NO_SOLUTION``.
    """
    return _format_boundary_result(solve_puzzle(grid))


def capture_ui_boundary_output(grid: list[list[int]] | None) -> str:
    """Capture Boundary solve result via ``UIBoundary`` facade (RF-3-05)."""
    return _format_boundary_result(UIBoundary().solve(grid))


def serialize_section(scenario: GoldenScenario) -> str:
    """Serialize one named scenario block."""
    output = capture_scenario_output([row[:] for row in scenario.grid])
    header = f"[{scenario.test_id}]"
    return normalize_section("\n".join((header, format_grid(scenario.grid), output)))


def build_expected_document() -> str:
    """Build full Golden Master document from live solver output."""
    sections = [serialize_section(scenario) for scenario in SCENARIOS]
    return SECTION_SEPARATOR.join(sections) + "\n"


def normalize_section(text: str) -> str:
    """Strip separators and normalize trailing newline for section comparison."""
    cleaned = text.strip()
    cleaned = re.split(r"\n+_{10,}\n*", cleaned, maxsplit=1)[0].strip()
    return cleaned + "\n"


def parse_expected_sections(content: str) -> dict[str, str]:
    """Parse Golden Master file into per-TC section text keyed by GM-TC id."""
    matches = list(SECTION_HEADER_PATTERN.finditer(content))
    if not matches:
        return {}

    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        test_id = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections[test_id] = normalize_section(content[start:end])
    return sections


def unified_diff(expected: str, actual: str, label: str) -> str:
    """Build unified diff with scenario-labelled expected/actual headers."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"expected/{label}",
            tofile=f"actual/{label}",
        )
    )


def write_expected(path: Path | None = None) -> Path:
    """Write Golden Master baseline file from current solver output."""
    target = path or EXPECTED_PATH
    target.write_text(build_expected_document(), encoding="utf-8")
    return target


def write_section(path: Path, test_id: str, section_text: str) -> None:
    """
    Merge one scenario section into the baseline file.

    Avoids full-file rewrite on approve to reduce xdist worker contention (RF-3-02).
    """
    target = path
    normalized = normalize_section(section_text)

    if not target.is_file():
        write_expected(target)
        return

    sections = parse_expected_sections(read_expected(target))
    sections[test_id] = normalized
    ordered = [
        sections[scenario.test_id]
        for scenario in SCENARIOS
        if scenario.test_id in sections
    ]
    if len(ordered) != len(SCENARIOS):
        write_expected(target)
        return

    target.write_text(SECTION_SEPARATOR.join(ordered) + "\n", encoding="utf-8")


def read_expected(path: Path | None = None) -> str:
    """Read Golden Master baseline file content."""
    target = path or EXPECTED_PATH
    return target.read_text(encoding="utf-8")


def assert_scenario_golden(
    test_id: str,
    *,
    path: Path | None = None,
    approve: bool = False,
) -> None:
    """
    Approve-pattern Golden Master assertion for one GM-TC scenario.

    When ``approve`` is True, update only the matching section in the baseline.
    Otherwise compare the scenario section against stored expected output.
    """
    scenario = SCENARIO_BY_ID[test_id]
    target = path or EXPECTED_PATH
    actual_section = serialize_section(scenario)

    if approve:
        write_section(target, test_id, actual_section)
        return

    if not target.is_file():
        write_expected(target)
        return

    expected_content = read_expected(target)
    expected_sections = parse_expected_sections(expected_content)

    if test_id not in expected_sections:
        write_section(target, test_id, actual_section)
        return

    expected_section = expected_sections[test_id]
    actual_normalized = normalize_section(actual_section)
    if actual_normalized == expected_section:
        return

    diff = unified_diff(expected_section, actual_normalized, test_id)
    raise AssertionError(
        f"Golden Master mismatch for {test_id}. "
        "Re-run with `pytest -m golden_master --approve-golden -v` to update.\n"
        f"{diff}"
    )
