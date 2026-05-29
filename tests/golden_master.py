"""Golden Master capture, serialization, and approve-pattern comparison (GM-2)."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

from src.boundary.contracts import GRID_SIZE
from src.boundary.input_validator import InputValidator
from src.control.exceptions import UnsolvableDomainError
from src.control.two_cell_solver import solution
from src.entity.constants import CELL_VALUE_MAX, CELL_VALUE_MIN
from src.entity.services.empty_cell_locator import find_blank_coords
from src.entity.services.missing_number_finder import find_not_exist_nums
from tests.conftest import G1, G2, G3

EXPECTED_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"
SECTION_SEPARATOR = "\n\n" + ("_" * 40) + "\n\n"
SECTION_HEADER_PATTERN = re.compile(r"^\[(GM-TC-\d{2})\]$", re.MULTILINE)

# GM-TC-05 domain failure — serialized until Boundary E_NO_SOLUTION GREEN
NO_VALID_MAGIC_SQUARE_CODE = "UnsolvableDomainError"


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

_validator = InputValidator()


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


def capture_scenario_output(grid: list[list[int]]) -> str:
    """
    Capture solver API result for one grid.

    Boundary validation failures return Error code; valid grids delegate to
    ``solution`` which may return int[6] or raise ``UnsolvableDomainError``.
    """
    failure = _validator.validate(grid)
    if failure is not None:
        return format_error(failure.code)
    try:
        return format_output(solution(grid))
    except UnsolvableDomainError:
        return format_error(NO_VALID_MAGIC_SQUARE_CODE)


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
    """Build unified diff with --- expected / +++ actual headers."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )


def write_expected(path: Path | None = None) -> Path:
    """Write Golden Master baseline file from current solver output."""
    target = path or EXPECTED_PATH
    target.write_text(build_expected_document(), encoding="utf-8")
    return target


def read_expected(path: Path | None = None) -> str:
    """Read Golden Master baseline file content."""
    target = path or EXPECTED_PATH
    return target.read_text(encoding="utf-8")


def assert_contract_int6(result: list[int]) -> None:
    """Verify int[6] envelope, 1-index coordinates, and value range."""
    assert len(result) == 6
    row1, col1, num1, row2, col2, num2 = result
    for row, col in ((row1, col1), (row2, col2)):
        assert CELL_VALUE_MIN <= row <= GRID_SIZE
        assert CELL_VALUE_MIN <= col <= GRID_SIZE
    for num in (num1, num2):
        assert CELL_VALUE_MIN <= num <= CELL_VALUE_MAX


def assert_contract_row_major(grid: list[list[int]], result: list[int]) -> None:
    """Verify blank coordinates follow row-major 1-index order."""
    (expected_r1, expected_c1), (expected_r2, expected_c2) = find_blank_coords(grid)
    row1, col1, _, row2, col2, _ = result
    assert (row1, col1) == (expected_r1, expected_c1)
    assert (row2, col2) == (expected_r2, expected_c2)


def assert_contract_small_first(grid: list[list[int]], result: list[int]) -> None:
    """Verify small-first attempt: smaller missing number placed first."""
    small, large = find_not_exist_nums(grid)
    _, _, num1, _, _, num2 = result
    assert num1 == small
    assert num2 == large
    assert num1 < num2


def assert_contract_reverse_fallback(grid: list[list[int]], result: list[int]) -> None:
    """Verify reverse fallback: larger missing number placed first."""
    small, large = find_not_exist_nums(grid)
    _, _, num1, _, _, num2 = result
    assert num1 == large
    assert num2 == small
    assert num1 > num2


def assert_contract_error_code(actual_code: str, expected_code: str) -> None:
    """Verify Error Contract code matches Boundary/Domain policy."""
    assert actual_code == expected_code


def assert_scenario_golden(
    test_id: str,
    *,
    path: Path | None = None,
    approve: bool = False,
) -> None:
    """
    Approve-pattern Golden Master assertion for one GM-TC scenario.

    When baseline is missing or ``approve`` is True, write/update full baseline.
    Otherwise compare the scenario section: open(expected).read() vs actual.
    """
    scenario = SCENARIO_BY_ID[test_id]
    target = path or EXPECTED_PATH
    actual_section = serialize_section(scenario)

    if approve or not target.is_file():
        write_expected(target)
        return

    expected_content = read_expected(target)
    expected_sections = parse_expected_sections(expected_content)

    if test_id not in expected_sections:
        write_expected(target)
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
