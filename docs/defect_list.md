# MagicSquare — Defect List (RED Phase)

| 항목 | 내용 |
|------|------|
| **문서 ID** | DL-MAGICSQUARE-RED-001 |
| **작성일** | 2026-05-29 |
| **기준 테스트** | `tests/boundary/test_fr01_01_invalid_size.py` |
| **실행 명령** | `pytest tests/boundary/test_fr01_01_invalid_size.py -v` |
| **최종 실행 결과** | **8 passed** |
| **관련 AC** | AC-FR-01-01 (PRD §8.1 `INVALID_SIZE` 계약) |
| **상태** | **Closed** — GREEN·REFACTOR 완료 (2026-05-29) |

---

## 결함 요약

| Severity | 건수 | Closed |
|----------|------|--------|
| Critical | 2 | 2 |
| High | 5 | 5 |
| **합계** | **7** | **7** |

**공통 근본 원인 (해결됨):** `src/boundary/solve_puzzle.py`의 `solve_puzzle()`이 Boundary 입력 검증 및 `FailureResult` 반환을 구현하지 않고 `NotImplementedError`만 발생시키던 문제 → `InputValidator` + `FailureResult` + Control adapter로 해소.

---

## 결함 목록

| ID | Severity | AC ID | 상태 | 수정 요약 |
|----|----------|-------|------|-----------|
| DEF-001 | Critical | AC-FR-01-01 | **Closed** | `grid is None` → `FailureResult(INVALID_SIZE)` |
| DEF-002 | Critical | AC-FR-01-01 | **Closed** | null/shape 실패 시 `resolver.resolve()` 0회 |
| DEF-003 | High | AC-FR-01-01 | **Closed** | `result.code == INVALID_SIZE_CODE` |
| DEF-004 | High | AC-FR-01-01 | **Closed** | `message=INVALID_SIZE_MESSAGE` (PRD §8.1 byte match) |
| DEF-005 | High | AC-FR-01-01 | **Closed** | `grid=[]` → INVALID_SIZE |
| DEF-006 | High | AC-FR-01-01 | **Closed** | `grid=[[]]*4` → INVALID_SIZE |
| DEF-007 | High | AC-FR-01-01 | **Closed** | 3×4 grid → INVALID_SIZE |

---

## 테스트 ↔ 결함 매핑

| 통과 테스트 | 결함 ID | 상태 |
|-------------|---------|------|
| `test_none_grid_returns_invalid_size_failure_result` | DEF-001 | Closed |
| `test_none_grid_resolve_called_zero_times_isolation` | DEF-002 | Closed |
| `test_none_grid_code_is_exactly_invalid_size_string` | DEF-003 | Closed |
| `test_none_grid_message_matches_prd_section_8_1_byte_for_byte` | DEF-004 | Closed |
| `test_empty_list_grid_returns_invalid_size_failure` | DEF-005 | Closed |
| `test_four_empty_rows_grid_returns_invalid_size_failure` | DEF-006 | Closed |
| `test_3x4_grid_returns_invalid_size_failure` | DEF-007 | Closed |

---

## 관찰 사항 (결함 외)

| ID | 유형 | 설명 | 조치 |
|----|------|------|------|
| OBS-001 | 계약 정합성 | PRD null → `E_NULL_INPUT` vs 테스트 `INVALID_SIZE` | GREEN에서 `INVALID_SIZE` 계약으로 통일·테스트 통과 |
| OBS-002 | 커버리지 | Boundary REFACTOR 후 `pytest --cov=src/boundary --cov-fail-under=85` **99%** | RF-3-07 Closed |

---

## 수정 완료 기준 (Closure)

- [x] DEF-001 ~ DEF-007 모두 **Closed**
- [x] `pytest tests/boundary/test_fr01_01_invalid_size.py -v` → **8 passed**
- [x] `resolve()` 미호출 격리 테스트 통과
- [x] Boundary 커버리지 **≥ 85%** (`pytest --cov=src/boundary --cov-fail-under=85`)

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2026-05-29 | RED 실행 결과 기반 초기 결함 7건 등록 |
| 1.1 | 2026-05-29 | GREEN·REFACTOR 완료 — DEF-001~007 Closed, Boundary coverage 99% |
