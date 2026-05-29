# MagicSquare 4x4 TDD Practice

## 1. Project Start Declaration

본 저장소는 **MagicSquare 4×4 TDD Practice** 프로젝트의 **시작을 선언**하는 문서입니다.

이 프로젝트는 4×4 격자에 빈칸 2개가 남은 퍼즐을 입력받아, 누락 숫자를 두 빈칸에 배치했을 때 **마방진(행·열·대각선 합 = 34)** 이 되는 해를 찾아 `[r1, c1, n1, r2, c2, n2]` 형식으로 반환하는 시스템을 **Dual-Track UI + Logic TDD**와 **ECB(Entity · Control · Boundary)** 아키텍처로 구현하기 위한 학습 프로젝트입니다.

**현재 단계는 PRD 기반 TDD 시작 준비 단계**입니다. 문제 정의, 설계, PRD, Cursor 규칙까지는 완료되었으며, **아직 구현 코드와 테스트 코드는 작성하지 않았습니다.**

**RED**는 “실패하는 테스트를 먼저 작성하고, `pytest` 실행으로 **테스트가 의도대로 실패하는 상태를 확인하는 단계**”입니다. RED는 구현이 아니라 **실패 확인**입니다.

**GREEN**은 RED에서 확인한 실패를 **통과시키기 위한 최소 구현 작업 후보**입니다. 본 README는 GREEN 구현을 수행하지 않습니다.

**REFACTOR**는 GREEN 이후 구조·가독성·중복 제거를 위한 **개선 후보**입니다. 본 README는 REFACTOR를 수행하지 않습니다.

이 README는 단순 소개가 아니라, **PRD 요약 → TDD 흐름 → Scenario 추적 보드 → RED 시작 체크리스트**를 통해 구현 전에 **개발 방향과 Concept-to-Code 추적 구조를 고정**하는 개발 가이드입니다.

---

## 2. PRD Summary

### 프로젝트 목적

4×4 마방진 문제를 “정답 계산기”가 아닌 **불변식 기반 사고 훈련 과제**로 정의합니다. 입력·출력 계약을 고정하고, Boundary 검증과 Domain 판정을 분리하며, Dual-Track TDD로 RED → GREEN → REFACTOR를 운영합니다.

### 학습 목표

- **규칙 명시화**: 모호한 요구를 검사 가능한 Acceptance Criteria로 분해
- **경계·상태 구분**: 입력 오류 / 도메인 실패 / 성공을 계약대로 구분
- **레이어 분리**: Boundary RED와 Logic RED를 독립적으로 추적
- **TDD 사이클**: Scenario → RED 실패 확인 → 최소 GREEN → REFACTOR 후보 식별
- **추적성**: Concept → Rule → Scenario → Test → Component 연결 유지

### 핵심 도메인 규칙

| ID | 규칙 |
|----|------|
| BR-01 | 입력은 **4×4** 정수 행렬 |
| BR-02 | 빈칸(`0`)은 **정확히 2개** |
| BR-03 | 셀 값은 **`0` 또는 `1~16`** |
| BR-04 | `0`을 제외한 값은 **중복 불가** |
| BR-05 | 첫 번째 빈칸 = **row-major** 스캔 최초 `0` |
| BR-06~07 | 누락 숫자 2개, 내부 표현 **오름차순** (`mSmall < mLarge`) |
| BR-08~09 | 마방진 상수 **34**, 행 4·열 4·대각 2 **합 = 34** |
| BR-10~11 | Attempt 1 = small-first, Attempt 2 = reverse |
| BR-12~13 | 출력 좌표 **1-index**, 형식 **`int[6]`** |

### 입력 계약

| 항목 | 규칙 | 실패 코드 예 |
|------|------|-------------|
| `matrix` | `null` 불가 | `E_NULL_INPUT` |
| shape | 4×4 | `E_DIM_ROWS`, `E_DIM_COLS` |
| cell value | `0` 또는 `1~16` | `E_CELL_RANGE` |
| blank count | `count(0) == 2` | `E_EMPTY_COUNT` |
| uniqueness | `0` 제외 중복 금지 | `E_DUPLICATE` |

### 출력 계약

| 항목 | 규칙 |
|------|------|
| 성공 형식 | `int[6] = [r1, c1, n1, r2, c2, n2]` |
| 좌표 | **1-index** (`1..4`) |
| Attempt 1 성공 | `[r1, c1, mSmall, r2, c2, mLarge]` |
| Attempt 2 성공 | `[r1, c1, mLarge, r2, c2, mSmall]` |
| 두 조합 실패 | `E_NO_SOLUTION` |

### 성공 기준

- Boundary 입력 검증 실패 시 **Domain resolver 미호출**
- 동일 입력 → **동일 성공 결과 또는 동일 오류 코드** (결정성)
- 10개 선(행 4·열 4·대각 2) **전수 검사** 후 valid 판정
- 테스트 기반 계약 준수: Domain Logic coverage **95%+**, Boundary Validation coverage **85%+**

---

## 3. TDD Development Flow

```
Scenario
  → Acceptance Criteria
  → RED Test ID
  → Test Skeleton
  → Run Test
  → Confirm Failure = RED
  → Minimal Implementation = GREEN
  → Structure Improvement = REFACTOR
```

| 단계 | 의미 |
|------|------|
| **Scenario** | 사용자·도메인 관점에서 검증할 상황을 한 문장으로 정의합니다. |
| **Acceptance Criteria** | Scenario를 **테스트 가능한 통과/거부 조건**으로 분해합니다. |
| **RED Test ID** | 각 AC에 고유 테스트 식별자를 부여해 추적성을 확보합니다. |
| **Test Skeleton** | AAA(Arrange-Act-Assert) 구조의 **테스트 함수 골격**을 작성합니다. 구현은 아직 없습니다. |
| **Run Test** | `pytest`로 테스트를 실행합니다. |
| **Confirm Failure = RED** | 테스트가 **의도한 이유로 실패**하는지 확인합니다. RED는 “실패 확인” 단계입니다. |
| **Minimal Implementation = GREEN** | RED 실패를 통과시키기 위한 **최소 구현 작업 후보**입니다. 본 단계에서만 코드를 작성합니다. |
| **Structure Improvement = REFACTOR** | GREEN 통과 후 중복 제거·네이밍·레이어 정리 등 **구조 개선 후보**입니다. 테스트는 Green을 유지해야 합니다. |

---

## 4. Development Methodology

### Dual-Track UI + Logic TDD

| Track | 범위 | RED 우선 대상 |
|-------|------|--------------|
| **Track A — Boundary / UI Contract** | 입력 검증, 출력 형식, 오류 코드, resolver 미호출 | `E_NULL_INPUT`, shape, range, duplicate, `int[6]` 길이, 1-index |
| **Track B — Domain / Logic** | 빈칸 탐색, 누락 수, 마방진 판정, 조합 시도 | row-major, 오름차순, 합 34, small-first / reverse, `E_NO_SOLUTION` |

Track A와 Track B의 RED는 **독립적으로** 작성하고, Domain 전체 선구현 후 Boundary를 붙이는 일괄 방식은 금지합니다.

### Boundary RED와 Logic RED의 분리

- **Boundary RED**: “입력이 계약을 위반하면 즉시 오류를 반환하고 Domain을 호출하지 않는다.”
- **Logic RED**: “검증 통과 입력에 대해 도메인 불변식(빈칸·누락 수·합 34·조합)을 만족하는 결과를 반환한다.”

### ECB 역할 분리

의존 방향: `Boundary → Control → Entity`

- **Entity**: Board 상태와 순수 도메인 규칙
- **Control**: 검증 통과 후 해 결정 흐름 조정
- **Boundary**: 입력 검증, 출력 형식, 오류 정책 (Domain Invariant 직접 구현 금지)

### Concept-to-Code Traceability

```
Concept → Business Rule → Scenario → Acceptance Criteria
  → RED Test ID → Test Skeleton → Component → ECB Layer
```

### RED → GREEN → REFACTOR 원칙

| 단계 | 허용 | 금지 |
|------|------|------|
| RED | 실패 테스트 작성·실패 확인 | 구현 코드 작성 |
| GREEN | RED 통과를 위한 최소 구현 | 테스트 삭제·약화 |
| REFACTOR | 구조 개선 (Green 유지) | 계약 변경, magic number 도입 |

---

## 5. ECB Role Separation

| ECB Layer | Responsibility | Example Component |
|-----------|----------------|-------------------|
| **Entity** | 4×4 Board 상태, Cell/Grid 값 객체, 마방진 상수(34), 순수 도메인 불변식 표현. UI·DB·Web·파일 시스템에 의존하지 않음 | `Grid`, `Cell`, `MagicConstant`, `Line` |
| **Control** | Boundary 검증 통과 후 BlankFinder → MissingNumberFinder → Validator → Solver 호출 순서 조정, 실패 코드 매핑 일관성 유지 | `SolvePuzzleUseCase`, `Solver` |
| **Boundary** | `int[][]` 입력 계약 검증, 표준 오류 응답 생성, 성공 `int[6]` 출력 형식·좌표 범위 검증. **Domain Invariant를 직접 구현하지 않음** | `BoundaryValidator`, `ResultFormatter`, CLI/API 어댑터 |

**경계 규칙**

- Boundary는 Domain Invariant(합 34, 누락 수 계산 등)를 **직접 구현하지 않습니다**.
- Domain(Entity/Control 내부 순수 로직)은 UI, DB, Web, 파일 시스템에 **의존하지 않습니다**.
- Boundary → Entity 직접 import **금지** (Control 경유).

---

## 6. Scenario → AC → RED → GREEN Tracking Board

| Status | Scenario ID | Scenario Summary | Acceptance Criteria | RED Test ID | Test Skeleton Candidate | Expected RED Failure | GREEN Task Candidate | REFACTOR Candidate | ECB Layer | Code Target |
|--------|-------------|------------------|---------------------|-------------|-------------------------|----------------------|----------------------|--------------------|-----------|-------------|
| RED 준비 | SC-BND-001 | None 입력 | AC: `null` 입력 시 `E_NULL_INPUT` 반환, Domain resolver 미호출 | RED-BND-001 | `test_boundary_rejects_null_input()` | `ModuleNotFoundError` 또는 `AttributeError` (BoundaryValidator 미구현) | `BoundaryValidator.validate()`에 null 검사 및 `E_NULL_INPUT` 반환 최소 구현 | 오류 코드 enum `ErrorCode` 분리 | Boundary | `src/boundary/boundary_validator.py` |
| RED 준비 | SC-BND-002 | 4×4가 아닌 입력 | AC: 행≠4 → `E_DIM_ROWS`, 열≠4 → `E_DIM_COLS`, resolver 미호출 | RED-BND-002 | `test_boundary_rejects_non_4x4_matrix()` | shape 검사 미구현으로 테스트 실패 | 4×4 shape 검증 로직 최소 구현 | shape 검증을 `MatrixShape` VO로 추출 | Boundary | `src/boundary/boundary_validator.py` |
| RED 준비 | SC-BND-003 | 빈칸 개수 오류 | AC: `count(0) != 2` → `E_EMPTY_COUNT`, resolver 미호출 | RED-BND-003 | `test_boundary_rejects_invalid_blank_count()` | 빈칸 수 검사 미구현 | `count(0)==2` 검증 최소 구현 | 빈칸 카운트 헬퍼 함수 분리 | Boundary | `src/boundary/boundary_validator.py` |
| RED 준비 | SC-BND-004 | 값 범위 오류 | AC: `0` 외 `1~16` 밖 값 → `E_CELL_RANGE` | RED-BND-004 | `test_boundary_rejects_out_of_range_cell()` | 범위 검사 미구현 | 셀 값 `0 or 1..16` 검증 최소 구현 | `CellValue` VO로 범위 캡슐화 | Boundary | `src/boundary/boundary_validator.py` |
| RED 준비 | SC-BND-005 | 중복 숫자 오류 | AC: `0` 제외 중복 → `E_DUPLICATE` | RED-BND-005 | `test_boundary_rejects_duplicate_non_zero()` | 중복 검사 미구현 | non-zero 중복 set 검증 최소 구현 | 중복 검사를 `DuplicateChecker`로 분리 | Boundary | `src/boundary/boundary_validator.py` |
| RED 준비 | SC-DOM-001 | 빈칸 좌표 row-major 탐색 | AC: 첫·둘째 빈칸이 row-major 스캔 순서와 일치 | RED-DOM-001 | `test_blank_finder_returns_row_major_order()` | `BlankFinder` 미구현 | row-major 스캔으로 `(r1,c1),(r2,c2)` 반환 최소 구현 | `EmptyCellLocator` 네이밍·인덱스 정책 통일 | Entity | `src/entity/blank_finder.py` |
| RED 준비 | SC-DOM-002 | 누락 숫자 오름차순 탐색 | AC: `{1..16} \ non-zero`에서 2개, `mSmall < mLarge` | RED-DOM-002 | `test_missing_number_finder_returns_ascending_pair()` | `MissingNumberFinder` 미구현 | 누락 2개 식별 및 오름차순 정렬 최소 구현 | `MissingNumberResolver`로 rename·인터페이스 정리 | Entity | `src/entity/missing_number_finder.py` |
| RED 준비 | SC-DOM-003 | 모든 행 합 34 검증 | AC: 완성 격자 4개 행 각각 합 = 34 | RED-DOM-003 | `test_validator_all_rows_sum_to_34()` | `MagicSquareValidator` 미구현 | 행 4개 합 검사 최소 구현 | `LineSumCalculator` 공통화 | Entity | `src/entity/magic_square_validator.py` |
| RED 준비 | SC-DOM-004 | 모든 열 합 34 검증 | AC: 완성 격자 4개 열 각각 합 = 34 | RED-DOM-004 | `test_validator_all_columns_sum_to_34()` | 열 합 검사 미구현 | 열 4개 합 검사 최소 구현 | 행·열 검사 루프 통합 | Entity | `src/entity/magic_square_validator.py` |
| RED 준비 | SC-DOM-005 | 두 대각선 합 34 검증 | AC: 주대각·부대각 합 각각 = 34 | RED-DOM-005 | `test_validator_both_diagonals_sum_to_34()` | 대각선 검사 미구현 | D1·D2 대각선 합 검사 최소 구현 | 10개 선 집합 `Line` VO로 표현 | Entity | `src/entity/magic_square_validator.py` |
| RED 준비 | SC-DOM-006 | small-first 성공 | AC: Attempt 1 (small→first, large→second) 성공 시 해당 순서 `[r1,c1,n1,r2,c2,n2]` 반환 | RED-DOM-006 | `test_solver_small_first_succeeds_immediately()` | `Solver` 미구현 | Attempt 1 배치·검증·성공 반환 최소 구현 | Attempt 실행을 `CompletionSolver`로 분리 | Control | `src/control/solver.py` |
| RED 준비 | SC-DOM-007 | small-first 실패 후 reverse 성공 | AC: Attempt 1 실패, Attempt 2 성공 시 reverse 순서 반환 | RED-DOM-007 | `test_solver_reverse_succeeds_after_small_first_fails()` | reverse 시도 로직 미구현 | Attempt 2 reverse 배치·반환 최소 구현 | 시도 순서를 Strategy 패턴 후보로 문서화 | Control | `src/control/solver.py` |
| RED 준비 | SC-DOM-008 | 두 조합 모두 실패 | AC: Attempt 1·2 모두 비마방진 → `E_NO_SOLUTION` | RED-DOM-008 | `test_solver_returns_no_solution_when_both_attempts_fail()` | 실패 정책 미구현 | 두 시도 실패 시 `E_NO_SOLUTION` 매핑 최소 구현 | Domain `NO_VALID_COMPLETION` → Boundary `E_NO_SOLUTION` 매퍼 분리 | Control + Boundary | `src/control/solver.py`, `src/boundary/result_formatter.py` |
| RED 준비 | SC-BND-006 | 결과 배열 길이 6 | AC: 성공 반환 `int[6]` 길이 고정 | RED-BND-006 | `test_result_formatter_returns_length_six_array()` | `ResultFormatter` 미구현 | 성공 결과 6원소 배열 조립 최소 구현 | 출력 DTO `SolveResult` 도입 후보 | Boundary | `src/boundary/result_formatter.py` |
| RED 준비 | SC-BND-007 | 반환 좌표 1-index | AC: `r1,c1,r2,c2` ∈ `1..4` | RED-BND-007 | `test_result_formatter_uses_one_based_coordinates()` | 1-index 변환 미구현 | 내부 0-index → 외부 1-index 변환 최소 구현 | `Cell` VO가 1-index 단일 출처 역할 수행 | Boundary | `src/boundary/result_formatter.py` |

---

## 7. RED Start Checklist

- [ ] 모든 Scenario가 정의되었는가?
- [ ] 모든 Acceptance Criteria가 테스트 가능한 문장인가?
- [ ] 모든 Scenario에 RED Test ID가 부여되었는가?
- [ ] 모든 RED Test ID에 Test Skeleton 후보가 있는가?
- [ ] 각 RED 항목에 Expected RED Failure가 명시되었는가?
- [ ] 각 RED 실패에 대응하는 GREEN Task 후보가 있는가?
- [ ] Boundary RED와 Logic RED가 분리되었는가?
- [ ] ECB Layer가 명확히 지정되었는가?
- [ ] 아직 구현 코드를 작성하지 않았는가?
- [ ] 아직 테스트 코드를 작성하지 않았는가?
- [ ] 아직 REFACTOR를 수행하지 않았는가?

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 [docs/test_plan.md](docs/test_plan.md) 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] [docs/defect_list.md](docs/defect_list.md) 생성 및 발견 결함 기록
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## GREEN 단계 To-Do 리스트

> 기준 브랜치: `stabilize/green` · Track A Full RED + Dual-Track Skeleton  
> 원칙: **한 GREEN 커밋 = 해당 테스트만 통과하는 최소 구현** (REFACTOR·AC 확장 금지)

### RED 단계 커밋 묶음 (참고)

- [ ] **RED-C-01** — 프로젝트 뼈대
  - [ ] `pyproject.toml`
  - [ ] `src/boundary/contracts.py`, `schemas.py`, `ports.py`
  - [ ] `src/boundary/solve_puzzle.py` (RED stub)
- [ ] **RED-C-02** — Track A Full RED
  - [ ] `tests/boundary/test_fr01_01_invalid_size.py` (8건)
- [ ] **RED-C-03** — Track A Skeleton
  - [ ] `tests/boundary/test_u_in_04_to_08.py`
  - [ ] `tests/boundary/test_u_out_01_to_03.py`
  - [ ] `tests/boundary/test_u_flow_02.py`
- [ ] **RED-C-04** — Track B Skeleton
  - [ ] `tests/entity/test_d_loc_01.py`, `test_d_mis_01.py`
  - [ ] `tests/entity/test_d_val_01_to_06.py`, `test_d_sol_01_to_04.py`
- [ ] **RED-C-05** — Fixture placeholder
  - [ ] `tests/conftest.py` (G0~G3 주석)
  - [ ] `tests/entity/conftest.py` (placeholder)

### Track A — Boundary GREEN

#### G-C-01 · null 입력 (G-001~004) — 4건

- [x] `test_none_grid_returns_invalid_size_failure_result`
- [x] `test_none_grid_code_is_exactly_invalid_size_string`
- [x] `test_none_grid_message_matches_prd_section_8_1_byte_for_byte`
- [x] `test_none_grid_resolve_called_zero_times_isolation`
- [x] **구현:** `grid is None` → `FailureResult(INVALID_SIZE)` + `resolve()` 0회
- [x] **검증:** 위 4건 `pytest -v` 통과 확인

#### G-C-02 · shape 위반 (G-005~007) — 3건

- [x] `test_empty_list_grid_returns_invalid_size_failure` (`grid=[]`)
- [x] `test_four_empty_rows_grid_returns_invalid_size_failure` (`grid=[[]]*4`)
- [x] `test_3x4_grid_returns_invalid_size_failure` (3×4)
- [x] **구현:** `len(grid) != 4` 또는 `len(row) != 4` → `INVALID_SIZE`
- [x] **금지:** empty count / range / duplicate 분기 선행 구현
- [x] **검증:** 위 3건 + G-C-01 회귀 4건 통과

#### G-C-03 · empty count (U-IN-03~04) — 2건

> 선행: Skeleton → Full RED 전환 (`pytest.fail` → assert)

- [x] U-IN-03 — 빈칸 0개 (G0) → `E002`
- [x] U-IN-04 — `test_u_in_04_three_blanks_returns_e002` (빈칸 3개)
- [x] **구현:** `count(0) != 2` 검증
- [x] **검증:** U-IN-03~04 + G-C-01~02 회귀

#### G-C-04 · cell range (U-IN-05, 05b) — 2건

- [x] U-IN-05 — `test_u_in_05_cell_value_17_returns_e004` (값 17)
- [x] U-IN-05b — `test_u_in_05b_negative_cell_returns_e004` (값 -1)
- [x] **구현:** `0` 외 `1~16` 밖 값 → `E004`
- [x] **검증:** U-IN-05~05b + 이전 GREEN 회귀

#### G-C-05 · duplicate (U-IN-06) — 1건

- [ ] U-IN-06 — `test_u_in_06_duplicate_non_zero_returns_e005`
- [ ] **구현:** non-zero 중복 → `E005`
- [ ] **검증:** U-IN-06 + 이전 GREEN 회귀

#### G-C-06 · empty count 확장 + short-circuit (U-IN-07, 08) — 2건

- [ ] U-IN-07 — `test_u_in_07_one_blank_returns_e002` (빈칸 1개)
- [ ] U-IN-08 — `test_u_in_08_empty_count_short_circuits_before_range`
- [ ] **구현:** 1 blank → `E002` / empty count가 range보다 선행
- [ ] **검증:** U-IN-07~08 + 이전 GREEN 회귀

#### G-C-07 · Domain 격리 (U-FLOW-02) — 5건

- [ ] `test_u_flow_02_null_matrix_execute_never_called`
- [ ] `test_u_flow_02_three_blanks_execute_never_called`
- [ ] `test_u_flow_02_out_of_range_execute_never_called`
- [ ] `test_u_flow_02_duplicate_execute_never_called`
- [ ] `test_u_flow_02_one_blank_execute_never_called`
- [ ] **구현:** invalid 입력 시 `execute.call_count == 0`
- [ ] **검증:** U-FLOW-02 5건 + Track A Boundary 전체 회귀

#### G-C-08 · 성공 envelope (U-OUT-01~03) — 3건

> 선행: Track B D-SOL-01 (G1 Step A)

- [ ] U-OUT-01 — `test_u_out_01_success_result_length_six`
- [ ] U-OUT-02 — `test_u_out_02_success_coordinates_one_indexed`
- [ ] U-OUT-03 — `test_u_out_03_success_missing_numbers_ascending_in_tuple`
- [ ] **구현:** 성공 시 `int[6]`, 좌표 1-index, `n1 < n2`
- [ ] **검증:** U-OUT 3건 + Track A 전체 회귀

### Track B — Domain / Logic GREEN

> 선행: G0~G3 fixture 주석 해제 · Skeleton Full RED 전환

#### G-C-B1 · D-LOC-01 — 1건

- [ ] `test_d_loc_01_find_blank_coords_row_major_on_g1`
- [ ] **구현:** G1 빈칸 `(2,2)`, `(3,3)` row-major (1-index)
- [ ] **대상:** `entity/services/empty_cell_locator.py`

#### G-C-B2 · D-MIS-01 — 1건

- [ ] `test_d_mis_01_find_not_exist_nums_ascending_on_g1`
- [ ] **구현:** G1 누락 수 `{7, 10}` 오름차순
- [ ] **대상:** `entity/services/missing_number_finder.py`

#### G-C-B3 · D-VAL-01~06 — 6건

- [ ] D-VAL-01 — G0 complete → `True`
- [ ] D-VAL-02 — row sum mismatch → `False`
- [ ] D-VAL-03 — column sum mismatch → `False`
- [ ] D-VAL-04 — diagonal sum mismatch → `False`
- [ ] D-VAL-05 — duplicate → `False`
- [ ] D-VAL-06 — contains 0 → `False`
- [ ] **구현:** `is_magic_square()` 최소 분기
- [ ] **대상:** `entity/services/magic_square_validator.py`

#### G-C-B4 · D-SOL-01, D-SOL-04 — 2건

- [ ] D-SOL-01 — G1 Step A → `[2,2,7,3,3,10]`
- [ ] D-SOL-04 — `int[6]` 길이 · 1-index 좌표 정책
- [ ] **대상:** `control/two_cell_solver.py`

#### G-C-B5 · D-SOL-02 — 1건

- [ ] D-SOL-02 — G2 Step B → `[2,3,10,4,1,4]`
- [ ] **선행:** G2 fixture 확정

#### G-C-B6 · D-SOL-03 — 1건

- [ ] D-SOL-03 — G3 both fail → `UnsolvableDomainError`
- [ ] **선행:** G3 placeholder 격자 확정

### 마일스톤 (Track A Full RED 완료 기준)

- [ ] `test_fr01_01_invalid_size.py` → **8 passed** (G-C-01 + G-C-02)
- [ ] [docs/defect_list.md](docs/defect_list.md) DEF-001~007 **Closed**
- [ ] Boundary `--cov-fail-under=85` 통과

### GREEN 진행 요약

| GREEN 커밋 | 테스트 수 | 상태 |
|-----------|----------|------|
| G-C-01 | 4 | ✅ 진행됨 |
| G-C-02 | 3 | ⬜ 다음 |
| G-C-03 | 2 | ⬜ |
| G-C-04 | 2 | ⬜ |
| G-C-05 | 1 | ⬜ |
| G-C-06 | 2 | ⬜ |
| G-C-07 | 5 | ⬜ |
| G-C-B1~B6 | 12 | ⬜ |
| G-C-08 | 3 | ⬜ |

**다음 작업:** **G-C-02** — `test_empty_list_*`, `test_four_empty_rows_*`, `test_3x4_*` (3건)

---

## 8. Quality Gates

| 항목 | 기준 |
|------|------|
| Domain Logic coverage | **95%+** |
| Boundary Validation coverage | **85%+** |
| 테스트 프레임워크 | **pytest** |
| 테스트 구조 | **AAA pattern** (Arrange · Act · Assert) |
| 테스트 약화 | **금지** (삭제·skip·assertion 완화로 Green 만들기 불가) |
| 디버깅 | **`print()` 금지** → `logging` 사용 |
| 상수 | 설명 없는 **magic number 금지** → `MagicConstant(34)` 등 명명 상수 |
| 타입 | **type hints 필수** |
| 스타일 | **PEP8** 준수 |
| 계약 | **입력/출력 계약 변경 금지** (변경 시 PRD·README·테스트 동시 갱신) |

**실행 도구 (예정)**

- `pyproject.toml`: pytest, coverage, 프로젝트 메타데이터 설정 예정
- `src/`: ECB 레이어 소스
- `tests/`: RED Test ID와 1:1 대응 테스트 모듈

---

## 9. Reference Documents

| 문서 | 역할 |
|------|------|
| [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) | 프로젝트 목적, FR/BR, 입·출력 계약, 오류 정책, Dual-Track TDD 전략의 **1차 기준(PRD)** |
| [docs/test_plan.md](docs/test_plan.md) | Track A/B 테스트 계획, AC·시나리오·커버리지·pytest 전략 |
| [docs/defect_list.md](docs/defect_list.md) | RED 단계 결함 목록 (DEF-xxx, Closure 기준) |
| [Report/01_Problem_Definition_Report.md](Report/01_Problem_Definition_Report.md) | STEP 1~5 문제 정의, Why Chain, Invariant, “검증·설명” 문제로의 재정의 |
| [Report/02_DualTrack_CleanArchitecture_TDD_Design.md](Report/02_DualTrack_CleanArchitecture_TDD_Design.md) | 입·출력 계약, Domain Invariant, Layer Boundary, Dual-Track TDD 설계 |
| [Report/03_CursorRules_Work_Report.md](Report/03_CursorRules_Work_Report.md) | 개발 환경, ECB, TDD, pytest, 품질·금지 패턴, `.cursorrules` 작성 이력 |
| [Report/06_scenario_verification_summary_2026-05-28.md](Report/06_scenario_verification_summary_2026-05-28.md) | Epic → Journey → Story → Scenario 정합성 검증, 누락 시나리오 보강 권고 |
| [.cursorrules](.cursorrules) | AI·개발자 공통 프로젝트 규칙 (Python, ECB, TDD, forbidden 패턴) |
| [.cursor/rules/*.mdc](.cursor/rules/) | 관심사별 Cursor 규칙 (project, ECB, TDD, code style, forbidden) |

**문서 간 관계**

```
01 Problem Definition  →  02 Design  →  PRD  →  06 Scenario Verification
                              ↓
                         03 Cursor Rules  →  .cursorrules / .cursor/rules/
                              ↓
                         README (본 문서): TDD 시작 선언 + 추적 보드
```

> 참고: 프롬프트에서 언급된 `docs/5.PRD_MagicSquare_4x4_TDD.md`, `Report/4.UserJourney_...` 등의 파일명은 본 저장소에서는 위 실제 경로로 대응됩니다. User Journey·Epic·Story 상세는 PRD §8과 Report/06을 함께 참조하세요.

---

## 10. Current Project Status

| 항목 | 상태 |
|------|------|
| **현재 단계** | PRD 기반 TDD 시작 준비 |
| **문제 정의 · 설계 · PRD · Cursor Rules** | ✅ 완료 |
| **구현 코드 (`src/`)** | ⏳ 미착수 |
| **테스트 코드 (`tests/`)** | ⏳ 미착수 |
| **`pyproject.toml`** | ⏳ 미생성 |
| **다음 단계** | Test Skeleton 작성 → `pytest` 실행 → **RED 실패 확인** |

---

## 저장소 구조 (목표)

```
MagicSquare_21/
├── README.md                 ← 본 문서 (TDD 시작 가이드)
├── docs/
│   ├── PRD_MagicSquare.md    ← PRD 1차 기준
│   ├── test_plan.md          ← 테스트 계획
│   └── defect_list.md        ← 결함 목록
├── Report/                   ← 문제 정의 · 설계 · 검증 보고서
├── Prompt/                   ← Cursor 프롬프트 이력
├── .cursorrules              ← 프로젝트 규칙
├── .cursor/rules/            ← 관심사별 MDC 규칙
├── pyproject.toml            ← (예정) pytest / coverage 설정
├── src/
│   ├── entity/               ← Grid, Validator, Finder
│   ├── control/              ← Solver, UseCase
│   └── boundary/             ← Validator, Formatter
└── tests/                    ← RED Test ID 대응 테스트
```

---

*최종 업데이트: 2026-05-29 — PRD 기반 TDD 시작 준비 (구현·테스트 코드 미착수)*
