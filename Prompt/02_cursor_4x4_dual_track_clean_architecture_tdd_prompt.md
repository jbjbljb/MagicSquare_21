# 4x4 magic square — dual-track clean architecture TDD (conversation transcript)
_Exported on 5/28/2026 from Cursor — MagicSquare_XX session_

---

**User**

@c:\DEV\MagicSquare_XX\ 에 대해 RED, Green, Refactoring 작업을 할 건데, 적당한 브렌치 전략을 알려줘

---

**Cursor**

## 권장 모델: Git Flow Lite

`main`(안정) + `develop`(통합) + **행동 단위 `feature/*`** (TDD 단계마다 브랜치 3개는 비권장).

| 브랜치 | 역할 |
|--------|------|
| **main** | 마일스톤, 항상 Green |
| **develop** | 일상 통합 |
| **feature/*** | invariant/계약 단위로 RED→Green→Refactor 한 사이클 |

**한 사이클:** `develop` → `feature/...` → (RED→Green→Refactor 커밋) → `develop` merge.

**feature 이름 예:** `feature/v4-incomplete-vs-invalid`, `feature/i3-all-lines-sum-34`

**주의:** RED(실패 테스트) 커밋은 feature 브랜치에만 두고 `develop`/`main`은 항상 Green 유지.

---

**User**

develop 브렌치에서 red, green, refactoring 브렌치를 생성하는 전략으로 진행할 겁니다. 검토해 주고, 괜찮으면 develop 브렌치에서 spec 브렌치 먼저 만들어 주세요.

---

**Cursor**

## 전략 검토: `develop` → `spec` / `red` / `green` / `refactor`

**결론: 진행 가능.** 단, 브랜치를 TDD 단계 이름의 **장기 브랜치**로 두지 말고, **한 사이클 = 한 lineage**로 운영:

```text
develop → spec → red → green → refactor → merge develop
```

| 규칙 | 내용 |
|------|------|
| 순차 분기 | `red`는 `spec` tip, `green`은 `red` tip … |
| develop Green | 실패 테스트는 `red`까지 |
| 사이클 후 | merge 후 브랜치 삭제 또는 develop 기준 재생성 |

## `spec` 브랜치 생성 완료

로컬 `develop`(`76fc56c`)에서 **`spec`** 생성, 현재 체크아웃 `spec`.

---

**User**

너는 Cursor.AI용 프롬프트 설계자다.
나는 Magic Square 4x4 TDD 설계 문서를 만들기 위한 프롬프트가 필요하다.
지금 설계 문서를 만들지 말고,그 설계 문서를 만들 수 있는 실행용 프롬프트만 작성하라.

---

**Cursor**

실행용 프롬프트(설계 문서 생성 전용)를 제공함. 핵심 구조:

- **역할:** TDD 설계 문서 작성 전문가
- **금지:** 구현 코드, 알고리즘, UI, n×n, 기술 스택 확정
- **필수 읽기:** `README.md`, `Report/01_Problem_Definition_Report.md`
- **산출:** `Report/02_TDD_Design_Report.md` (§1~§13 고정)
- **내용:** Invariant 매핑, SCN-ID 시나리오, spec/red/green/refactor 브랜치 DoD, Traceability

*(전체 프롬프트 본문은 당시 채팅 응답 참조 — §13개 섹션, P0 시나리오 8개, Open Decision 표 포함)*

---

**User**

당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정
입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------
# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
...
# 4) Integration & Verification
## 4.5 Traceability Matrix (필수)

------------------------------------------------------------
추가 조건
------------------------------------------------------------
- 모호한 표현 금지
- 모든 규칙은 검증 가능해야 함
- 구현 코드 작성 금지
- 표/체크리스트를 적극 사용

---

**Cursor**

요청한 출력 구조(§1~§4)에 맞춰 Dual-Track UI + Logic TDD · Clean Architecture 설계를 작성함.

**산출 요약**

| 섹션 | 핵심 |
|------|------|
| §1 Logic | `Grid`, `CompletionSolver`, `MagicSquareValidator`, Domain API, DT-* 테스트 |
| §2 Screen | `PuzzleBoundary`, Input/Output/Error schema, UT-* (Domain Mock) |
| §3 Data | `MatrixRepository`, InMemory 추천, ST-* |
| §4 Integration | 의존성 방향, IT-*, RG-*, 커버리지 95/85/80%, Traceability Matrix |

**고정 계약:** 빈칸 2개, 스캔 순서(행·열 1→4), `int[6]` 1-index, 에러 문구 8종 고정.

**전문 보고서:** [Report/02_DualTrack_CleanArchitecture_TDD_Design.md](../Report/02_DualTrack_CleanArchitecture_TDD_Design.md)

---

**User**

다음의 순서로 실행해줘
1. Report 폴더에 니가 작성한 내용을 보고서로 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompting 폴더에 Export transcript 해줘 프롬프트 파일이름은 적절히 정해주고, 다만 02_ prefix를 붙여줘

---

**Cursor**

1. `Report/02_DualTrack_CleanArchitecture_TDD_Design.md` 생성 완료  
2. `Prompt/02_cursor_4x4_dual_track_clean_architecture_tdd_prompt.md` (본 파일) export 완료  
3. `Report/README.md` 에 02 문서 링크 추가

---

## 재실행용 — Dual-Track 설계 프롬프트 (단독 붙여넣기)

아래 블록만 복사해 새 Cursor 채팅에 붙이면 동일 설계를 다시 요청할 수 있다.

```markdown
당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련

제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정

입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지

출력 계약:
- int[6], 좌표 1-index, [r1,c1,n1,r2,c2,n2]
- n1,n2 = 누락 수(오름차순). 작은수→첫 빈칸·큰수→둘째 빈칸이 마방진이면 그 순서, 아니면 반대

빈칸 순서: 행 1→4, 열 1→4 스캔으로 첫·둘째 빈칸 고정.

참조: README.md, Report/01_Problem_Definition_Report.md

출력 형식 — 반드시 다음 구조:
# 1) Logic Layer … # 4) Integration … ## 4.5 Traceability Matrix

추가: 모호한 표현 금지, 검증 가능한 규칙만, 표/체크리스트 사용.
산출 파일: Report/02_DualTrack_CleanArchitecture_TDD_Design.md (없으면 생성, 있으면 갱신)
```

---

## 재실행용 — TDD 설계 문서 생성 프롬프트 (STEP 1~5 기반)

```markdown
당신은 TDD 설계 문서 작성 전문가입니다.
MagicSquare_XX 4×4 마방진 **판정** 도메인 TDD 설계 문서를 작성하십시오.

금지: 구현 코드, 알고리즘, UI, n×n 확정, 기술 스택 확정
필수 읽기: README.md, Report/01_Problem_Definition_Report.md
산출: Report/02_TDD_Design_Report.md (§1~§13: 개요, Frozen/Open, 상태모델, I/O, Invariant 매핑, SCN 카탈로그, 테스트 레이어, RED-GREEN-REFACTOR·spec/red/green/refactor DoD, Traceability, DoD, 미결정, 다음단계)

구현 코드 출력 금지. 먼저 파일 경로 보고 후 본문 출력.
```

---

*Transcript 끝 — 설계 전문: [Report/02_DualTrack_CleanArchitecture_TDD_Design.md](../Report/02_DualTrack_CleanArchitecture_TDD_Design.md)*
