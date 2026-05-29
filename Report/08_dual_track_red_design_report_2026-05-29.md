# 08 Dual-Track RED Design Report (FR-01~FR-05)

- **작성일:** 2026-05-29
- **범위:** Track A (Boundary/UI Contract) + Track B (Domain/Logic) RED 설계표
- **현재 단계:** RED 설계 완료 / 테스트·구현 코드 미작성 (설계 산출물만)

---

## 1. Executive Summary

본 세션에서는 MagicSquare 4×4 프로젝트의 **Dual-Track TDD RED 단계**를 FR-01~FR-05 전체 범위로 확장하여, **구현·테스트 코드 없이** RED 테스트 설계표만 작성했다.

| 항목 | 결과 |
|------|------|
| Track A (Boundary) | U-IN-01~06, U-OUT-01~02, U-FLOW-02 — **11건** (+ U-IN-05b 보조) |
| Track B (Domain/Logic) | D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04 — **13건** |
| 코드 작성 | **없음** (금지 준수) |
| pytest 실행 | **없음** |
| GREEN / REFACTOR | **미착수** |

---

## 2. 요청 및 수행 결과

### A. RED 설계 요청 (Dual-Track 전체)

**사용자 요청 요약:**

- TDD phase: **RED** — 설계표 텍스트만 출력
- 금지: 구현·테스트·스켈레톤·pytest·파일 저장(설계 단계), GREEN/REFACTOR
- SSOT: `docs/PRD_MagicSquare.md` v0.2, `Report/02` (동등: `02_DualTrack_CleanArchitecture_TDD_Design.md`), `.cursorrules`
- 프로젝트 계약: E003/E001/E002/E004/E005, `int[6]` 1-index, M=34, 검증 순서 short-circuit, invalid 시 `execute` 0회

**수행:**

- **# UI RED Tests** 표 (입력 U-IN-*, 출력 U-OUT-*, 흐름 U-FLOW-02)
- **# Logic RED Tests** 표 (D-LOC/MIS/VAL/SOL-*)
- RED 설계 자체 검수 체크리스트 6항목
- Invariant I1~I11 ↔ Test ID 매핑

### B. SSOT 정합 처리

| 항목 | 처리 |
|------|------|
| `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` | 저장소에 없음 → `Report/02_DualTrack_CleanArchitecture_TDD_Design.md`로 대체 참조 |
| PRD 오류 코드 (`E_NULL_INPUT`, `E_DIM_*` 등) | 세션 **프로젝트 계약** E003/E001/E002/E004/E005 우선 적용 |
| G0~G3 부록 | Report/02에 없음 → **고정 픽스처 + G3 placeholder** 명시 |

---

## 3. Track A — Boundary RED 설계 요약

### 3.1 입력 검증 (U-IN-*, Domain 0회)

| Test ID | 조건 | 기대 code |
|---------|------|-----------|
| U-IN-01 | `matrix=null` | E003 |
| U-IN-02 | size ≠ 4×4 (3×4, 4×3, 5×5, `[]`) | E001 |
| U-IN-03 | 빈칸 0개 (G0) | E002 |
| U-IN-04 | 빈칸 3개 | E002 |
| U-IN-05 / 05b | 값 17 / -1 | E004 |
| U-IN-06 | non-zero 중복 | E005 |

**검증 순서 (고정):** null → size → empty count → value range → duplicate

**Failure envelope:** Python 예외 throw 금지; `{code, message}` 반환.

### 3.2 출력 계약 (U-OUT-*)

| Test ID | 내용 | Given |
|---------|------|-------|
| U-OUT-01 | 성공 배열 길이 6 | G1 + Mock `execute` → `[2,2,7,3,3,10]` |
| U-OUT-02 | 좌표 1-index `r,c ∈ [1,4]` | 동일 |

### 3.3 흐름 격리 (U-FLOW-02)

- invalid 입력 시 `SolvePartialMagicSquare.execute` **call_count == 0**
- AC-FR01-06 / U-FLOW-02 대응

---

## 4. Track B — Domain/Logic RED 설계 요약

### 4.1 고정 격자 픽스처 (G0~G3)

| ID | 격자 (요약) | 용도 |
|----|-------------|------|
| G0 | 완전 유효 4×4 마방진 (0 없음) | `is_magic_square` → true |
| G1 | 빈칸 (2,2),(3,3); 누락 {7,10} | D-LOC-01, D-MIS-01, D-SOL-01 |
| G2 | PRD RD-02 유형 | Step A 실패 · Step B 성공 → `[2,3,10,4,1,4]` |
| G3 | **placeholder** | Step A·B 모두 실패 → `UnsolvableDomainError` |

### 4.2 Logic Test ID 맵

| Test ID | 별칭(설계용) | Layer | 핵심 Then |
|---------|--------------|-------|-----------|
| D-LOC-01 | `find_blank_coords` / EmptyCellLocator | Entity | (2,2), (3,3) row-major |
| D-MIS-01 | `find_not_exist_nums` / MissingNumberFinder | Entity | {7, 10} 오름차순 |
| D-VAL-01~06 | `is_magic_square` / MagicSquareValidator | Entity | G0 true; 행/열/대각/집합/0 포함 false |
| D-SOL-01~04 | `solution` / TwoCellSolver | Control | G1/G2/G3 + int[6]·1-index |

**Domain Mock:** Track B 전 항목 **금지**.

---

## 5. Invariant 추적성

| Invariant | Test ID |
|-----------|---------|
| I1 행 합 | D-VAL-01, D-VAL-02 |
| I2 열 합 | D-VAL-01, D-VAL-03 |
| I3 대각 | D-VAL-01, D-VAL-04 |
| I4 값 집합·0 금지 | D-VAL-05, D-VAL-06 |
| I5 M=34 | D-VAL-01~04 |
| I6 빈칸 좌표 | D-LOC-01 |
| I7 / I11 누락 수 | D-MIS-01 |
| I8 Step A | D-SOL-01, D-SOL-04 |
| I9 Step B | D-SOL-02, D-SOL-04 |
| I10 해 없음 | D-SOL-03 |

---

## 6. RED 설계 자체 검수

| # | 항목 | 결과 |
|---|------|------|
| 1 | Boundary E00x Failure schema (generic Exception 아님) | ✅ |
| 2 | invalid → execute 0회 (U-FLOW-02) | ✅ |
| 3 | U-IN vs U-OUT 분리 | ✅ |
| 4 | Logic Track Domain Mock 없음 | ✅ |
| 5 | I1~I11 · AC-FR* 추적 가능 | ✅ |
| 6 | 코드/스켈레톤/구현 미작성 | ✅ |

---

## 7. 관찰 사항 및 리스크

| ID | 항목 | 설명 | 권고 |
|----|------|------|------|
| OBS-002 | PRD vs 세션 계약 | PRD: `E_NULL_INPUT` / 세션: `E003` | GREEN 전 오류 코드 단일 SSOT 확정 |
| OBS-003 | G3 placeholder | Step A·B 실패 격자 미검증 | GREEN 전 `is_magic_square`로 G3 확정 |
| RISK-003 | 기존 RED 테스트 | `test_fr01_01_invalid_size.py`는 `INVALID_SIZE` 계약 | 본 설계표(E003/E001…) 반영 시 테스트·계약 동시 갱신 |
| RISK-004 | 검증 순서 | Report/02는 range→empty 순; 세션은 empty→range | 구현 시 **세션 계약** 또는 PRD/Report 중 하나로 고정 |

---

## 8. 후속 작업 (RED → GREEN 체크리스트)

1. Track A: `U-IN-01`부터 pytest RED 테스트 파일 분리 작성 (`tests/boundary/`)
2. Track A: `U-FLOW-02` spy 테스트 — `solve_puzzle` + `CompletionResolverPort`
3. Track B: Entity RED — `D-LOC-01`, `D-MIS-01`, `D-VAL-01` 우선 (Report/02 RED 순서 정렬)
4. Track B: Control RED — `D-SOL-01` (G1) → `D-SOL-02` (G2) → `D-SOL-03` (G3 확정 후)
5. G3 격자 수동 검증 후 placeholder 교체
6. 오류 코드 E003/E001… vs PRD `E_NULL_INPUT` 통합 결정
7. 설계표 기준 커버리지: Domain 95%+ / Boundary 85%+

---

## 9. 산출물 목록

| 유형 | 파일 |
|------|------|
| RED 설계 (대화 산출) | 본 세션 Assistant 응답 (UI/Logic 표) |
| 보고 | `Report/08_dual_track_red_design_report_2026-05-29.md` (본 문서) |
| Transcript | `Prompt/08_export_transcript_dual_track_red_design_2026-05-29.md` |

**본 세션에서 생성·수정하지 않은 항목:** `tests/`, `src/`, `test_plan.md`, `defect_list.md`

---

## 10. 참조 문서

- [docs/PRD_MagicSquare.md](../docs/PRD_MagicSquare.md)
- [Report/02_DualTrack_CleanArchitecture_TDD_Design.md](./02_DualTrack_CleanArchitecture_TDD_Design.md)
- [Report/07_red_phase_tdd_work_report_2026-05-29.md](./07_red_phase_tdd_work_report_2026-05-29.md)
- [.cursorrules](../.cursorrules)
- [Prompt/08_export_transcript_dual_track_red_design_2026-05-29.md](../Prompt/08_export_transcript_dual_track_red_design_2026-05-29.md)

---

*문서 버전 1.0 — Dual-Track RED 설계 세션 종료 시점 기준*
