# 13 REFACTOR 준비 — 코드 리뷰 · 테스트 매핑 · 스멜 분석 Work Report

- **작성일:** 2026-05-29
- **브랜치:** `refactor/refactor` (기준)
- **범위:** `src/boundary/*`, `src/control/*` · REFACTOR phase 준비 · code-reviewer 위임 리뷰 · 스멜 점검
- **현재 단계:** GREEN 완료 · Golden Master 구축 완료 · **REFACTOR 착수 전 분석**

---

## 1. Executive Summary

본 세션에서는 REFACTOR phase(`.cursor/rules/magicsquare-tdd-testing.mdc`) 착수 전에 **Boundary·Control 레이어**를 대상으로 (1) code-reviewer 서브에이전트 코드 리뷰, (2) 테스트–소스 매핑·RED/GREEN 잔여 점검, (3) REFACTOR 스멜 표 작성을 수행했다.

| 항목 | 결과 |
|------|------|
| code-reviewer 리뷰 | ECB 경계·GM 인프라 양호; Boundary–Control E2E·예외 매핑·시나리오 SSOT gap |
| pytest.fail 스켈레톤 | **0건** (Report/09 Skeleton → Report/11 Full RED 전환 완료) |
| REFACTOR 전 GREEN 잔여 | `solve_puzzle` NotImplementedError, Control 어댑터, Boundary E2E, `UnsolvableDomainError`→`FailureResult` |
| High 스멜 | 8건 (계약·레이어·SSOT) |
| Medium 스멜 | 9건 (DRY·가독성·결합) |
| 구현 변경 | **없음** (분석 세션) |

---

## 2. code-reviewer 리뷰 요약

### 2.1 잘된 점

- ECB: `boundary`→entity 직접 import 없음; `entity`→control/boundary 역의존 없음
- 금지 패턴: `src/`·테스트에 `print()` 디버그, bare `except` 없음
- Golden Master: approve 패턴, 섹션 diff, contract assertion 이중 방어
- `FailureResult` frozen Pydantic; solver가 grid 복사본만 수정

### 2.2 주요 Findings (우선순위)

| ID | 심각도 | 요약 |
|----|--------|------|
| H-1 | 높음 | `CompletionResolverPort` 어댑터 없음; `UnsolvableDomainError` Boundary 미매핑 |
| M-1 | 중간 | GM-TC-03/04 그리드가 `SCENARIOS`와 테스트 파일에 이중 정의 |
| M-2 | 중간 | Entity locator/finder가 2-blank 전제 미검증 → Boundary 우회 시 `IndexError` |
| M-3 | 중간 | `contracts.py` ↔ `entity/constants.py` 상수 이중 정의 |
| M-4 | 중간 | U-OUT-03 `n1<n2` vs D-SOL-02 reverse 정책 충돌 가능 |
| M-5 | 중간 | approve 시 baseline 전체 재쓰기 · xdist 경쟁 |
| M-7 | 중간 | GM이 `UIBoundary` 경로 미검증 |

---

## 3. REFACTOR phase 테스트 매핑 (`src/boundary/*`, `src/control/*`)

### 3.1 Boundary

| 소스 | 대응 테스트 | 상태 |
|------|-------------|------|
| `input_validator.py` | `test_u_in_04_to_08.py` (U-IN-03~08) | △ U-IN-01~02는 `test_fr01_01_invalid_size.py` |
| `solve_puzzle.py` | 간접 (`UIBoundary` 경유) | △ valid-path NotImplementedError |
| `ui_boundary.py` | `test_u_flow_02.py`, `test_u_out_01_to_03.py` | △ mock resolver만 |
| `contracts.py`, `schemas.py`, `ports.py` | 전용 없음 (간접) | △ SSOT·어댑터 테스트 부재 |

### 3.2 Control

| 소스 | 대응 테스트 | 상태 |
|------|-------------|------|
| `two_cell_solver.py` | `tests/entity/test_d_sol_01_to_04.py` | ✅ D-SOL-01~04 |
| `exceptions.py` | D-SOL-03, GM-TC-05 간접 | △ Boundary 매핑 테스트 없음 |

### 3.3 REFACTOR 전 GREEN 잔여

1. `TwoCellSolverAdapter` + `solve_puzzle` valid-path (NotImplementedError 제거)
2. `UIBoundary` + 실제 adapter E2E (G1/G3)
3. `UnsolvableDomainError` → `FailureResult` 고정 code
4. GM 시나리오 그리드 단일 출처화 (M-1)

### 3.4 REFACTOR 전제 (한 줄)

> REFACTOR는 전체 테스트 GREEN 상태에서만 구조를 바꾸므로, 테스트 없이 리팩터하면 계약(E002/E004/E005/int[6]) 회귀를 감지할 수 없다.

---

## 4. REFACTOR 스멜 분석 표

### 4.1 High

| 파일 | 줄 | 스멜 | 설명 |
|------|-----|------|------|
| `solve_puzzle.py` | 24–27 | 예외 제어 흐름 | `NotImplementedError("RED: …")` — 구현 부재 신호 |
| `solve_puzzle.py` | 21–28 | ECB 혼재 | Control 어댑터·예외 매핑 부재 |
| `contracts.py` | 3–21 | SSOT | entity/constants 이중 정의 |
| `contracts.py` | 6, 18 | 매직 문자열 | `"4x4"`, `"1~16"` 리터럴 |
| `input_validator.py` | 37–52 | 중복 | INVALID_SIZE FailureResult 3회 |
| `two_cell_solver.py` | 26 | 예외 (결합) | Boundary 미매핑 `UnsolvableDomainError` |
| `ports.py` | 6–10 | ECB 명명 | "Domain resolver" vs Control 어댑터 |
| `input_validator.py` | 53–80 | 결합 | entity 2-blank 전제와 Boundary 우회 경로 |

### 4.2 Medium / Low

- Medium 9건: `validate()` 45줄, 3회 grid 스캔, GREEN docstring, `_validator` 중복, int[6] 상수 부재, Attempt 대칭 등
- Low 4건: docstring `4x4` 리터럴, `__all__` 범위, `solver_port` 명명

### 4.3 스멜 없음

- `schemas.py`, `exceptions.py`, `control/__init__.py` — 전 항목 해당 없음

---

## 5. REFACTOR 권장 순서

1. 전체 pytest + `@pytest.mark.golden_master` GREEN 확인
2. `contracts` ↔ `entity/constants` SSOT (fr01 바이트 테스트 동시)
3. Control 어댑터 + `NotImplementedError` 제거
4. `UnsolvableDomainError` → Boundary `FailureResult`
5. `input_validator.validate()` 구조 분해 (계약 문자열 불변)
6. GM/`capture_scenario_output` → `UIBoundary` 경로 정렬 (선택)

---

## 6. 미수행 · 후속

| 항목 | 상태 |
|------|------|
| REFACTOR 코드 변경 | 미수행 |
| `docs/defect_list.md` DEF Closed | 미수행 |
| Boundary coverage 85% gate | 미수행 |
| REFACTOR 착수 | 본 Report 이후 진행 |

---

## 7. Traceability

| 산출물 | 경로 |
|--------|------|
| Transcript | [Prompt/13_export_transcript_refactor_readiness_2026-05-29.md](../Prompt/13_export_transcript_refactor_readiness_2026-05-29.md) |
| Golden Master Report | [Report/12_golden_master_work_report_2026-05-29.md](./12_golden_master_work_report_2026-05-29.md) |
| TDD REFACTOR 규칙 | `.cursor/rules/magicsquare-tdd-testing.mdc` |
| Approve 패턴 | `docs/golden_master_approve_pattern.md` |

*문서 버전 1.0 — REFACTOR 준비 분석 세션 종료 시점 기준*
