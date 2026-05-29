# 09 Dual-Track RED Skeleton Work Report

- **작성일:** 2026-05-29
- **범위:** Report/08 설계표 기반 Dual-Track RED **Skeleton** pytest (Track A/B)
- **현재 단계:** RED Skeleton 작성 완료 / GREEN·REFACTOR 미착수

---

## 1. Executive Summary

본 세션에서는 [Report/08](./08_dual_track_red_design_report_2026-05-29.md) Dual-Track RED 설계표 중 **pytest가 없던 항목**에 대해 **RED Skeleton** 테스트만 작성했다. 각 테스트 본문은 `pytest.fail("RED: …")` 한 줄이며, 기대값 `assert`·`skip`·`xfail`은 사용하지 않았다. `src/` 운영 코드는 추가·수정하지 않았다.

| 항목 | 결과 |
|------|------|
| 신규 스켈레톤 | **26건** (`pytest.fail` 본문) |
| 신규 테스트 모듈 | **10개** (boundary 3 + entity 5 + conftest 2) |
| 기존 RED 유지 | `tests/boundary/test_fr01_01_invalid_size.py` **미수정** (8건) |
| `src/` 변경 | **없음** |
| pytest (`tests/boundary/` + `tests/entity/`) | **7 errors**, **7 failed**, **1 passed** |
| GREEN / REFACTOR | **미착수** |

---

## 2. 요청 및 수행 결과

### A. RED Skeleton 요청 (Dual-Track)

**사용자 요청 요약:**

- TDD phase: **RED (Skeleton)** — 구조·`pytest.fail`만
- SSOT: `test_plan.md`, `docs/PRD_MagicSquare.md`, Report/, `.cursorrules`
- 금지: `src/` 구현, GREEN/REFACTOR, assert 기대값, Report/08 기존 Full RED 수정
- 범위: U-IN-04~08, U-OUT-01~03, U-FLOW-02(확장), D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04
- 중복 금지: U-IN-01~03 (Report/08 `test_ac_fr_01_01_*` 대응)

**수행:**

- Track A·B 스켈레톤 모듈 분리 작성
- G0~G3 fixture는 `tests/conftest.py`·`tests/entity/conftest.py`에 **주석·placeholder**만
- production import 허용 (`boundary.*`, `entity.*`, `control.*`) — 미구현 시 collection ERROR를 RED로 인정

### B. 산출물 구조

| 경로 | Test ID | 건수 |
|------|---------|------|
| `tests/boundary/test_u_in_04_to_08.py` | U-IN-04~08, U-IN-05b | 6 |
| `tests/boundary/test_u_out_01_to_03.py` | U-OUT-01~03 | 3 |
| `tests/boundary/test_u_flow_02.py` | U-FLOW-02 (확장) | 5 |
| `tests/entity/test_d_loc_01.py` | D-LOC-01 | 1 |
| `tests/entity/test_d_mis_01.py` | D-MIS-01 | 1 |
| `tests/entity/test_d_val_01_to_06.py` | D-VAL-01~06 | 6 |
| `tests/entity/test_d_sol_01_to_04.py` | D-SOL-01~04 | 4 |
| `tests/conftest.py` | G0~G3 placeholder | — |
| `tests/entity/conftest.py` | entity fixture placeholder | — |

---

## 3. RED Skeleton 규칙 준수

| 규칙 | 준수 |
|------|------|
| 본문 `pytest.fail("RED: <Test ID> — …")` only | ✅ |
| Given/When/Then·Arrange/Act는 주석만 | ✅ |
| Then assert 없음 | ✅ |
| Track B Domain Mock 없음 | ✅ |
| U-OUT/U-FLOW Control mock 주석 표시 | ✅ |
| D-SOL-02 G2 TBD 메시지 | ✅ (`pytest.fail("RED: D-SOL-02 — G2 TBD")`) |
| `src/` 미작성 | ✅ |

---

## 4. pytest 실행 결과

```text
python -m pytest tests/boundary/ tests/entity/ -v --continue-on-collection-errors
======================== 7 failed, 1 passed, 7 errors ========================
```

### 4.1 신규 스켈레톤 (7 modules)

| 결과 | 원인 |
|------|------|
| **ERROR (collection)** ×7 | `ModuleNotFoundError`: `boundary`, `entity`, `control` 패키지·모듈 미구현 |

| 모듈 | import 대상 (예) |
|------|------------------|
| `test_u_in_04_to_08.py` | `boundary.input_validator.InputValidator` |
| `test_u_out_01_to_03.py` | `boundary.ui_boundary.UIBoundary` |
| `test_u_flow_02.py` | `boundary.ui_boundary.UIBoundary` |
| `test_d_loc_01.py` | `entity.services.empty_cell_locator.find_blank_coords` |
| `test_d_mis_01.py` | `entity.services.missing_number_finder.find_not_exist_nums` |
| `test_d_val_01_to_06.py` | `entity.services.magic_square_validator.is_magic_square` |
| `test_d_sol_01_to_04.py` | `control.two_cell_solver.solution` |

→ GREEN에서 `src/boundary/`, `src/entity/`, `src/control/` 최소 모듈 추가 시 **ERROR → FAILED (`pytest.fail`)** 로 전환 예상.

### 4.2 기존 RED (Report/07, 미수정)

| 결과 | 테스트 수 | 공통 실패 원인 |
|------|-----------|----------------|
| FAILED | 7 | `solve_puzzle` → `NotImplementedError` |
| PASSED | 1 | `test_scope_contract_is_invalid_size_not_other_ac_codes` |

---

## 5. Test ID ↔ Report / SSOT 매핑

| Test ID | SSOT | 스켈레톤 함수 |
|---------|------|---------------|
| U-IN-04 | Report/08 §3.1 | `test_u_in_04_three_blanks_returns_e002` |
| U-IN-05 | Report/08 §3.1 | `test_u_in_05_cell_value_17_returns_e004` |
| U-IN-05b | Prompt/08 | `test_u_in_05b_negative_cell_returns_e004` |
| U-IN-06 | Report/08 §3.1 | `test_u_in_06_duplicate_non_zero_returns_e005` |
| U-IN-07 | PRD RD-04, Report/02 UT-006 | `test_u_in_07_one_blank_returns_e002` |
| U-IN-08 | 세션 검증 순서 (empty→range) | `test_u_in_08_empty_count_short_circuits_before_range` |
| U-OUT-01 | Report/08 §3.2 | `test_u_out_01_success_result_length_six` |
| U-OUT-02 | Report/08 §3.2 | `test_u_out_02_success_coordinates_one_indexed` |
| U-OUT-03 | Report/02 OUT-03 | `test_u_out_03_success_missing_numbers_ascending_in_tuple` |
| U-FLOW-02 | Report/08 §3.3 | `test_u_flow_02_*_execute_never_called` (5건) |
| D-LOC-01 | Report/08 §4.2 | `test_d_loc_01_find_blank_coords_row_major_on_g1` |
| D-MIS-01 | Report/08 §4.2 | `test_d_mis_01_find_not_exist_nums_ascending_on_g1` |
| D-VAL-01~06 | Report/08 §4.2 | `test_d_val_01` … `test_d_val_06` |
| D-SOL-01 | Report/08, G1 | `test_d_sol_01_step_a_success_on_g1` |
| D-SOL-02 | Report/08, G2 | `test_d_sol_02_step_b_success_on_g2` |
| D-SOL-03 | Report/08, G3 placeholder | `test_d_sol_03_both_steps_fail_on_g3` |
| D-SOL-04 | Report/08 §4.2 | `test_d_sol_04_result_shape_and_one_index_policy_on_g1` |

**미작성 (의도):** U-IN-01~03 — Report/08 Full RED (`test_ac_fr_01_01_*`) 및 Report/07 `test_fr01_01_invalid_size.py`와 중복 방지.

---

## 6. 고정 픽스처 (G0~G3, 주석)

| ID | 용도 | 스켈레톤 상태 |
|----|------|---------------|
| G0 | 완전 마방진 · D-VAL-01 | `tests/conftest.py` 주석 |
| G1 | 빈칸 (2,2),(3,3) · D-LOC/MIS/SOL-01 | 주석 |
| G2 | Step B 성공 · D-SOL-02 | 주석 + **TBD** |
| G3 | 해 없음 · D-SOL-03 | placeholder 주석 |

---

## 7. 관찰 사항 및 리스크

| ID | 항목 | 설명 | 권고 |
|----|------|------|------|
| OBS-004 | import 경로 | 스켈레톤: `boundary.*` / 기존 RED: `src.boundary.*` | GREEN 시 `pythonpath` 또는 패키지 레이아웃 단일화 |
| OBS-005 | Report/08 vs 07 계약 | E003/E001 vs `INVALID_SIZE` | GREEN 전 오류 코드 SSOT 확정 |
| RISK-005 | collection ERROR | 신규 26건이 수집 전 중단 | `src` 최소 스텁 또는 `--continue-on-collection-errors`로 회귀 감시 |
| RISK-006 | G2/G3 | D-SOL-02/03 fixture 미확정 | GREEN 전 `is_magic_square`로 G2·G3 검증 |

---

## 8. 후속 작업 (Skeleton → GREEN 체크리스트)

1. `src/boundary/input_validator.py`, `ui_boundary.py` 최소 스텁 → U-IN/U-OUT/U-FLOW collection 해소
2. `src/entity/services/` — locator, finder, validator 최소 구현 → D-LOC/D-MIS/D-VAL
3. `src/control/two_cell_solver.py` — D-SOL-01 우선 (G1)
4. G2 격자 확정 후 D-SOL-02 스켈레톤 메시지·fixture 교체
5. G3 placeholder 확정 후 D-SOL-03
6. 스켈레톤 `pytest.fail` → 실제 assert로 단계적 치환 (Test ID별 GREEN)
7. U-IN-01~03: Report/08 Full RED와 계약 통합 여부 결정

---

## 9. 산출물 목록

| 유형 | 파일 |
|------|------|
| 테스트 (Skeleton) | `tests/boundary/test_u_*.py`, `tests/entity/test_d_*.py`, `tests/conftest.py` |
| 보고 | `Report/09_dual_track_red_skeleton_work_report_2026-05-29.md` (본 문서) |
| Transcript | `Prompt/09_export_transcript_dual_track_red_skeleton_2026-05-29.md` |

**본 세션에서 생성·수정하지 않은 항목:** `src/` 신규 모듈, `test_fr01_01_invalid_size.py`, GREEN 구현

---

## 10. 참조 문서

- [Report/08_dual_track_red_design_report_2026-05-29.md](./08_dual_track_red_design_report_2026-05-29.md)
- [Report/07_red_phase_tdd_work_report_2026-05-29.md](./07_red_phase_tdd_work_report_2026-05-29.md)
- [docs/PRD_MagicSquare.md](../docs/PRD_MagicSquare.md)
- [test_plan.md](../test_plan.md)
- [.cursorrules](../.cursorrules)
- [Prompt/09_export_transcript_dual_track_red_skeleton_2026-05-29.md](../Prompt/09_export_transcript_dual_track_red_skeleton_2026-05-29.md)

---

*문서 버전 1.0 — Dual-Track RED Skeleton 세션 종료 시점 기준*
