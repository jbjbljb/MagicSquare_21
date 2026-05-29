# MagicSquare — Defect List (RED Phase)

| 항목 | 내용 |
|------|------|
| **문서 ID** | DL-MAGICSQUARE-RED-001 |
| **작성일** | 2026-05-29 |
| **기준 테스트** | `tests/boundary/test_fr01_01_invalid_size.py` |
| **실행 명령** | `pytest tests/boundary/test_fr01_01_invalid_size.py -v` |
| **최종 실행 결과** | **7 failed**, 1 passed (scope guard) |
| **관련 AC** | AC-FR-01-01 (PRD §8.1 `INVALID_SIZE` 계약) |
| **상태** | Open — GREEN 미착수 |

---

## 결함 요약

| Severity | 건수 |
|----------|------|
| Critical | 2 |
| High | 5 |
| **합계** | **7** |

**공통 근본 원인:** `src/boundary/solve_puzzle.py`의 `solve_puzzle()`이 Boundary 입력 검증 및 `FailureResult` 반환을 구현하지 않고 `NotImplementedError`만 발생시킴.

---

## 결함 목록

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | AC-FR-01-01 | 1. `pytest tests/boundary/test_fr01_01_invalid_size.py::TestAcFr0101InvalidSize::test_none_grid_returns_invalid_size_failure_result -v` 2. 또는 `solve_puzzle(grid=None, resolver=mock)` 호출 | `FailureResult(code="INVALID_SIZE", message="Grid must be 4x4.")` 반환 | `NotImplementedError: RED: implement Boundary validation and INVALID_SIZE failure response` (`solve_puzzle.py:18`) | `grid is None` 분기 및 INVALID_SIZE 실패 응답 미구현 | `solve_puzzle()` 선두에 `if grid is None:` 검사 추가 후 `FailureResult(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)` 반환 |
| DEF-002 | Critical | AC-FR-01-01 | 1. `test_none_grid_resolve_called_zero_times_isolation` 실행 2. `grid=None`, `mock_resolver` 주입 후 `solve_puzzle()` 호출 3. `mock_resolver.resolve.call_count` 확인 | `resolve()` **0회** 호출 후 실패 응답 반환 | `NotImplementedError`로 조기 종료 — mock 호출 여부 검증 전에 예외 발생 | 검증 실패 시 Domain 진입점 호출 차단 로직 없음 | DEF-001과 동일: null/shape 실패 시 `resolver.resolve()` 호출 없이 즉시 `FailureResult` 반환 |
| DEF-003 | High | AC-FR-01-01 | 1. `test_none_grid_code_is_exactly_invalid_size_string` 실행 2. `grid=None` | `result.code == "INVALID_SIZE"` (str, 정확 일치) | `NotImplementedError` | 실패 응답 객체 자체 미생성 | `FailureResult`에 `code=INVALID_SIZE_CODE` 설정 |
| DEF-004 | High | AC-FR-01-01 | 1. `test_none_grid_message_matches_prd_section_8_1_byte_for_byte` 실행 2. `grid=None` | `result.message == "Grid must be 4x4."` (문자 단위 동일) | `NotImplementedError` | PRD §8.1 고정 메시지 미반환 | `message=INVALID_SIZE_MESSAGE` (`contracts.py` 상수) 반환 |
| DEF-005 | High | AC-FR-01-01 | 1. `test_empty_list_grid_returns_invalid_size_failure` 실행 2. `grid=[]` | `FailureResult(INVALID_SIZE)` + `resolve()` 미호출 | `NotImplementedError` | 4×4 shape 검증(빈 리스트) 미구현 | `len(grid) != 4` 또는 빈 리스트 조건에서 INVALID_SIZE 반환 |
| DEF-006 | High | AC-FR-01-01 | 1. `test_four_empty_rows_grid_returns_invalid_size_failure` 실행 2. `grid=[[]] * 4` | `FailureResult(INVALID_SIZE)` + `resolve()` 미호출 | `NotImplementedError` | 열 길이 0인 4행 입력에 대한 shape 검증 미구현 | 각 행 `len(row) != 4` 검사 후 INVALID_SIZE 반환 |
| DEF-007 | High | AC-FR-01-01 | 1. `test_3x4_grid_returns_invalid_size_failure` 실행 2. `grid=[[0]*4 for _ in range(3)]` | `FailureResult(INVALID_SIZE)` + `resolve()` 미호출 | `NotImplementedError` | 행 개수 3인 입력에 대한 shape 검증 미구현 | `len(grid) != 4` 시 INVALID_SIZE 반환 |

---

## 테스트 ↔ 결함 매핑

| 실패 테스트 | 결함 ID |
|-------------|---------|
| `test_none_grid_returns_invalid_size_failure_result` | DEF-001 |
| `test_none_grid_resolve_called_zero_times_isolation` | DEF-002 |
| `test_none_grid_code_is_exactly_invalid_size_string` | DEF-003 |
| `test_none_grid_message_matches_prd_section_8_1_byte_for_byte` | DEF-004 |
| `test_empty_list_grid_returns_invalid_size_failure` | DEF-005 |
| `test_four_empty_rows_grid_returns_invalid_size_failure` | DEF-006 |
| `test_3x4_grid_returns_invalid_size_failure` | DEF-007 |

---

## 관찰 사항 (결함 외)

| ID | 유형 | 설명 | 조치 |
|----|------|------|------|
| OBS-001 | 계약 정합성 | `docs/PRD_MagicSquare.md`는 null 입력 시 `E_NULL_INPUT` / `입력 행렬이 null입니다.`를 정의함. RED 테스트·README To-Do는 `INVALID_SIZE` / `Grid must be 4x4.`를 사용함. | GREEN 전 PRD vs 테스트 계약 단일화 결정 필요 |
| OBS-002 | 커버리지 | RED 단계 `htmlcov` 기준 `solve_puzzle.py` 실행 분기 0% — 구현 후 Boundary 85%+ 재측정 | GREEN 완료 후 `pytest --cov=src/boundary --cov-report=html` |

---

## 수정 완료 기준 (Closure)

- [ ] DEF-001 ~ DEF-007 모두 **Closed**
- [ ] `pytest tests/boundary/test_fr01_01_invalid_size.py -v` → **8 passed**
- [ ] `resolve()` 미호출 격리 테스트 통과
- [ ] Boundary 커버리지 **≥ 85%** (`pytest --cov=src/boundary --cov-fail-under=85`)

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2026-05-29 | RED 실행 결과 기반 초기 결함 7건 등록 |
