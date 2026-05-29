# 08 Export Transcript — Dual-Track RED Design (FR-01~FR-05)

- **Exported at:** 2026-05-29
- **Scope:** FR-01~FR-05 Dual-Track RED 테스트 설계표 (코드·pytest 없음)
- **Pair report:** [Report/08_dual_track_red_design_report_2026-05-29.md](../Report/08_dual_track_red_design_report_2026-05-29.md)

---

## Turn 1

**User**

Dual-Track UI + Logic TDD 전문가 역할. **TDD phase: RED** — 오직 RED 테스트 설계표만 작성.

**금지 (엄격):**

- 구현/테스트/스켈레톤 코드, 클래스·파일 구조 확정
- GREEN / REFACTOR, pytest 실행, 파일 저장

**SSOT:** `docs/PRD_MagicSquare.md` v0.2, `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md`, `.cursorrules`

**프로젝트 계약:**

- 입력: 4×4 `int[][]`, `0`=빈칸 2개, 값 `0` 또는 `1~16`, 0 제외 중복 금지
- 출력: `int[6]` 1-index; M=34; 검증 순서: null → size → empty count → range → duplicate
- Boundary invalid: Failure envelope (E003/E001/E002/E004/E005), `execute` 0회
- Domain: Entity/Control, Domain Mock 금지

**범위:** FR-01~FR-05 Dual-Track RED 설계표

**Track A:** U-IN-* (입력 5종 + size 예시), U-OUT-* (길이 6, 1-index), U-FLOW-02 (execute 0회)

**Track B:** `find_blank_coords`, `find_not_exist_nums`, `is_magic_square` (G0~분리 6건), `solution` (G1/G2/G3 + 길이·1-index); G0~G3 부록

**출력 형식:** `# UI RED Tests` / `# Logic RED Tests` 마크다운 표 + 검수 체크리스트

**Assistant**

**TDD phase: RED** 로 응답 시작.

- SSOT: `Report/02.MagicSquare_...` 없음 → `02_DualTrack_CleanArchitecture_TDD_Design.md` 대체 명시
- **G0~G3** 픽스처 표 작성 (G3 placeholder)
- **# UI RED Tests** 표 11행 (+ U-IN-05b)
- **# Logic RED Tests** 표 13행
- Invariant I1~I11 ↔ Test ID 매핑
- 검수 체크리스트 6항목 전부 ✅
- 코드·파일 저장 없음

---

## Turn 2

**User**

Report 폴더에 보고서 생성하고, Prompt 폴더에 Transcript도 Export 해줘.

**Assistant**

- `Report/08_dual_track_red_design_report_2026-05-29.md` 생성
- `Prompt/08_export_transcript_dual_track_red_design_2026-05-29.md` 생성 (본 문서)
- `Report/README.md` 인덱스 갱신

---

## Session Artifact Index

| # | 산출물 | 비고 |
|---|--------|------|
| 1 | Dual-Track RED 설계표 (대화 본문) | UI 11건 + Logic 13건 |
| 2 | `Report/08_dual_track_red_design_report_2026-05-29.md` | 작업 보고서 |
| 3 | `Prompt/08_export_transcript_dual_track_red_design_2026-05-29.md` | 본 Transcript |
| 4 | `Report/README.md` | 08 항목 추가 |

**미생성 (의도):** `tests/`, `src/` 신규 RED 테스트, pytest 실행

---

## Design Snapshot (요약)

### Track A Test IDs

`U-IN-01` … `U-IN-06`, `U-IN-05b`, `U-OUT-01`, `U-OUT-02`, `U-FLOW-02`

### Track B Test IDs

`D-LOC-01`, `D-MIS-01`, `D-VAL-01` … `D-VAL-06`, `D-SOL-01` … `D-SOL-04`

### G1 기대 solution

`[2,2,7,3,3,10]`

### G2 기대 solution (reverse)

`[2,3,10,4,1,4]`

---

## Notes

- PRD 원문 AC는 `AC-FR01-01` 형식; 일부 대화·기존 테스트는 `AC-FR-01-01` / `INVALID_SIZE` 혼용 — GREEN 전 계약 통합 권장.
- [Report/07](./07_red_phase_tdd_work_report_2026-05-29.md)은 SC-BND-001 중심 **코드 RED** 세션; 본 세션(08)은 **전체 FR 설계표** 세션으로 구분.
- GREEN 착수 시 Turn 3(첫 RED 테스트 파일·G3 확정) 추가 권장.
