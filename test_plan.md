# MagicSquare — Test Plan (Track A / FR-01)

| 항목 | 내용 |
|------|------|
| **문서 ID** | TP-MAGICSQUARE-FR01-BND-001 |
| **버전** | 1.0 |
| **작성 관점** | 시니어 QA 리드 |
| **기준 시나리오** | **SC-BND-001** — None(null) 입력 거부 |
| **기준 AC** | **AC-FR01-01**, **AC-FR01-06** (연계) |
| **PRD 참조** | `docs/PRD_MagicSquare.md` — FR-01 (§10), Input Contract (§12), Error Policy (§13) |
| **기술 스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **아키텍처** | ECB — Boundary → Control → Entity(Domain) |

---

## 1. 목적 및 범위

### 1.1 목적

본 테스트 계획은 **SC-BND-001**을 앵커로, FR-01 Boundary 입력 검증의 **RED → GREEN** 사이클을 pytest로 운영하기 위한 단위 테스트 범위·우선순위·검증 전략을 정의한다.

핵심 검증 목표:

1. **AC-FR01-01**: `matrix is None` → 표준 오류 `{ code: E_NULL_INPUT, message: 고정 문구 }`
2. **AC-FR01-06**: FR-01 검증 실패 시 **Domain 해 결정 진입점 0회 호출**
3. FR-01 검증 **순서 고정** 준수 (null → shape → range → blank count → duplicate)

### 1.2 In-Scope

| 구분 | 내용 |
|------|------|
| 레이어 | Boundary (`BoundaryValidator`, Boundary Port `solvePuzzle`) |
| Track | **Track A** — Boundary / UI Contract TDD |
| 컴포넌트 | `src/boundary/boundary_validator.py`, Boundary 진입 어댑터(예: `solve_puzzle`) |
| 테스트 유형 | 단위 테스트 (pytest), Mock/Spy 기반 격리 검증 |

### 1.3 Out-of-Scope (본 계획서 명시 제외)

| 제외 항목 | 사유 |
|-----------|------|
| **4×4 정상 입력** (빈칸 2개, 값·중복 유효) | AC-FR01-01 범위 외; Domain/통합 시나리오(SC-DOM-*, SC-BND-006/007)로 분리 |
| Domain 불변식(합 34, Solver 시도 순서) | Track B — 별도 `test_plan_domain.md` 후보 |
| UI 화면, DB, Web/API | PRD §9.2 Out-of-Scope |
| 성능(50ms) 벤치마크 | NFR-05 — 별도 성능 테스트 계획 |

---

## 2. 추적성 (Traceability)

| Concept | Business Rule | FR | AC | Scenario | RED Test ID | Test Module (예정) |
|---------|---------------|----|----|----------|-------------|-------------------|
| null 입력 거부 | BR-01 선행 | FR-01 | AC-FR01-01, AC-FR01-06 | SC-BND-001 | RED-BND-001 | `tests/boundary/test_null_input.py` |
| 4×4 shape | BR-01 | FR-01 | AC-FR01-02, AC-FR01-06 | SC-BND-002 | RED-BND-002 | `tests/boundary/test_matrix_shape.py` |

**검증 순서 (고정)** — `Report/02_DualTrack_CleanArchitecture_TDD_Design.md` §2.2:

1. `matrix is None` → `E_NULL_INPUT`
2. `len(matrix) != 4` → `E_DIM_ROWS`
3. any `len(row) != 4` → `E_DIM_COLS`
4. 이하 range / empty count / duplicate (본 계획의 2차 우선순위)

---

## 3. pytest 단위 테스트 범위 및 우선순위

### 3.1 테스트 피라미드 (본 스프린트)

```
        [ Integration — 후속 IT-001~ ]
       /   Control + Boundary + Mock Domain  \
      /----------------------------------------\
     |  Boundary Unit (본 계획 핵심)            |
     |  BoundaryValidator + solvePuzzle Port  |
      \----------------------------------------/
```

### 3.2 우선순위 매트릭스

| Priority | ID | 대상 | AC | 설명 | 선행 조건 |
|----------|-----|------|-----|------|-----------|
| **P0** | UT-BND-001 | `BoundaryValidator.validate(None)` | AC-FR01-01 | null → `E_NULL_INPUT`, 예외 미발생 | 없음 |
| **P0** | UT-BND-002 | `solvePuzzle(None)` + Mock Domain | AC-FR01-01, AC-FR01-06 | Port 경유 시 동일 오류 + **resolver.call_count == 0** | UT-BND-001 GREEN |
| **P1** | UT-BND-003 | `validate([])` | AC-FR01-02 | 빈 리스트 → `E_DIM_ROWS` | P0 통과 |
| **P1** | UT-BND-004 | `validate([[]]*4)` | AC-FR01-02 | 4행·0열 → `E_DIM_COLS` | P0 통과 |
| **P1** | UT-BND-005~007 | 3×4, 4×3, 5×5 | AC-FR01-02 | shape 불일치 코드 분기 | P0 통과 |
| **P2** | UT-BND-008 | 결정성 | NFR-03 | 동일 None 입력 2회 → 동일 code/message | P0 통과 |
| **P2** | UT-BND-009 | Pydantic 스키마 | §12 Error schema | `code`/`message` 필드·타입 계약 | P0 통과 |

### 3.3 테스트 모듈 구조 (예정)

```
tests/
├── conftest.py                 # fixtures, ErrorResponse 검증 헬퍼
├── boundary/
│   ├── test_null_input.py      # P0: SC-BND-001
│   └── test_matrix_shape.py    # P1: shape 경계값
└── helpers/
    └── assert_error.py         # AAA Assert 공통화
```

### 3.4 AAA 패턴 및 네이밍

- **Arrange**: 입력 `matrix`, Mock Domain resolver 주입
- **Act**: `validate(matrix)` 또는 `solve_puzzle(matrix)`
- **Assert**: `ErrorResponse` code/message; `mock_resolver.assert_not_called()` 또는 `call_count == 0`

네이밍 규칙: `test_<layer>_<behavior>_<condition>()`

예: `test_boundary_rejects_null_input_with_e_null_input()`

---

## 4. 경계값 케이스 목록

검증 순서에 따라 **선행 규칙이 실패하면 후속 규칙은 실행되지 않아야 함**을 전제로 기대 오류 코드를 정의한다.

### 4.1 P0 — SC-BND-001 (AC-FR01-01) 핵심

| Case ID | 입력 (`matrix` / `grid`) | 기대 `code` | 기대 `message` (바이트 동일) | AC | Domain 호출 |
|---------|--------------------------|-------------|------------------------------|-----|---------------|
| **BV-001** | `None` (명시적 None) | `E_NULL_INPUT` | `입력 행렬이 null입니다.` | AC-FR01-01 | **0** |

> Python 표기: `grid = None`. Java/PRD 표기: `matrix == null`.

### 4.2 P1 — Shape 경계값 (AC-FR01-02, AC-FR01-06)

| Case ID | 입력 | 기대 `code` | 비고 | Domain 호출 |
|---------|------|-------------|------|---------------|
| **BV-002** | `[]` (빈 리스트) | `E_DIM_ROWS` | `len(matrix)==0` → 행 개수 위반 | **0** |
| **BV-003** | `[[]] * 4` (행 4, 열 0) | `E_DIM_COLS` | 행 수 통과 후 열 검사에서 실패 | **0** |
| **BV-004** | 3×4 행렬 (예: RD-03 유형) | `E_DIM_ROWS` | `len(matrix)==3` | **0** |
| **BV-005** | 4×3 행렬 (한 행이라도 길이 3) | `E_DIM_COLS` | 행 수 4, 열 불일치 | **0** |
| **BV-006** | 5×5 행렬 | `E_DIM_ROWS` | `len(matrix)==5` | **0** |

**3×4 / 4×3 / 5×5 최소 픽스처 예시** (값은 shape만 검증하므로 더미 허용):

```python
# BV-004: 3×4
grid_3x4 = [[0]*4 for _ in range(3)]

# BV-005: 4×3
grid_4x3 = [[0]*3 for _ in range(4)]

# BV-006: 5×5
grid_5x5 = [[0]*5 for _ in range(5)]
```

### 4.3 명시적 제외 (본 계획서에 테스트 케이스로 추가하지 않음)

| 제외 입력 | 제외 사유 |
|-----------|-----------|
| **4×4 정상 입력** (빈칸 2개, 1..16 유효, 중복 없음) | AC-FR01-01 범위 외; 검증 **통과** 후 Domain 호출 시나리오 — Track B / SC-DOM-* / IT 계획으로 이관 |
| RD-01, RD-02 (small-first / reverse 성공) | FR-05 정상 경로 |
| RD-04~RD-06 (빈칸·범위·중복) | AC-FR01-03~05 — **별도 스프린트** (SC-BND-003~005) |

---

## 5. 예외 / 특이 케이스 목록

| Case ID | 유형 | 조건 | 기대 동작 | AC / NFR |
|---------|------|------|-----------|----------|
| **EX-001** | 정책 준수 | Boundary 검증 실패 | **예외 throw 금지** — `Error(code, message)` 반환 | FR-01 Error Policy |
| **EX-002** | 타입 혼동 | `matrix=""` / `matrix=0` | 구현 전: **결정 필요** — `E_NULL_INPUT` vs `E_INTERNAL` vs 입력 타입 가드 | Decision Needed (구현 시 명세 고정) |
| **EX-003** | Python alias | `[[]] * 4` — 동일 빈 리스트 참조 4개 | shape 검증만 목적; **셀 변경 부작용 테스트는 NFR-04** 별도 | BV-003 |
| **EX-004** | 이중 호출 | `solve_puzzle(None)` 연속 2회 | 동일 `E_NULL_INPUT`, resolver **각 0회** | NFR-03 |
| **EX-005** | Mock 누수 | 첫 테스트 후 mock 미 reset | `autouse` fixture로 **mock reset** 필수 | 테스트 신뢰성 |
| **EX-006** | 부분 구현 | shape만 구현, null 미구현 | RED-BND-001 **실패** 유지 (테스트 삭제/약화 금지) | Rule-P5 |
| **EX-007** | Control 경유 | `SolvePuzzleUseCase.execute(None)` | Boundary 검증 실패 시 Entity/Domain **직접 import 없이** 0 호출 | ECB §17 |

---

## 6. Domain 해 결정 진입점 호출 횟수 검증 전략

### 6.1 “Domain 해 결정 진입점” 정의

본 프로젝트에서 Boundary가 호출하는 **Domain/Application 해 결정 진입점**은 다음 중 **구현 시 단일 Port로 고정**한다 (테스트는 그 Port를 Mock).

| 후보 Port | 역할 | Mock 대상 |
|-----------|------|-----------|
| `CompletionSolver.solve(matrix)` | 2-blank 완성 시도 | **Primary spy target** |
| `SolvePuzzleUseCase.execute(matrix)` | Control 오케스트레이션 | Integration 시 |

**AC-FR01-06 판정 기준**: FR-01 검증 실패 시 위 Port의 **`call_count == 0`**, `assert_not_called()`.

### 6.2 Mock / Spy 패턴 (unittest.mock)

#### 패턴 A — BoundaryValidator 단독 (P0-α)

`BoundaryValidator`는 Domain을 호출하지 않는 **순수 검증 함수**로 유지할 경우:

- **검증**: `validate(None)` 반환값만 assert
- **Domain 호출 테스트**: Port 테스트(패턴 B)에서 수행

#### 패턴 B — solvePuzzle + Mock Domain (P0-β, **권장**)

```python
from unittest.mock import MagicMock, create_autospec

# Arrange
mock_solver = create_autospec(CompletionSolverPort, instance=True)
boundary = SolvePuzzleBoundary(validator=BoundaryValidator(), solver=mock_solver)

# Act
result = boundary.solve_puzzle(None)

# Assert — AC-FR01-01
assert result.code == "E_NULL_INPUT"
assert result.message == "입력 행렬이 null입니다."

# Assert — AC-FR01-06
mock_solver.solve.assert_not_called()
assert mock_solver.solve.call_count == 0
```

#### 패턴 C — pytest `mocker` fixture (pytest-mock, 선택)

```python
def test_solve_puzzle_null_never_calls_domain(mocker):
    mock_solver = mocker.patch("src.boundary.solve_puzzle_boundary._solver")
    ...
    mock_solver.solve.assert_not_called()
```

### 6.3 Spy 체크리스트 (케이스별)

| Case ID | Act | Assert (Domain) |
|---------|-----|-----------------|
| BV-001 | `solve_puzzle(None)` | `solve.call_count == 0` |
| BV-002~006 | `solve_puzzle(invalid_shape)` | `solve.call_count == 0` |
| EX-004 | `solve_puzzle(None)` × 2 | 누적 `call_count == 0` |

### 6.4 금지 사항

- Domain Mock을 **patch 경로 오류**로 우회 통과시키지 않는다.
- 검증 실패 시 `pytest.raises(Exception)`으로 통과시키지 않는다 (계약 위반).
- Green 달성을 위해 `call_count` assertion을 삭제·주석 처리하지 않는다.

---

## 7. 테스트 데이터 및 Pydantic 계약 검증

### 7.1 Error Response 스키마 (pydantic)

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    code: str
    message: str
```

테스트에서 `ErrorResponse.model_validate(result)`로 **필드 누락·타입 오류**를 조기 탐지한다.

### 7.2 허용 code 열거 (본 계획 범위)

`E_NULL_INPUT`, `E_DIM_ROWS`, `E_DIM_COLS`

---

## 8. 커버리지 목표

| 레이어 | 목표 | PRD | 측정 대상 (예정) |
|--------|------|-----|------------------|
| **Domain (Entity/Control logic)** | **≥ 95%** | NFR-01 | `src/entity/`, `src/control/` |
| **Boundary Validation** | **≥ 85%** | NFR-02 | `src/boundary/boundary_validator.py` 등 |

### 8.1 본 스프린트(SC-BND-001) 최소 Boundary 목표

| 파일 | 라인 목표 | 비고 |
|------|-----------|------|
| `boundary_validator.py` | null 분기 **100%** | P0 완료 기준 |
| `solve_puzzle_boundary.py` (예정) | 실패 경로 **≥ 85%** | Mock 테스트 포함 |

> Domain 95%는 **Track B 구현 후** 전체 스위트에서 달성한다. 본 계획 단계에서는 Domain 코드가 없거나 Mock만 존재할 수 있으며, **미구현 시 Domain cov는 N/A**로 보고한다.

---

## 9. pytest-cov 측정 전략

### 9.1 설치

```bash
pip install pytest pytest-cov pytest-mock pydantic
```

### 9.2 실행 (전체)

```bash
pytest --cov=src --cov-report=term-missing
```

### 9.3 실행 (Boundary만 — SC-BND-001 스프린트)

```bash
pytest tests/boundary/ \
  --cov=src/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 9.4 실행 (P0 null만)

```bash
pytest tests/boundary/test_null_input.py -v \
  --cov=src/boundary/boundary_validator \
  --cov-report=term-missing
```

### 9.5 CI / 로컬 게이트 (권장)

| 게이트 | 명령 | 실패 조건 |
|--------|------|-----------|
| PR — Boundary | `pytest tests/boundary/ --cov=src/boundary --cov-fail-under=85` | Boundary < 85% |
| Main — Full | `pytest --cov=src --cov-report=xml` | Domain < 95% (Track B 완료 후) |

### 9.6 커버리지 해석 규칙

- **미구현 모듈**: RED 단계에서는 `ModuleNotFoundError`가 정상; cov 0%는 **구현 전 상태**로 기록만 한다.
- **Mock으로만 통과한 라인**: Boundary Port의 “실패 시 early return” 분기는 **반드시 term-missing으로 미커버 분기 확인**.
- **제외**: `if TYPE_CHECKING:`, `pragma: no cover` — 리뷰 시 justification 필수.

### 9.7 pyproject.toml 설정 (예정 스니펫)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 85
show_missing = true
```

---

## 10. RED / GREEN / REFACTOR 운영

| 단계 | 활동 | 완료 기준 |
|------|------|-----------|
| **RED** | `test_boundary_rejects_null_input` 작성 후 pytest 실행 | `ModuleNotFoundError` / AssertionError — **의도된 실패** |
| **GREEN** | `BoundaryValidator`에 null 검사 + `E_NULL_INPUT` 최소 구현 | BV-001, UT-BND-001~002 통과 |
| **REFACTOR** | `ErrorCode` enum, Pydantic `ErrorResponse` 분리 | 전체 boundary 테스트 녹색 유지 |

**Expected RED Failure (SC-BND-001)**: `BoundaryValidator` 미구현 → `ModuleNotFoundError` 또는 `AttributeError`.

---

## 11. 테스트 케이스 요약表

| ID | Priority | 입력 | 기대 code | Domain calls | RED ID |
|----|----------|------|-----------|--------------|--------|
| BV-001 | P0 | `None` | `E_NULL_INPUT` | 0 | RED-BND-001 |
| BV-002 | P1 | `[]` | `E_DIM_ROWS` | 0 | RED-BND-002 |
| BV-003 | P1 | `[[]]*4` | `E_DIM_COLS` | 0 | RED-BND-002 |
| BV-004 | P1 | 3×4 | `E_DIM_ROWS` | 0 | RED-BND-002 |
| BV-005 | P1 | 4×3 | `E_DIM_COLS` | 0 | RED-BND-002 |
| BV-006 | P1 | 5×5 | `E_DIM_ROWS` | 0 | RED-BND-002 |
| *(제외)* | — | 4×4 정상 | — | N/A | SC-DOM-* |

---

## 12. 승인 및 변경 이력

| 버전 | 일자 | 변경 내용 | 작성 |
|------|------|-----------|------|
| 1.0 | 2026-05-29 | SC-BND-001 기반 FR-01 Boundary 테스트 계획 초안 | QA Lead |

---

## 부록 A — 참조 문서

- `docs/PRD_MagicSquare.md`
- `README.md` §6 Scenario → AC → RED Tracking Board
- `Report/02_DualTrack_CleanArchitecture_TDD_Design.md` §2.2, §2.3 (UT-002~008, Mock 전제)

## 부록 B — SC-BND-001 Gherkin (요약)

```gherkin
Feature: Boundary null input rejection
  Scenario: SC-BND-001 None input
    Given the puzzle matrix is null
    When the client calls solve_puzzle
    Then the response code is E_NULL_INPUT
    And the message is "입력 행렬이 null입니다."
    And the domain completion solver is not invoked
```
