# Golden Master Approve Pattern — GM-2

| 항목 | 내용 |
|------|------|
| **문서 ID** | GM-MAGICSQUARE-002 |
| **버전** | 2.0 |
| **기준 파일** | `tests/golden_master_expected.txt` |
| **캡처 모듈** | `tests/golden_master.py` |
| **회귀 테스트** | `tests/test_golden_master_magic_square.py` |
| **생성 스크립트** | `scripts/generate_golden_master.py` |

---

## 1. 목적

Magic Square Solver의 **API result serialization** 출력을 Golden Master로 고정하고, GM-TC-01~05 개별 회귀 테스트로 drift를 감지한다.

---

## 2. 테스트 케이스 (GM-TC)

| ID | 시나리오 | Grid | 검증 대상 |
|----|----------|------|-----------|
| GM-TC-01 | 정상 조합 성공 | G1 (RD-01) | int[6], row-major, 1-index, small-first |
| GM-TC-02 | reverse 조합 성공 | G2 (RD-02) | int[6], row-major, 1-index, reverse fallback |
| GM-TC-03 | INVALID_BLANK_COUNT | 빈칸 3개 | Error Contract `E002` |
| GM-TC-04 | DUPLICATE_NUMBER | non-zero 중복 | Error Contract `E005` |
| GM-TC-05 | NO_VALID_MAGIC_SQUARE | G3 | Domain `UnsolvableDomainError` |

---

## 3. 출력 캡처

**API result serialization** (`capture_scenario_output`):

1. Boundary `InputValidator` → `FailureResult.code` → `Error:\n{code}`
2. Control `solution()` 성공 → `Output:\n[r1,c1,n1,r2,c2,n2]`
3. `UnsolvableDomainError` → `Error:\nUnsolvableDomainError`

---

## 4. Approve 패턴

| 상태 | 동작 |
|------|------|
| 기준 파일 **없음** | `golden_master_expected.txt` **자동 생성** 후 PASS |
| 기준 파일 **있음** | `open(expected).read()` vs actual section **비교** |
| **불일치** | `--- expected` / `+++ actual` unified diff → FAIL |
| **승인(갱신)** | `--approve-golden` 또는 `GOLDEN_MASTER_APPROVE=1` |

---

## 5. 실행

```bash
# Golden Master 전용 실행
pytest -m golden_master -v

# 기준 파일 갱신
pytest -m golden_master --approve-golden -v

# 독립 생성
python scripts/generate_golden_master.py
git add tests/golden_master_expected.txt
```

---

## 6. 실행 결과 예시

```
$ pytest -m golden_master -v
============================= test session starts =============================
collected 5 items

tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_01_normal_success PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_02_reverse_success PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_03_invalid_blank_count PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_04_duplicate_number PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_05_no_valid_magic_square PASSED

============================== 5 passed in 0.12s ==============================
```

**불일치 시 diff 예시:**

```
--- expected (GM-TC-01)
+++ actual (GM-TC-01)
@@ -6,4 +6,4 @@
 4 14 15 1
 Output:
-[1,2,2,3,4,12]
+[1,2,2,3,4,11]
```

---

## 7. 기준 파일 구조

```text
[GM-TC-01]
Input:
16 0 3 13
...
Output:
[1,2,2,3,4,12]

________________________________________

[GM-TC-02]
...
```

---

## 8. pytest 마킹

- 클래스/함수: `@pytest.mark.golden_master`
- `pyproject.toml` markers 등록
- 필터: `pytest -m golden_master`
