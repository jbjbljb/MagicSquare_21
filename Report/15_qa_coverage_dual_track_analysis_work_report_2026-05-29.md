# 15 QA Coverage Dual-Track Analysis Work Report

- **작성일:** 2026-05-29
- **범위:** TDD Phase QA 커버리지 분석 (Ask mode) · Step 0 기준선 · Step 1 Dual-Track SSOT · production 코드 미변경
- **선행:** [Report/14](./14_refactor_three_category_complete_work_report_2026-05-29.md) REFACTOR 완료 (59 pytest · Boundary 99%)
- **현재 단계:** **QA 게이트 점검** · Domain Track NFR-01 미달 · Boundary·전역 PASS

---

## 1. Executive Summary

Report/14 이후 REFACTOR 완료 상태에서 **Dual-Track 커버리지 게이트**를 SSOT 명령으로 재측정했다. 기능 테스트는 전량 GREEN이나, **Domain Track 단독 측정 시 NFR-01(≥ 95%) 미충족**이 확인되었다.

| 항목 | 결과 | Gate |
|------|------|------|
| `pytest -q` | **59 passed** | GREEN |
| GM-1 (`test_golden_master_magic_square.py`) | **10 passed** | GREEN |
| `pytest.fail` 스켈레톤 | **0건** | REFACTOR RED gate ✅ |
| Domain Track (`entity` tests → `src/entity` + `src/control`) | **88%** (80 stmts, 10 miss) | NFR-01 **FAIL** |
| Boundary Track | **99%** (107 stmts, 1 miss) | NFR-02 **PASS** |
| Global `src/` | **97%** (187 stmts, 6 miss) | NFR-03 (≥ 80%) **PASS** |

---

## 2. Step 0 — 기준선

### 2.1 전체 스위트

```bash
python -m pytest -q
```

| 항목 | 값 |
|------|-----|
| passed | 59 |
| failed | 0 |
| error | 0 |

**모듈별 분해**

| 경로 | passed |
|------|--------|
| `tests/boundary/` | 37 |
| `tests/entity/` | 12 |
| `tests/test_golden_master_magic_square.py` | 10 |

### 2.2 GM-1 (Golden Master)

프롬프트 관례 파일 `tests/test_gm_01_magic_square_golden_master.py`는 저장소에 없음. 실제 SSOT:

```bash
python -m pytest tests/test_golden_master_magic_square.py -q
```

| 항목 | 결과 |
|------|------|
| GM-TC-01~05 (`solve_puzzle` 경로) | 5 passed |
| GM-TC-01~05 (`UIBoundary` parity) | 5 passed |
| **합계** | **10 passed** |

### 2.3 RED 스켈레톤 · REFACTOR gate

| 검사 | 결과 |
|------|------|
| `grep pytest.fail tests/` | **0건** |
| Report/09 Skeleton (26건) | Report/11·13에서 Full RED 전환 완료 |
| “19 RED” (프롬프트 선행 조건) | **해당 없음** — 현재 스켈레톤 0, 전 스위트 GREEN |

**판정:** RED/REFACTOR(skeleton) gate **충족**. 커버리지 Domain Track만 후속 작업 대상.

---

## 3. Step 1 — Dual-Track 커버리지 (SSOT)

### 3.1 Domain Track — NFR-01 (≥ 95%)

**프롬프트 명령:**

```bash
python -m pytest tests/entity/ tests/control/ \
  --cov=src/entity --cov=src/control \
  --cov-report=term-missing
```

| 항목 | 결과 |
|------|------|
| `tests/control/` | **디렉터리 없음** → exit 4 (cov 미산출) |
| **실측 대체** | `pytest tests/entity/ --cov=src/entity --cov=src/control` |

| 모듈 | Stmts | Miss | Cover | Missing |
|------|------:|-----:|------:|---------|
| `control/completion_resolver.py` | 5 | 5 | **0%** | 3–13 |
| `entity/services/magic_square_validator.py` | 23 | 4 | 83% | 20, 30, 32, 36 |
| `entity/services/empty_cell_locator.py` | 12 | 1 | 92% | 22 |
| `control/two_cell_solver.py` | 24 | 0 | 100% | — |
| 기타 entity/control | — | 0 | 100% | — |
| **TOTAL** | **80** | **10** | **88%** | |

**NFR-01:** **FAIL** (−7%p)

**미커버 원인**

1. **`completion_resolver.py` (0%)** — `tests/entity/`만 실행 시 `TwoCellCompletionResolver.resolve()` 미호출. Boundary/GM 경로에서만 실행.
2. **`magic_square_validator.py` 20, 30, 32, 36** — D-VAL-02~04가 행 합(26–27)에서 선행 return → 열·대각·길이 가드 미도달.
3. **`empty_cell_locator.py` 22** — `len(blanks) != 2` 시 `ValueError`. Entity 테스트는 G1(빈칸 2)만 사용.

### 3.2 Boundary Track — NFR-02 (≥ 85%)

```bash
python -m pytest tests/boundary/ \
  --cov=src/boundary \
  --cov-report=term-missing
```

| 모듈 | Cover | Missing |
|------|------:|---------|
| `input_validator.py` | 100% | — |
| `solve_puzzle.py` | 100% | — |
| `ui_boundary.py` | 100% | — |
| `contracts.py`, `schemas.py` | 100% | — |
| `ports.py` | 83% | 14 (Protocol `...` stub) |
| **TOTAL** | **99%** | 1 miss |

37 passed · **NFR-02 PASS**

### 3.3 Global gate — NFR-03 (≥ 80%, 프롬프트 SSOT)

```bash
python -m pytest --cov=src --cov-report=term-missing
```

| 항목 | 값 |
|------|-----|
| passed | 59 |
| **TOTAL `src/`** | **97%** (187 stmts, 6 miss) |

**NFR-03 (커버리지):** **PASS**

> `docs/test_plan.md`의 NFR-03은 **결정성(동일 입력 → 동일 결과)** 이다. 본 측정의 “전역 ≥ 80%”는 프롬프트 Step 1 SSOT 기준.

**전역 잔여 6 miss**

| 파일 | Missing |
|------|---------|
| `boundary/ports.py` | 14 |
| `entity/services/empty_cell_locator.py` | 22 |
| `entity/services/magic_square_validator.py` | 20, 30, 32, 36 |

---

## 4. ECB 경로 매핑 · Invariant 추적

| 프롬프트 관례 | 실제 경로 | 레이어 | Domain cov 관측 |
|---------------|-----------|--------|-----------------|
| domain.py | `src/control/solve_partial_magic_square.py` *(미존재)* → `two_cell_solver.py` | Control | solver 100% |
| Domain Logic | `src/entity/services/*.py` | Entity | validator/locator gap |
| boundary.py | `src/boundary/ui_boundary.py`, `input_validator.py`, `schemas.py` | Boundary | 99% |
| gui | `src/boundary/screen/` | Screen | **미구현** |

### Invariant I1~I11 (Report/08)

| Inv | Test ID | 기능 | 라인 cov |
|-----|---------|------|----------|
| I1 | D-VAL-01, 02 | PASS | 행 분기 커버 |
| I2 | D-VAL-01, 03 | PASS | 열 30 미실행 |
| I3 | D-VAL-01, 04 | PASS | 대각 32, 36 미실행 |
| I4 | D-VAL-05, 06 | PASS | — |
| I5 | D-VAL-01~04 | PASS | — |
| I6 | D-LOC-01 | PASS | locator 22 미실행 |
| I7/I11 | D-MIS-01 | PASS | — |
| I8~I10 | D-SOL-01~04 | PASS | — |
| U-IN/OUT/FLOW | boundary 37 | PASS | — |

**기능 추적성:** GREEN · **Domain Track 라인 gate:** 미달.

---

## 5. 게이트 요약

| Gate | 목표 | 측정 | 판정 |
|------|------|------|------|
| pytest 전체 | GREEN | 59/59 | **PASS** |
| GM-1 | GREEN | 10/10 | **PASS** |
| RED skeleton | 0× `pytest.fail` | 0 | **PASS** |
| NFR-01 Domain | ≥ 95% | 88% | **FAIL** |
| NFR-02 Boundary | ≥ 85% | 99% | **PASS** |
| NFR-03 Global cov | ≥ 80% | 97% | **PASS** |

---

## 6. 권장 후속 (테스트만 — production 미변경)

Domain Track NFR-01 충족을 위한 **최소 테스트 추가** 후보:

| # | 대상 | 목적 | 예상 커버 |
|---|------|------|-----------|
| 1 | `tests/control/test_completion_resolver.py` | `TwoCellCompletionResolver.resolve(G1)` | `completion_resolver` 0% → 100% |
| 2 | `test_d_val_*` 확장 | 3×4 격자, 열·대각만 깨는 fixture | validator 20, 30, 32, 36 |
| 3 | `test_d_loc_*` 확장 | 빈칸 1/3개 → `ValueError` | locator 22 |

**측정 SSOT (정정):**

```bash
python -m pytest tests/entity/ --cov=src/entity --cov=src/control --cov-report=term-missing
python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing
python -m pytest --cov=src --cov-report=term-missing
```

**운영 주의:** Windows에서 병렬 `--cov` 실행 시 `.coverage` PermissionError 가능 → 순차 실행.

---

## 7. 참조

| 문서 | 용도 |
|------|------|
| [docs/test_plan.md](../docs/test_plan.md) §6·§7·§8 | Domain spy · Pydantic · cov 목표 |
| [Report/02_DualTrack_CleanArchitecture_TDD_Design.md](./02_DualTrack_CleanArchitecture_TDD_Design.md) | I1~I11 · Dual-Track |
| [Report/14](./14_refactor_three_category_complete_work_report_2026-05-29.md) | REFACTOR 직전 baseline |
| [Prompt/15](../Prompt/15_export_transcript_qa_coverage_dual_track_analysis_2026-05-29.md) | 본 세션 Transcript |

---

## 8. 산출물

| 파일 | 설명 |
|------|------|
| `Report/15_qa_coverage_dual_track_analysis_work_report_2026-05-29.md` | 본 보고서 |
| `Prompt/15_export_transcript_qa_coverage_dual_track_analysis_2026-05-29.md` | 대화 Transcript |

**코드 변경:** 없음 (분석·문서화 only).
