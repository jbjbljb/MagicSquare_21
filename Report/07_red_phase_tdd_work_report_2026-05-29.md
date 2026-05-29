# 07 RED Phase TDD Work Report

- **작성일:** 2026-05-29
- **범위:** PRD FR-01 기반 테스트 계획 · RED 테스트 · 결함 문서화 · 개발 가이드 보강
- **현재 단계:** RED 확인 완료 / GREEN 미착수

---

## 1. Executive Summary

본 세션에서는 MagicSquare 4×4 프로젝트의 **Track A (Boundary)** RED 단계를 착수했다. 앵커 시나리오 **SC-BND-001** (`grid=None` 입력 거부)를 기준으로 테스트 계획서를 작성하고, pytest 기반 실패 테스트 8건을 구현한 뒤, 실행 결과를 `defect_list.md`에 7건의 결함으로 등록했다.

| 항목 | 결과 |
|------|------|
| 테스트 실행 | `pytest tests/boundary/test_fr01_01_invalid_size.py -v` |
| 통과/실패 | **1 passed**, **7 failed** (의도된 RED) |
| 결함 등록 | DEF-001 ~ DEF-007 (Open) |
| GREEN | 미착수 (`solve_puzzle` → `NotImplementedError`) |

---

## 2. 요청 및 수행 결과

### A. 테스트 플랜 샘플 예제 선정 (코드 없음)

- `docs/PRD_MagicSquare.md` FR-01 Acceptance Criteria 검토
- **SC-BND-001 / AC-FR01-01** 선정: null 입력이 FR-01 검증 순서의 최선행 조건
- Domain resolver 미호출(AC-FR01-06)과 Boundary 격리 검증이 동시에 가능한 사유 문서화

### B. 테스트 계획서 작성

| 산출물 | 설명 |
|--------|------|
| `test_plan.md` | SC-BND-001 앵커, 경계값·Mock/Spy·커버리지·pytest-cov 전략 |

주요 내용:

- Track A 우선순위 (P0 null + resolve 0회 → P1 shape 경계값)
- BV-001~BV-006 경계값 표
- 4×4 정상 입력 명시적 제외
- Domain 95%+ / Boundary 85%+ 커버리지 목표

### C. README RED To-Do 리스트 추가

- `README.md`에 **§ RED 단계 To-Do 리스트** 삽입 (기존 섹션 유지)
- Track A/B, 커버리지, 결함 목록 연결 체크리스트 포함

### D. RED 테스트 코드 작성

| 경로 | 역할 |
|------|------|
| `tests/boundary/test_fr01_01_invalid_size.py` | AC-FR-01-01 RED 테스트 8건 |
| `src/boundary/solve_puzzle.py` | 진입점 (RED: `NotImplementedError`) |
| `src/boundary/schemas.py` | `FailureResult` (pydantic) |
| `src/boundary/contracts.py` | `INVALID_SIZE` 상수 |
| `src/boundary/ports.py` | `CompletionResolverPort` |
| `pyproject.toml` | pytest / dev 의존성 |

테스트 설계 요약:

- Given-When-Then 주석, `# AC-FR-01-01` 표기
- `test_[입력조건]_[기대동작]_[검증포인트]` 네이밍
- `unittest.mock.create_autospec`으로 `resolve()` 0회 격리 검증
- 경계값: `None`, `[]`, `[[]]*4`, 3×4

### E. 실행 환경 안내

- 가상환경(venv) 생성·활성화·`pip install -e ".[dev]"` 절차 문서화 (대화 응답)
- HTML 커버리지: `pytest --cov=src --cov-report=html` → `htmlcov/index.html`

### F. 결함 목록 문서화

| 산출물 | 설명 |
|--------|------|
| `defect_list.md` | DEF-001~007, OBS-001(계약 불일치), Closure 기준 |

- README 결함 체크리스트: `defect_list.md 생성` → **[x]**

### G. 본 보고서 및 Transcript Export

- `Report/07_red_phase_tdd_work_report_2026-05-29.md` (본 문서)
- `Prompt/07_export_transcript_red_phase_tdd_2026-05-29.md`

---

## 3. 테스트 실행 결과

```text
pytest tests/boundary/test_fr01_01_invalid_size.py -v
========================= 7 failed, 1 passed =========================
```

| 결과 | 테스트 |
|------|--------|
| FAILED (7) | null/shape 실패 반환, code/message, resolve 격리, `[]`, `[[]]*4`, 3×4 |
| PASSED (1) | `test_scope_contract_is_invalid_size_not_other_ac_codes` |

**실패 원인 (공통):** `src/boundary/solve_puzzle.py:18` — `NotImplementedError`

---

## 4. 산출물 목록

| 유형 | 파일 |
|------|------|
| 계획 | `test_plan.md` |
| 테스트 | `tests/boundary/test_fr01_01_invalid_size.py` |
| 소스 (RED) | `src/boundary/*.py`, `pyproject.toml` |
| 결함 | `defect_list.md` |
| 가이드 | `README.md` (RED To-Do 추가) |
| 커버리지 (생성물) | `htmlcov/` (로컬, 비커밋 권장) |
| 보고 | `Report/07_red_phase_tdd_work_report_2026-05-29.md` |
| Transcript | `Prompt/07_export_transcript_red_phase_tdd_2026-05-29.md` |

---

## 5. 추적성 매트릭스 (요약)

| Concept | Scenario | AC | RED Test | Component | 상태 |
|---------|----------|-----|----------|-----------|------|
| null 입력 거부 | SC-BND-001 | AC-FR01-01 | `test_none_grid_*` | `solve_puzzle` | RED |
| Domain 미호출 | SC-BND-001 | AC-FR01-06 | `test_none_grid_resolve_*` | `CompletionResolverPort` | RED |
| shape 경계 | SC-BND-002 유사 | AC-FR01-01* | `test_empty_list_*` 등 | `solve_puzzle` | RED |

\* 본 커밋 테스트는 README To-Do 계약 `INVALID_SIZE` 사용. PRD 원문은 `E_NULL_INPUT` / `E_DIM_*` 분리.

---

## 6. 관찰 사항 및 리스크

| ID | 항목 | 설명 | 권고 |
|----|------|------|------|
| OBS-001 | 계약 불일치 | PRD: `E_NULL_INPUT` / 테스트·README: `INVALID_SIZE` | GREEN 전 단일 계약 확정 |
| RISK-001 | AC 범위 혼선 | shape 실패를 AC-FR01-01 범위로 통합 테스트 | PRD 정합 시 AC-FR01-02 분리 검토 |
| RISK-002 | 커버리지 | RED 단계 Boundary 실행 분기 0% | GREEN 후 85%+ 재측정 |

---

## 7. 후속 작업 (GREEN 체크리스트)

1. `solve_puzzle()`에 null → `FailureResult(INVALID_SIZE)` 최소 구현
2. shape 검증 (`[]`, `[[]]*4`, 3×4) → 동일 INVALID_SIZE 또는 PRD 코드 분리 결정
3. 검증 실패 시 `resolver.resolve()` 미호출 보장
4. `pytest tests/boundary/test_fr01_01_invalid_size.py -v` → **8 passed**
5. `defect_list.md` DEF-001~007 **Closed** 처리
6. README: `모든 결함 수정 후 회귀 테스트 통과 확인` **[x]**
7. Boundary `--cov-fail-under=85` 게이트 통과

---

## 8. 참조 문서

- [docs/PRD_MagicSquare.md](../docs/PRD_MagicSquare.md)
- [test_plan.md](../test_plan.md)
- [defect_list.md](../defect_list.md)
- [README.md](../README.md)
- [Prompt/07_export_transcript_red_phase_tdd_2026-05-29.md](../Prompt/07_export_transcript_red_phase_tdd_2026-05-29.md)

---

*문서 버전 1.0 — RED Phase 세션 종료 시점 기준*
