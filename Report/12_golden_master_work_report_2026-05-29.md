# 12 Golden Master 회귀 안전장치 Work Report

- **작성일:** 2026-05-29
- **브랜치:** `stabilize/green`
- **범위:** GM-1 ~ GM-3 · Golden Master baseline · approve 패턴 · pytest 마킹 · README GM To-Do
- **현재 단계:** GREEN 완료 후 **REFACTOR 전** 회귀 안전장치 구축 완료

---

## 1. Executive Summary

본 세션에서는 Magic Square Solver의 **실제 출력**을 Golden Master baseline으로 고정하고, approve 패턴 기반 회귀 테스트(GM-TC-01~05)를 구축했다. REFACTOR 시작 전 drift를 감지할 수 있는 안전장치를 GREEN 직후 적용했다.

| 항목 | 결과 |
|------|------|
| GM-1 baseline | `tests/golden_master_expected.txt` (5 시나리오) |
| GM-2 테스트 | `tests/test_golden_master_magic_square.py` (5건, `@pytest.mark.golden_master`) |
| GM-3 README | `README.md` Golden Master 회귀 안전장치 섹션 (GM-01~10 `[x]`) |
| Golden Master pytest | **5 passed** (`pytest -m golden_master -v`) |
| 통합 pytest | **40 passed** (기존 35 + Golden Master 5) |
| 설계 문서 | `docs/golden_master_approve_pattern.md` |
| 생성 스크립트 | `scripts/generate_golden_master.py` |
| Git | staged (커밋·push 미수행) |

---

## 2. 작업 이력 (GM-01 ~ GM-10)

### 2.1 기준 파일 생성

| ID | 작업 | 산출물 | 상태 |
|----|------|--------|------|
| GM-01 | baseline 파일 생성 | `tests/golden_master_expected.txt` | ✅ |
| GM-02 | 정상 / 역순 / 오류 시나리오 | GM-TC-01~05 섹션 | ✅ |
| GM-03 | 버전 관리 포함 | `git add tests/golden_master_expected.txt` (staged) | ✅ |

### 2.2 테스트 코드

| ID | 작업 | 산출물 | 상태 |
|----|------|--------|------|
| GM-04 | Golden Master 테스트 | `tests/test_golden_master_magic_square.py` | ✅ |
| GM-05 | approve 패턴 | `--approve-golden`, `GOLDEN_MASTER_APPROVE=1` | ✅ |
| GM-06 | PASS 확인 | `pytest -m golden_master -v` → 5 passed | ✅ |

### 2.3 회귀 보호

| ID | 보호 규칙 | 테스트 |
|----|-----------|--------|
| GM-07 | row-major | GM-TC-01, GM-TC-02 (`assert_contract_row_major`) |
| GM-08 | 1-index 출력 | GM-TC-01, GM-TC-02 (`assert_contract_int6`) |
| GM-09 | reverse fallback | GM-TC-02 (`assert_contract_reverse_fallback`) |
| GM-10 | Error Contract | GM-TC-03 `E002`, GM-TC-04 `E005`, GM-TC-05 `UnsolvableDomainError` |

---

## 3. 아키텍처 및 파일 구조

```
tests/
├── golden_master.py                    # 캡처 · 직렬화 · approve · contract 검증
├── golden_master_expected.txt          # Golden Master baseline (Git tracked)
├── test_golden_master_magic_square.py  # GM-TC-01~05 회귀 테스트
└── conftest.py                         # --approve-golden, golden_approve fixture

scripts/
└── generate_golden_master.py           # baseline 재생성 CLI

docs/
└── golden_master_approve_pattern.md    # GM-2 설계 문서

pyproject.toml                          # markers: golden_master
README.md                               # GM-01~10 체크리스트
```

---

## 4. Golden Master 시나리오 (GM-TC)

| ID | 시나리오 | Grid SSOT | 기대 출력 |
|----|----------|-----------|-----------|
| GM-TC-01 | small-first 성공 | G1 (RD-01) | `[1,2,2,3,4,12]` |
| GM-TC-02 | reverse 성공 | G2 (RD-02) | `[2,3,10,4,1,4]` |
| GM-TC-03 | INVALID_BLANK_COUNT | 빈칸 3개 | `Error: E002` |
| GM-TC-04 | DUPLICATE_NUMBER | non-zero 중복 7 | `Error: E005` |
| GM-TC-05 | NO_VALID_MAGIC_SQUARE | G3 | `Error: UnsolvableDomainError` |

**캡처 방식:** stdout 대신 **API result serialization** (`capture_scenario_output`)

1. `InputValidator.validate` → Boundary `FailureResult.code`
2. `solution()` 성공 → compact `int[6]`
3. `UnsolvableDomainError` → Domain 예외명 직렬화

---

## 5. Approve 패턴

| 상태 | 동작 |
|------|------|
| baseline **없음** | 현재 출력으로 `golden_master_expected.txt` 자동 생성 → PASS |
| baseline **있음** | `open(expected).read()` vs actual section 비교 |
| **불일치** | `--- expected` / `+++ actual` unified diff → FAIL |
| **갱신** | `pytest -m golden_master --approve-golden -v` |

---

## 6. pytest 실행

```bash
# Golden Master 전용
pytest -m golden_master -v

# baseline 갱신
pytest -m golden_master --approve-golden -v

# 독립 생성
python scripts/generate_golden_master.py
```

### 6.1 실행 결과 (2026-05-29)

```text
pytest -m golden_master -v
collected 40 items / 35 deselected / 5 selected
tests/test_golden_master_magic_square.py::...test_gm_tc_01_normal_success PASSED
tests/test_golden_master_magic_square.py::...test_gm_tc_02_reverse_success PASSED
tests/test_golden_master_magic_square.py::...test_gm_tc_03_invalid_blank_count PASSED
tests/test_golden_master_magic_square.py::...test_gm_tc_04_duplicate_number PASSED
tests/test_golden_master_magic_square.py::...test_gm_tc_05_no_valid_magic_square PASSED
====================== 5 passed, 35 deselected in 0.12s =======================

pytest -q  →  40 passed
```

---

## 7. README 업데이트 (GM-3)

`README.md` · `## RED 단계 To-Do 리스트` 직하에 **Golden Master 회귀 안전장치** 섹션 추가:

- Refactoring 시작 전 구축 · GREEN 완료 후 즉시 적용
- GM-01 ~ GM-10 전항목 `[x]`
- 설계 문서 링크: `docs/golden_master_approve_pattern.md`

---

## 8. 변경 파일 목록

| 경로 | 유형 |
|------|------|
| `tests/golden_master.py` | 신규 |
| `tests/golden_master_expected.txt` | 신규 |
| `tests/test_golden_master_magic_square.py` | 신규 |
| `tests/conftest.py` | 수정 (`--approve-golden`, `golden_approve`) |
| `scripts/generate_golden_master.py` | 신규 |
| `docs/golden_master_approve_pattern.md` | 신규 |
| `pyproject.toml` | 수정 (`markers: golden_master`) |
| `README.md` | 수정 (GM-3 섹션) |
| `tests/test_golden_master.py` | 삭제 (GM-2에서 TC별 테스트로 대체) |

---

## 9. 향후 과제 (Out of Scope)

| 항목 | 설명 |
|------|------|
| Boundary `E_NO_SOLUTION` GREEN | GM-TC-05 Error 코드를 `UnsolvableDomainError` → `E_NO_SOLUTION`으로 갱신 |
| REFACTOR 단계 | Golden Master 40 passed 유지하며 구조 개선 |
| 커버리지 gate | Domain 95%+, Boundary 85%+ (README 목표) |

---

## 10. 추적성

| Concept | 문서 | 테스트 |
|---------|------|--------|
| Golden Master baseline | GM-1, `docs/golden_master_approve_pattern.md` | `golden_master_expected.txt` |
| Approve 패턴 | GM-2, GM-5 | `assert_scenario_golden` |
| Contract 보호 | GM-7~10 | `test_golden_master_magic_square.py` |
| README 체크리스트 | GM-3 | `README.md` § Golden Master |

**Pair Transcript:** [Prompt/12_export_transcript_golden_master_2026-05-29.md](../Prompt/12_export_transcript_golden_master_2026-05-29.md)

---

*End of report — Golden Master GM-1~3 complete, stabilize/green (uncommitted)*
