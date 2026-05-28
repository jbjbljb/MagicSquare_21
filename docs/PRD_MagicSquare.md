# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary
본 PRD는 4x4 마방진 문제를 "정답 계산"이 아닌 "불변식 기반 사고 훈련" 과제로 정의한다. 문서는 입력/출력 계약을 고정하고, Boundary와 Domain 책임을 분리하며, Dual-Track TDD(Track A: Boundary/UI Contract, Track B: Domain/Logic Invariant)로 RED-GREEN-REFACTOR를 운영하기 위한 구현 전 기준을 제공한다. 모든 요구사항은 검증 가능 문장으로 작성하며, Concept -> Rule -> Use Case -> Contract -> Test -> Component 추적성을 필수로 유지한다.

## 2. Background
`Report/01_Problem_Definition_Report.md`에 따라 본 과제의 핵심은 "마방진을 만들기"가 아니라 "규칙을 일관되게 판정하고 설명 가능한 기준을 고정하기"이다. 학습자는 손계산 기반 검증에서 반복성, 완전성, 재현성 문제를 겪는다. 따라서 본 프로젝트는 4x4 고정 문제를 사용해 규칙 정의, 상태 경계, 판정 기준, 실패 분류를 명시적으로 훈련하는 목적을 가진다.

## 3. Problem Statement
본 프로젝트의 문제는 "4x4를 채운다"가 아니라 "검증 가능한 불변식 집합을 충족하는지 판정하고, 위반 시 계약된 실패 정책을 반환하는 시스템을 설계한다"이다.
핵심은 다음 두 축이다.

- 입력 계약 고정: 무엇이 유효 입력인지 사전에 고정한다.
- 출력 계약 고정: 성공 반환 형식과 실패 정책을 사전에 고정한다.

이 두 계약은 TDD에서 RED 기준의 단일 출처로 사용된다.

## 4. Why Now / Why Chain
지금 이 프로젝트를 수행해야 하는 이유는 다음 학습 실패를 즉시 교정하기 위해서다.

- 구현 선행: 테스트 기준 없이 구현을 먼저 시작하는 습관
- 판정 기준 불명확: "통과/실패"의 근거가 실행마다 달라지는 문제
- 책임 혼합: Boundary 입력검증과 Domain 수학판정이 섞이는 구조
- 회귀 취약: 리팩토링 후 계약 파손을 탐지하지 못하는 문제

Why Chain은 다음과 같이 고정한다.

- Why #1: 완성의 의미를 "규칙 만족"으로 고정해야 한다.
- Why #2: 반복 가능한 자동 판정 체계가 필요하다.
- Why #3: TDD로 계약을 먼저 고정해야 모호성을 통제할 수 있다.

## 5. Target Users
- TDD 학습자
- 코드 리뷰어
- Clean Architecture/ECB 계층 분리 훈련 개발자

사용 환경은 콘솔 실행 또는 테스트 실행이며, 실제 UI 화면/DB/Web/API는 범위 밖으로 고정한다.

## 6. Vision & Epic Goal
- Vision: 불변식 중심으로 계약을 고정하고, 계약 위반을 일관되게 탐지하는 TDD 학습 시스템을 제공한다.
- Epic Goal: **불변식 기반 사고 훈련 시스템 구축**

`Report/06_scenario_verification_summary_2026-05-28.md` 반영 사항:

- Boundary/Domain 책임 분리는 유지한다.
- Scenario를 RED 분해 가능한 형태로 관리한다.
- 누락 시나리오(4x4 shape, small-first 즉시 성공, 경계값 1/16, 누락수 오름차순)는 보강 대상으로 포함한다.

## 7. Persona
- Persona P1: TDD 초중급 개발자. 실패 테스트를 먼저 정의하고 최소 구현으로 통과시키는 훈련이 필요하다.
- Persona P2: 계층 분리를 학습하는 개발자. Boundary와 Domain 책임 분리를 실습으로 체득하려 한다.
- Persona P3: 알고리즘 정답보다 계약/검증/리팩토링 흐름을 우선하는 사용자.

## 8. User Journey Summary
1) 문제 인식
- Pain Point: "무엇이 정답인지" 기준이 모호하다.
- Learning Outcome: 불변식 목록(I/O 포함)을 먼저 작성한다.

2) 계약 정의
- Pain Point: 실패 정책이 미정이면 테스트 기준이 흔들린다.
- Learning Outcome: 입력/출력/오류 계약을 고정한다.

3) 도메인 분리
- Pain Point: 입력검증과 수학판정을 한 계층에 섞는다.
- Learning Outcome: Boundary 검증과 Domain 판정을 분리한다.

4) Dual-Track TDD 진행
- Pain Point: Track 분리 없이 구현 우선으로 진행한다.
- Learning Outcome: Track A/Track B를 병행하고 RED 기준을 독립 유지한다.

5) 회귀 보호
- Pain Point: 리팩토링에서 계약 파손이 발생한다.
- Learning Outcome: Traceability와 회귀 테스트로 계약을 보호한다.

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 마방진 판정(행/열/대각선 10개 선)
- 두 조합 시도 후 결과 반환
- Boundary 계층 입력 검증
- 출력 계약 검증
- RED-GREEN-REFACTOR에 맞춘 테스트 가능 요구사항 정의

### 9.2 Out-of-Scope
- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전 마방진 생성 알고리즘
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

## 10. Functional Requirements

### FR-01 Input Verification, Boundary
- Description: Boundary는 입력 `int[][]`가 계약 조건을 만족하는지 검증한다.
- Layer: Boundary
- Input: `int[][] matrix`
- Processing Rules:
  - null 여부 검증
  - 4x4 shape 검증
  - 셀 값 범위 검증(`0` 또는 `1..16`)
  - 빈칸 개수 검증(`0` 정확히 2개)
  - 0 제외 중복 검증
- Output:
  - 성공 시 Domain 호출 가능 상태
  - 실패 시 표준 오류 코드/메시지 반환
- Acceptance Criteria:
  - AC-FR01-01: null 입력은 `E_NULL_INPUT` 반환
  - AC-FR01-02: 행/열 크기 위반은 `E_DIM_ROWS` 또는 `E_DIM_COLS` 반환
  - AC-FR01-03: 값 범위 위반은 `E_CELL_RANGE` 반환
  - AC-FR01-04: 빈칸 수 위반은 `E_EMPTY_COUNT` 반환
  - AC-FR01-05: 0 제외 중복은 `E_DUPLICATE` 반환
  - AC-FR01-06: AC-FR01-01~05 실패 시 Domain resolver 미호출
- Error / Exception Policy: 검증 실패는 예외 throw 대신 표준 오류 응답 반환
- Related Business Rules: BR-01, BR-02, BR-03, BR-04
- Related Test Direction: Track A의 입력 검증/미호출 테스트
- Component Candidate: `BoundaryValidator`

### FR-02 Blank Coordinate Discovery
- Description: row-major 순서로 첫 번째/두 번째 빈칸 좌표를 결정한다.
- Layer: Domain
- Input: 검증 통과한 4x4 matrix
- Processing Rules:
  - 행 우선, 열 우선으로 스캔
  - 첫 번째 `0`을 first blank로 지정
  - 두 번째 `0`을 second blank로 지정
- Output: `(r1,c1),(r2,c2)` (도메인 내부는 인덱스 정책 고정, 외부 반환은 1-index)
- Acceptance Criteria:
  - AC-FR02-01: 빈칸 좌표 반환 순서는 row-major 결과와 동일
  - AC-FR02-02: 빈칸 개수가 2가 아니면 `INVALID_EMPTY_COUNT`
- Error / Exception Policy: 도메인 실패 코드 반환
- Related Business Rules: BR-05, BR-02
- Related Test Direction: Track B의 blank finder 테스트
- Component Candidate: `BlankFinder`

### FR-03 Missing Number Discovery
- Description: 1..16에서 non-zero 값 집합을 제외해 누락 숫자 2개를 식별한다.
- Layer: Domain
- Input: 검증 통과한 4x4 matrix
- Processing Rules:
  - 전체 후보 집합 `1..16` 생성
  - non-zero 존재값 제외
  - 누락 숫자 2개 확인
  - 내부 표현은 오름차순 정렬(`mSmall < mLarge`)
- Output: `(mSmall, mLarge)`
- Acceptance Criteria:
  - AC-FR03-01: 누락 숫자 수는 항상 2개
  - AC-FR03-02: 내부 누락 쌍은 오름차순
  - AC-FR03-03: 범위/중복 위반 시 `OUT_OF_RANGE` 또는 `DUPLICATE_VALUE`
- Error / Exception Policy: 도메인 실패 코드 반환
- Related Business Rules: BR-06, BR-07, BR-03, BR-04
- Related Test Direction: Track B의 missing-number 테스트
- Component Candidate: `MissingNumberFinder`

### FR-04 Magic Square Validation
- Description: 완성 후보 격자가 마방진 불변식을 만족하는지 판정한다.
- Layer: Domain
- Input: 0이 없는 4x4 candidate matrix
- Processing Rules:
  - 10개 선(행4/열4/대각2) 전수 검사
  - 각 선 합 = 34 확인
- Output: valid/invalid 판정 결과
- Acceptance Criteria:
  - AC-FR04-01: 유효 격자는 10개 선 모두 34
  - AC-FR04-02: 1개 선이라도 불일치 시 invalid
  - AC-FR04-03: 부분 선 검사만으로 valid 반환 금지
- Error / Exception Policy: invalid는 비즈니스 결과로 처리
- Related Business Rules: BR-08, BR-09
- Related Test Direction: Track B의 validator 테스트
- Component Candidate: `MagicSquareValidator`

### FR-05 Two-Combination Solver and Result Formatting
- Description: 두 조합을 순차 시도해 성공 조합을 `int[6]`으로 반환한다.
- Layer: Control + Domain + Boundary 출력계약
- Input: 검증 통과 matrix
- Processing Rules:
  - Attempt 1: `mSmall -> first blank`, `mLarge -> second blank`
  - Attempt 1 성공 시 즉시 반환
  - Attempt 2: `mLarge -> first blank`, `mSmall -> second blank`
  - Attempt 2 성공 시 해당 배치 순서로 반환
  - 둘 다 실패 시 고정 실패 정책 실행
- Output:
  - 성공: `[r1,c1,n1,r2,c2,n2]`, 좌표 1-index, 길이 6
  - 실패: `E_NO_SOLUTION` (Boundary)
- Acceptance Criteria:
  - AC-FR05-01: small-first 성공 시 Attempt 1 순서 반환
  - AC-FR05-02: Attempt 1 실패 + reverse 성공 시 reverse 순서 반환
  - AC-FR05-03: 두 조합 모두 실패 시 `E_NO_SOLUTION`
  - AC-FR05-04: 성공 반환 배열 길이 6, 좌표 1..4
- Error / Exception Policy:
  - 비즈니스 실패는 표준 오류 응답 반환
  - 예상 불가 시스템 오류는 `E_INTERNAL`
- Related Business Rules: BR-10, BR-11, BR-12, BR-13
- Related Test Direction: Track A/B 통합 시도 순서 테스트
- Component Candidate: `Solver`, `ResultFormatter`

## 11. Business Rules / Domain Rules
- BR-01: 입력 행렬은 항상 4x4 정수 행렬이어야 한다.
- BR-02: 빈칸 값 `0`의 개수는 항상 정확히 2개여야 한다.
- BR-03: 각 셀 값은 항상 `0` 또는 `1..16`이어야 한다.
- BR-04: `0`을 제외한 숫자는 항상 중복이 없어야 한다.
- BR-05: 첫 번째 빈칸은 row-major 스캔으로 처음 발견된 `0`이어야 한다.
- BR-06: 누락 숫자 집합 크기는 항상 2여야 한다.
- BR-07: 누락 숫자 내부 표현은 항상 오름차순(`mSmall < mLarge`)이어야 한다.
- BR-08: 마방진 상수는 항상 `34`이어야 한다.
- BR-09: 행 4개, 열 4개, 대각선 2개의 합은 항상 각각 34여야 한다.
- BR-10: Attempt 1은 항상 small-first 배치 순서를 사용해야 한다.
- BR-11: Attempt 2는 항상 reverse 배치 순서를 사용해야 한다.
- BR-12: 성공 출력 좌표는 항상 1-index(`1..4`)여야 한다.
- BR-13: 성공 출력 형식은 항상 `int[6] = [r1,c1,n1,r2,c2,n2]`여야 한다.

## 12. Input / Output Contract

### Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code / Failure Policy |
|---|---|---|---|---|---|
| `matrix` | `int[][]` | null이 아니어야 함 | `[[16,2,3,13],[5,11,0,8],[9,7,6,12],[0,14,15,1]]` | `null` | `E_NULL_INPUT` |
| `matrix` shape | 4x4 | 행 개수 4, 각 행 열 개수 4 | 4x4 배열 | 3x4, 4x5 | `E_DIM_ROWS`, `E_DIM_COLS` |
| cell value | int | 값은 `0` 또는 `1..16` | `0`, `1`, `16` | `-1`, `17` | `E_CELL_RANGE` |
| blank count | count | `count(0)==2` | 0이 2개 | 0이 1개 또는 3개 | `E_EMPTY_COUNT` |
| non-zero uniqueness | set | 0 제외 중복 금지 | `...7...` 1회 | `...7...7...` | `E_DUPLICATE` |

### Output Contract (Success)

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code / Failure Policy |
|---|---|---|---|---|---|
| result | `int[6]` | 길이 6 고정 | `[1,2,2,3,4,12]` | `[1,2,2,3,4]` | `E_INTERNAL` |
| coordinates | int | `r1,c1,r2,c2`는 `1..4` | `1,2,3,4` | `0,2,3,4` | `E_INTERNAL` |
| values in result | int | `n1,n2`는 `1..16`, `n1!=n2` | `2,12` | `0,12`, `12,12` | `E_INTERNAL` |
| ordering semantics | rule | 성공한 시도 배치 순서를 그대로 반환 | Attempt 1 또는 2 순서 반영 | 임의 재정렬 | `E_INTERNAL` |

## 13. Error / Failure Policy

| Failure Case | Error Code | Message | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---|---|
| 4x4가 아닌 입력 | `E_DIM_ROWS` / `E_DIM_COLS` | `행 개수는 4여야 합니다.` / `각 행의 열 개수는 4여야 합니다.` | Boundary | 아니오 | AC-FR01-02, AC-FR01-06 |
| 빈칸 개수 불일치 | `E_EMPTY_COUNT` | `빈칸(0)은 정확히 2개여야 합니다.` | Boundary | 아니오 | AC-FR01-04, AC-FR01-06 |
| 값 범위 위반 | `E_CELL_RANGE` | `셀 값은 0 또는 1~16이어야 합니다.` | Boundary | 아니오 | AC-FR01-03, AC-FR01-06 |
| 0 제외 중복 | `E_DUPLICATE` | `0을 제외한 값은 중복될 수 없습니다.` | Boundary | 아니오 | AC-FR01-05, AC-FR01-06 |
| 두 조합 모두 실패 | `E_NO_SOLUTION` | `두 빈칸을 채워도 마방진이 되지 않습니다.` | Domain→Boundary 매핑 | 예 | AC-FR05-03 |

정책 고정:
- 입력 검증 실패는 Boundary에서 즉시 종료한다.
- 입력 검증 실패 시 Domain resolver는 호출되지 않는다.
- 비즈니스 실패(`NO_VALID_COMPLETION`)는 `E_NO_SOLUTION`으로 매핑한다.
- 예상 불가 예외는 `E_INTERNAL`으로 표준화한다.

## 14. Non-Functional Requirements
- NFR-01 Coverage: Domain Logic 라인 커버리지는 95% 이상이어야 한다.
- NFR-02 Coverage: Boundary Validation 라인 커버리지는 85% 이상이어야 한다.
- NFR-03 Determinism: 동일 입력은 항상 동일 성공 결과 또는 동일 오류 코드를 반환해야 한다.
- NFR-04 No Side Effects: 입력 행렬은 외부 관찰 기준에서 변경되지 않아야 한다.
- NFR-05 Performance: 4x4 기준 단일 요청 처리 시간은 50ms 이하여야 한다.
- NFR-06 Maintainability: Boundary/Control/Domain 의존 방향을 위반하지 않아야 한다.
- NFR-07 Maintainability: 설명 없는 매직 넘버 사용을 금지하고 명명된 상수만 허용해야 한다.
- NFR-08 Reliability: 금지 패턴(`print()`, bare `except`, 무의미 하드코딩)을 사용하지 않아야 한다.

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- 입력 검증 실패 코드 테스트를 우선 RED로 작성한다.
- 출력 형식 길이/좌표 범위 계약 테스트를 작성한다.
- 실패 응답 포맷(`code`,`message`) 테스트를 작성한다.
- 검증 실패 케이스에서 Domain resolver 미호출 테스트를 작성한다.

### 15.2 Track B — Domain / Logic TDD
- 빈칸 탐색(row-major) 테스트를 작성한다.
- 누락 숫자 탐색 및 오름차순 내부 표현 테스트를 작성한다.
- 마방진 검증(10개 선, 34 상수) 테스트를 작성한다.
- small-first 즉시 성공 테스트를 작성한다.
- small-first 실패 후 reverse 성공 테스트를 작성한다.
- 두 조합 모두 실패 테스트를 작성한다.

### 15.3 Parallel Progression Rules
- Rule-P1: UI RED와 Logic RED는 독립적으로 작성한다.
- Rule-P2: UI GREEN과 Logic GREEN은 각각 최소 구현 기준으로 통과시킨다.
- Rule-P3: 구조 개선은 REFACTOR 단계에서만 수행한다.
- Rule-P4: Domain 전체 선구현 후 Boundary를 붙이는 일괄 방식은 금지한다.
- Rule-P5: 테스트 삭제/약화로 Green을 만드는 행위를 금지한다.

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- TS-N01: small-first 성공
- TS-N02: small-first 실패 후 reverse 성공

### 16.2 Exception Scenarios
- TS-E01: 4x4가 아닌 입력
- TS-E02: 빈칸 개수 오류
- TS-E03: 값 범위 오류
- TS-E04: 중복 숫자 오류
- TS-E05: 두 조합 모두 실패

### 16.3 Boundary Scenarios
- TS-B01: 최소값 1 허용
- TS-B02: 최대값 16 허용
- TS-B03: `0`은 빈칸으로만 처리
- TS-B04: 출력 좌표 1-index 확인
- TS-B05: 반환 배열 길이 6 확인

### 16.4 Representative Test Data
- RD-01 small-first 성공 matrix:
  `[[16,0,3,13],[5,11,10,8],[9,7,6,0],[4,14,15,1]]`
- RD-02 reverse 성공 matrix:
  `[[16,2,3,13],[5,11,0,8],[9,7,6,12],[0,14,15,1]]`
- RD-03 invalid size matrix:
  `[[1,2,3],[4,5,6],[7,8,9]]`
- RD-04 invalid blank count matrix(빈칸 1개):
  `[[16,2,3,13],[5,11,10,8],[9,7,6,12],[0,14,15,1]]`
- RD-05 duplicate value matrix(0 제외 중복):
  `[[16,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,15]]`
- RD-06 invalid range matrix:
  `[[16,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,17]]`

## 17. Architecture Overview, High-Level
- Boundary Layer:
  - 입력 계약 검증 수행
  - 오류 코드/메시지 표준 응답 생성
  - 성공 시 출력 포맷 계약 검증
- Domain Layer:
  - 빈칸 탐색, 누락 수 계산, 마방진 판정, 조합 시도 규칙 수행
  - 불변식 검사 수행
- Control / Application Layer:
  - Boundary와 Domain 호출 흐름 조정
  - 실패 코드 매핑 일관성 유지
  - 본 프로젝트에서는 필요 시 최소 포함

의존 방향 고정:
- `Boundary -> Control -> Domain`
- Domain은 Boundary를 참조하지 않는다.
- Domain은 UI/DB/Web/파일시스템 의존을 갖지 않는다.

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| `BoundaryValidator` | 입력 계약 검증 및 오류 코드 결정 | Boundary | `int[][]` | valid flag or error | FR-01 | TS-E01~E04, TS-B01~B03 |
| `BlankFinder` | row-major 기준 두 빈칸 좌표 결정 | Domain | 4x4 matrix | `(blank1, blank2)` | FR-02 | TS-N01, TS-N02 |
| `MissingNumberFinder` | 누락 숫자 2개 식별 및 내부 오름차순 유지 | Domain | 4x4 matrix | `(mSmall,mLarge)` | FR-03 | TS-B01, TS-B02 |
| `MagicSquareValidator` | 10개 선 합 34 판정 | Domain | candidate matrix | valid/invalid | FR-04 | TS-N01, TS-N02, TS-E05 |
| `Solver` | Attempt 1/2 순차 실행 및 성공/실패 결정 | Control/Domain | validated matrix | solution or failure | FR-05 | TS-N01, TS-N02, TS-E05 |
| `ResultFormatter` | 성공 `int[6]` 포맷 및 실패 표준화 | Boundary/Control | solver result | success tuple or error schema | FR-05 | TS-B04, TS-B05 |

## 19. Risks & Ambiguities

| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index/0-index 혼동 | 좌표 계약 파손 및 오답 반환 | 출력 계약을 1-index로 고정하고 TS-B04 필수화 |
| row-major 첫 빈칸 정의 누락 | Attempt 순서 불일치 | BR-05를 단일 규칙으로 고정 |
| small-first/reverse 데이터 혼동 | 시나리오 오류로 테스트 신뢰 저하 | RD-01/RD-02를 대표 데이터로 고정 |
| 입력 행렬 변경 여부 불명확 | 부작용 발생 및 회귀 위험 | NFR-04로 무변경 정책 고정 |
| 두 조합 실패 정책 누락 | 실패 시 동작 불일치 | `E_NO_SOLUTION` 반환 정책으로 고정 |
| 상수 34 하드코딩 남발 | 가독성/유지보수 저하 | 명명 상수 사용 규칙 강제(NFR-07) |
| Boundary/Domain 책임 혼합 | 계층 위반 및 테스트 결합 증가 | FR별 레이어 고정 + Track 분리 운영 |
| 문서 우선순위 표현 불일치(`Report/4`) | 참조 기준 혼란 | Section 22에 Decision Needed 등록 |

## 20. Engineering Principles
- Python 스타일은 PEP8을 준수한다.
- 공개 함수/메서드는 type hints를 필수로 작성한다.
- 테스트 프레임워크는 `pytest`를 사용한다.
- 테스트는 AAA 패턴을 따른다.
- 커버리지는 Domain 95%+, Boundary 85%+를 유지한다.
- ECB 레이어 분리를 준수한다.
- RED-GREEN-REFACTOR 순서를 고정한다.
- `print()` 디버깅을 금지한다.
- bare `except`를 금지한다.
- 테스트 삭제/약화로 통과시키는 행위를 금지한다.
- 설명 없는 매직 넘버 사용을 금지한다.

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-FR01-02 | TS-E01 | `BoundaryValidator` |
| 빈칸 2개 | BR-02 | FR-01, FR-02 | AC-FR01-04, AC-FR02-02 | TS-E02 | `BoundaryValidator`, `BlankFinder` |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-03 | TS-E03, TS-B01, TS-B02 | `BoundaryValidator` |
| 중복 금지 | BR-04 | FR-01, FR-03 | AC-FR01-05, AC-FR03-03 | TS-E04 | `BoundaryValidator`, `MissingNumberFinder` |
| row-major 첫 번째 빈칸 | BR-05 | FR-02 | AC-FR02-01 | TS-N01, TS-N02 | `BlankFinder` |
| 누락 숫자 2개 | BR-06 | FR-03 | AC-FR03-01 | TS-N01, TS-N02 | `MissingNumberFinder` |
| 누락 숫자 오름차순(내부 표현) | BR-07 | FR-03 | AC-FR03-02 | TS-B01, TS-B02 | `MissingNumberFinder` |
| 마방진 상수 34 | BR-08 | FR-04 | AC-FR04-01 | TS-N01, TS-N02 | `MagicSquareValidator` |
| 행/열/대각선 합 규칙 | BR-09 | FR-04 | AC-FR04-02, AC-FR04-03 | TS-E05 | `MagicSquareValidator` |
| small-first 시도 | BR-10 | FR-05 | AC-FR05-01 | TS-N01 | `Solver` |
| reverse 시도 | BR-11 | FR-05 | AC-FR05-02 | TS-N02 | `Solver` |
| int[6] 반환 | BR-13 | FR-05 | AC-FR05-04 | TS-B05 | `ResultFormatter` |
| 1-index 좌표 | BR-12 | FR-05 | AC-FR05-04 | TS-B04 | `ResultFormatter` |

## 22. Open Questions / Decision Needed
- Decision Needed 1: 참조 우선순위 규칙 문구의 `Report/4`는 실제로 `Report/06`을 의미하는지 확정이 필요하다.
- Decision Needed 2: `Report/02`의 OUT-03(누락수 오름차순)과 OUT-05(reverse 성공 시 출력 순서) 해석 기준을 "내부 누락쌍 정렬"과 "출력은 성공 시도 배치 순서"로 확정할지 승인 필요.
- Decision Needed 3: 문제정의 문서(`Report/01`)의 "판정+설명 피드백" 범위와 본 PRD의 "2-blank solver 반환" 범위 간 최종 경계 승인 필요.
- Decision Needed 4: `E_INTERNAL` 발생 시 메시지 고정(한국어)과 로깅 정책 연계 범위를 PRD에 고정할지, 구현 가이드로 분리할지 확정 필요.

## 23. Appendix

### A. 참고 문서 목록
- `Report/01_Problem_Definition_Report.md`
- `Report/02_DualTrack_CleanArchitecture_TDD_Design.md`
- `Report/03_CursorRules_Work_Report.md`
- `Report/06_scenario_verification_summary_2026-05-28.md`
- `.cursorrules`
- `.cursor/rules/magicsquare-project.mdc`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
- `.cursor/rules/magicsquare-forbidden.mdc`
- `.cursor/rules/magicsquare-python-code-style.mdc`
- `.cursor/rules/magicsquare-tdd-testing.mdc`

### B. Cursor Rules 요약
- 프로젝트: Python 3.10+, ECB 구조(`boundary/control/entity`), `src/tests` 분리
- TDD: RED-GREEN-REFACTOR 단계 엄수
- 테스트: pytest, AAA, 커버리지 하한 유지
- 금지: `print()`, bare `except`, 설명 없는 하드코딩 상수
- 품질: 타입힌트/문서화/레이어 의존 방향 준수

### C. 대표 Gherkin Scenario 요약
- Scenario G-01 (Normal): Given 유효 4x4와 빈칸 2개, When solve, Then small-first 성공 시 `int[6]` 반환
- Scenario G-02 (Normal): Given 유효 4x4, When small-first 실패 후 reverse 성공, Then reverse 순서 `int[6]` 반환
- Scenario G-03 (Exception): Given 4x4 위반 입력, When solve, Then `E_DIM_ROWS` 또는 `E_DIM_COLS` 반환, Domain 미호출
- Scenario G-04 (Exception): Given 두 조합 모두 실패 입력, When solve, Then `E_NO_SOLUTION` 반환

### D. 향후 RED Test ID 후보
- Track A: `UT-BND-001`~`UT-BND-020`
- Track B: `DT-BLK-001`~`DT-BLK-010`, `DT-MIS-001`~`DT-MIS-010`, `DT-VAL-001`~`DT-VAL-015`, `DT-SOL-001`~`DT-SOL-015`
- Integration: `IT-001`~`IT-020`
