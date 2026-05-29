# 12 Export Transcript — Golden Master 회귀 안전장치 (GM-1~3)

- **Exported at:** 2026-05-29
- **Scope:** GM-1 baseline · GM-2 테스트 코드 · GM-3 README · approve 패턴 · pytest 마킹
- **Pair report:** [Report/12_golden_master_work_report_2026-05-29.md](../Report/12_golden_master_work_report_2026-05-29.md)

---

## Turn 1 — GM-1 Golden Master baseline (GM-01~03)

**User**

현재 Magic Square Solver의 실제 출력을 기반으로 Golden Master 기준 파일을 생성하고 버전 관리에 포함한다.

- GM-1: `golden_master_expected.txt` 생성
- 입력 시나리오: 정상 / reverse / invalid blank / duplicate / no valid solution
- approve 패턴: 파일 없으면 생성, 있으면 비교, 불일치 시 unified diff FAIL
- 산출물: baseline + 생성 스크립트 + 설계 문서

**Assistant**

- `tests/golden_master.py` — API result serialization, approve 비교 유틸
- `tests/golden_master_expected.txt` — 5 시나리오 baseline (실제 Solver 출력)
- `tests/test_golden_master.py` — 단일 통합 회귀 테스트
- `scripts/generate_golden_master.py` — baseline 재생성 CLI
- `docs/golden_master_approve_pattern.md` — GM-1 설계 문서
- `tests/conftest.py` — `--approve-golden` CLI 옵션
- `git add tests/golden_master_expected.txt` (staged)

**Baseline (실제 출력):**

| Section | Output |
|---------|--------|
| normal_success (G1) | `[1,2,2,3,4,12]` |
| reverse_success (G2) | `[2,3,10,4,1,4]` |
| invalid_blank_count | `E002` |
| duplicate_number | `E005` |
| no_valid_solution (G3) | `UnsolvableDomainError` |

---

## Turn 2 — GM-2 테스트 코드 (GM-04~06, GM-07~10)

**User**

Golden Master 테스트 코드 작성 (GM-2). 이미 있으면 재작성.

- `@pytest.mark.golden_master` · `pytest -m golden_master -v`
- GM-TC-01~05 개별 테스트
- approve 패턴 · contract 검증 (int[6], row-major, 1-index, small-first, reverse, Error)
- 실패 시 `--- expected` / `+++ actual` diff

**Assistant**

- `tests/test_golden_master_magic_square.py` — GM-TC-01~05 개별 테스트 5건
- `tests/golden_master.py` — GM-TC 섹션 파싱, contract assert 헬퍼, section별 approve
- `pyproject.toml` — `markers: golden_master` 등록
- `tests/golden_master_expected.txt` — `[GM-TC-XX]` 섹션 헤더로 갱신
- `tests/test_golden_master.py` 삭제 (TC별 테스트로 대체)
- 섹션 구분선 파싱 버그 수정 (`normalize_section` regex)
- **pytest:** `pytest -m golden_master -v` → **5 passed** · 전체 **40 passed**

**Contract 보호 매핑:**

| GM | 규칙 | 테스트 |
|----|------|--------|
| GM-07 | row-major | GM-TC-01, 02 |
| GM-08 | 1-index | GM-TC-01, 02 |
| GM-09 | reverse fallback | GM-TC-02 |
| GM-10 | Error Contract | GM-TC-03~05 |

---

## Turn 3 — GM-3 README 업데이트

**User**

`README.md` · `## RED 단계 To-Do 리스트` 아래 Golden Master 회귀 안전장치 섹션 추가 (GM-01~10).

**Assistant**

- `README.md`에 **Golden Master 회귀 안전장치** 삽입
  - Refactoring 시작 전 구축 · GREEN 완료 후 즉시 적용
  - GM-01~10 전항목 `[x]`
  - `docs/golden_master_approve_pattern.md` 링크

---

## Turn 4 — Report · Transcript Export

**User**

Report 폴더에 보고서 생성, Prompt 폴더에 Transcript Export.

**Assistant**

- [Report/12_golden_master_work_report_2026-05-29.md](../Report/12_golden_master_work_report_2026-05-29.md)
- [Prompt/12_export_transcript_golden_master_2026-05-29.md](./12_export_transcript_golden_master_2026-05-29.md) (본 문서)
- [Report/README.md](../Report/README.md) 인덱스 갱신

---

## pytest Snapshot (최종)

```text
pytest -m golden_master -v
collected 40 items / 35 deselected / 5 selected
tests/test_golden_master_magic_square.py .....                           [100%]
====================== 5 passed, 35 deselected in 0.12s =======================

pytest -q
........................................                                 [100%]
40 passed in 0.15s
```

---

## Golden Master 파일 맵

| 경로 | 역할 |
|------|------|
| `tests/golden_master.py` | 캡처 · approve · contract |
| `tests/golden_master_expected.txt` | baseline (Git) |
| `tests/test_golden_master_magic_square.py` | GM-TC-01~05 |
| `scripts/generate_golden_master.py` | baseline 재생성 |
| `docs/golden_master_approve_pattern.md` | GM-2 설계 |

---

## Approve 패턴 요약

```bash
# 회귀
pytest -m golden_master -v

# baseline 갱신
pytest -m golden_master --approve-golden -v

# 또는
python scripts/generate_golden_master.py
GOLDEN_MASTER_APPROVE=1 pytest -m golden_master -v
```

---

## Git 상태 (Export 시점)

```text
 M README.md
A  docs/golden_master_approve_pattern.md
M  pyproject.toml
A  scripts/generate_golden_master.py
M  tests/conftest.py
A  tests/golden_master.py
A  tests/golden_master_expected.txt
A  tests/test_golden_master_magic_square.py
(staged, uncommitted)
```

---

*End of transcript — Golden Master GM-1~3 complete, stabilize/green*
