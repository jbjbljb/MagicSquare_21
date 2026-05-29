# 07 Export Transcript — RED Phase TDD

- **Exported at:** 2026-05-29
- **Scope:** MagicSquare RED 단계 세션 (테스트 플랜 · RED 테스트 · 결함 문서화)
- **Pair report:** [Report/07_red_phase_tdd_work_report_2026-05-29.md](../Report/07_red_phase_tdd_work_report_2026-05-29.md)

---

## Turn 1

**User**

`docs/PRD_MagicSquare.md`를 참고하여 테스트 플랜 작성을 위한 샘플 예제 1개를 선택해줘.

선택 기준:
1. PRD FR-01의 Acceptance Criteria 중 가장 선행 조건인 입력 유효성 검사
2. 비즈니스 로직(grid is None → INVALID_SIZE 반환)을 직접 검증
3. Boundary 계층과 Domain 진입점 호출 격리를 동시에 검증 가능한 기능

선택 시 AC ID, PRD 요구사항 번호, 입력/기대 출력, 선택 이유를 명시. 코드 작성 금지.

**Assistant**

PRD FR-01 검토 후 **SC-BND-001 / AC-FR01-01** (null 입력) 선정.

- 입력: `matrix = null` (`grid = None`)
- PRD 계약: `E_NULL_INPUT` / `입력 행렬이 null입니다.`
- 사용자 예시 템플릿(`INVALID_SIZE`)과 PRD 차이 명시
- AC-FR01-06(Domain 미호출) 연계 가능 사유 2줄 요약

---

## Turn 2

**User**

선택한 샘플 예제를 기반으로 `test_plan.md` 작성.

포함: pytest 단위 테스트 범위/우선순위, 경계값(`None`, `[]`, `[[]]*4`, 3×4·4×3·5×5), 4×4 정상 제외, 예외/특이 케이스, Domain resolve 0회 Mock/Spy, 커버리지 95%/85%, pytest-cov 명령.

**Assistant**

프로젝트 루트에 **`test_plan.md`** 생성 (TP-MAGICSQUARE-FR01-BND-001).

- SC-BND-001 앵커, P0~P2 우선순위
- BV-001~BV-006 경계값 표
- Mock 패턴 A/B/C, pytest-cov 실행 예시
- AC-FR01-02~05 / FR-02~05 범위 제외 명시

---

## Turn 3

**User**

`README.md`에 **§ RED 단계 To-Do 리스트** 섹션 추가 (기존 내용 유지).

Track A/B 체크리스트, 커버리지, `defect_list.md` 연결 항목 포함.

**Assistant**

`README.md` §7과 §8 사이에 RED To-Do 리스트 삽입.

- TC-A-01~07, TC-B-01~04
- 커버리지·결함 목록 체크박스 (미완료 상태)

---

## Turn 4

**User**

선택 샘플(SC-BND-001) 기반 실제 테스트 코드 작성.

조건: AC-FR-01-01 범위, 최소 5개 테스트, Given-When-Then, `INVALID_SIZE` / `Grid must be 4x4.`, 경계값·resolve 0회·메시지 동일성, AC-FR-01-02~05 제외, RED 실패 상태.

**Assistant**

다음 파일 생성:

| 파일 | 내용 |
|------|------|
| `tests/boundary/test_fr01_01_invalid_size.py` | RED 테스트 8건 |
| `src/boundary/solve_puzzle.py` | `NotImplementedError` (미구현) |
| `src/boundary/schemas.py`, `contracts.py`, `ports.py` | 계약·Port |
| `pyproject.toml` | pytest / pydantic / dev deps |

`pytest` 실행: **7 failed, 1 passed** (의도된 RED).

---

## Turn 5

**User**

테스트 코드를 가상환경 기준으로 실행하는 방법 안내.

**Assistant**

Windows PowerShell 기준 venv 절차 안내:

1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `pip install -e ".[dev]"`
4. `pytest tests/boundary/test_fr01_01_invalid_size.py -v`

실행 정책, `where python`, Cursor 인터프리터 선택 팁 포함.

---

## Turn 6

**User**

커버리지를 HTML로 보는 방법 안내.

**Assistant**

`pytest --cov=src --cov-report=html` → `htmlcov/index.html` 열기.

Boundary만 측정, `term-missing` 병행, `.gitignore`에 `htmlcov/` 권장.

---

## Turn 7

**User**

발견된 테스트 실패/결함을 `defect_list.md`에 정리. 표 형식(ID, Severity, AC ID, 재현, 기대, 실제, 근본 원인, 수정 요약). README 결함 체크박스 업데이트.

**Assistant**

**`defect_list.md`** 생성 — DEF-001~007 (Critical 2, High 5), OBS-001(계약 불일치).

README `defect_list.md 생성 및 발견 결함 기록` → **[x]**, 회귀 통과 항목은 미체크 유지.

---

## Turn 8

**User**

Report 폴더에 보고서 생성, Prompt 폴더에 Transcript Export.

**Assistant**

- `Report/07_red_phase_tdd_work_report_2026-05-29.md`
- `Prompt/07_export_transcript_red_phase_tdd_2026-05-29.md` (본 문서)
- `Report/README.md` 인덱스 갱신

---

## Session Artifact Index

| # | 산출물 |
|---|--------|
| 1 | `test_plan.md` |
| 2 | `README.md` (RED To-Do) |
| 3 | `tests/boundary/test_fr01_01_invalid_size.py` |
| 4 | `src/boundary/*`, `pyproject.toml` |
| 5 | `defect_list.md` |
| 6 | `htmlcov/` (로컬 생성) |
| 7 | `Report/07_red_phase_tdd_work_report_2026-05-29.md` |
| 8 | `Prompt/07_export_transcript_red_phase_tdd_2026-05-29.md` |

---

## Notes

- 본 transcript는 세션 대화를 **Turn 단위 요약** 형태로 export함.
- PRD 원문 AC ID는 `AC-FR01-01` 형식; 사용자·테스트에서는 `AC-FR-01-01` 표기 혼용됨.
- GREEN 단계 착수 시 본 transcript에 Turn 9(구현·8 passed) 추가 권장.
