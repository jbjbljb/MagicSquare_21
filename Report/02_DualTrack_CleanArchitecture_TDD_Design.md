# 4×4 Magic Square — Dual-Track UI + Logic TDD · Clean Architecture 설계

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **범위** | Logic / Screen(Boundary) / Data 레이어 설계, 계약, 테스트·통합 계획 |
| **작성일** | 2026-05-28 |
| **상태** | 설계 문서(TDD)·구현 미포함 |
| **전제 문서** | [01_Problem_Definition_Report.md](./01_Problem_Definition_Report.md), [루트 README.md](../README.md) |

---

## 문서 목적

알고리즘 난이도보다 **레이어 분리 + 계약 기반 테스트 + 리팩토링** 훈련을 위해, Dual-Track TDD(UI Track / Logic Track)와 Clean Architecture 의존성 방향을 고정한다.

**구현 코드·알고리즘·UI 화면·DB는 본 문서 범위 외.**

---

## 고정 입·출력 계약 (프로젝트 전역)

### 입력

| 규칙 ID | 내용 |
|---------|------|
| IN-01 | `int[4][4]` |
| IN-02 | `0` = 빈칸 |
| IN-03 | 빈칸(0) **정확히 2개** |
| IN-04 | 값: `0` 또는 `1~16` |
| IN-05 | 0 제외 값 **중복 금지** |

### 출력

| 규칙 ID | 내용 |
|---------|------|
| OUT-01 | `int[6]` = `[r1,c1,n1,r2,c2,n2]` |
| OUT-02 | 좌표 **1-index** (`1..4`) |
| OUT-03 | `n1,n2` = 누락 수 **오름차순** (`n1 < n2`) |
| OUT-04 | 배치 시도 1: 작은 수→첫 빈칸, 큰 수→둘째 빈칸 → 마방진이면 그 순서 반환 |
| OUT-05 | 시도 1 실패·시도 2 성공 시 `[r1,c1,n2,r2,c2,n1]` |

### 빈칸 스캔 순서 (고정)

행 `1→4`, 열 `1→4` 순으로 `0`인 셀을 찾아 **첫 빈칸**, **둘째 빈칸**을 정한다.

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 구분 | 이름 | 책임 (SRP) | 비고 |
|------|------|------------|------|
| **Entity** | `Grid` | 4×4 셀 집합 보유; 불변 크기 4×4 | 값 변경은 `Grid` 메서드 또는 팩토리를 통해서만 |
| **Value Object** | `Cell` | `(row, col)` 1-index 좌표; 동등성·유효 범위(1~4) 검증 | 좌표계 단일 출처 |
| **Value Object** | `CellValue` | 0(빈칸) 또는 1~16; 범위 위반 시 생성 거부 | 0과 1~16 구분 |
| **Value Object** | `MagicConstant` | 4×4 마방진 합 목표값 **34** 고정 | `n=4` 전용 상수 |
| **Value Object** | `Line` | 검사 대상 선(행/열/대각) 정의; 소속 `Cell` 4개 | 총 10개 선 집합 |
| **Domain Service** | `LineSumCalculator` | 한 `Line`의 합 계산 | 산술만 담당 |
| **Domain Service** | `MagicSquareValidator` | 완전 채워진 격자가 I-2·I-3 만족 여부 판정 | 10개 선 전수 검사 |
| **Domain Service** | `EmptyCellLocator` | 빈칸(0) 위치를 **스캔 순서**로 2개 반환 | 순서 규칙 고정 |
| **Domain Service** | `MissingNumberResolver` | 1~16 중 격자에 없는 수 2개 식별·오름차순 정렬 | 조합은 항상 1쌍 |
| **Domain Service** | `CompletionSolver` | 두 빈칸에 두 수를 배치해 마방진 되는 순서 결정 | 출력 `int[6]` 생성 규칙 소유 |
| **Domain Service** | `PartialGridPolicy` | 입력 격자가 “빈칸 2개·중복 없음·범위” 도메인 전제 만족 여부 | Domain은 **재검증** |

**Aggregate Root:** `Grid` — 완성 판정·채움 시뮬레이션의 일관성 경계.

**Application Layer (선택):** `SolvePuzzleUseCase` — UI 계약 DTO ↔ Domain 변환·`CompletionSolver` 호출·결과 매핑.

---

## 1.2 도메인 불변조건(Invariants)

### (A) 마방진 대상 불변 (완성 격자 기준)

| ID | 불변 | 검증 가능 조건 |
|----|------|----------------|
| **I-1** | 격자 크기 4×4 | `rows==4 && cols==4` |
| **I-2** | 값 집합 = {1,…,16} 각 1회 | 중복 0, 누락 0, 0 없음 |
| **I-3** | 행 4·열 4·주대각·부대각 합 = **34** | 10개 선 각각 `sum==34` |
| **I-4** | 동일 규칙을 만족하는 서로 다른 완성 격자는 동등 | 특정 배치 문자열 비교 금지 |

### (B) 본 퍼즐(빈칸 2개) 입력 불변

| ID | 불변 | 검증 가능 조건 |
|----|------|----------------|
| **P-1** | 빈칸(0) 개수 = **정확히 2** | `count(0)==2` |
| **P-2** | 0 외 값 ∈ [1,16] | 모든 non-zero |
| **P-3** | 0 제외 값 중복 없음 | `distinct(nonZero).size==14` |
| **P-4** | 누락 수는 {1..16}\\{격자 non-zero} 크기 2 | 자동 도출 |

### (C) 빈칸 순서·출력 불변

| ID | 불변 | 검증 가능 조건 |
|----|------|----------------|
| **O-1** | **첫 빈칸** = 행 1→4, 열 1→4 스캔 시 최초 `0` | `EmptyCellLocator` 단일 규칙 |
| **O-2** | **둘째 빈칸** = 첫 빈칸 이후 동일 스캔으로 두 번째 `0` | |
| **O-3** | `n1,n2` = 누락 수 오름차순 (`n1 < n2`) | |
| **O-4** | 배치 시도 1: `(n1→첫 빈칸, n2→둘째 빈칸)` 마방진이면 `[r1,c1,n1,r2,c2,n2]` | 1-index 좌표 |
| **O-5** | 시도 1 실패·시도 2 성공 시 `[r1,c1,n2,r2,c2,n1]` | 반대 배치 |
| **O-6** | 두 시도 모두 실패 → Domain 실패 `NO_VALID_COMPLETION` | |

### (D) 판정·결정성 불변

| ID | 불변 | 검증 가능 조건 |
|----|------|----------------|
| **V-3** | 동일 입력 → 동일 `int[6]` 또는 동일 실패 코드 | |
| **V-1** | `isMagic` 판정 전 10개 선 전수 검사 | 부분 선만으로 통과 금지 |

**Magic Constant:** `M = 34` (= `n(n²+1)/2`, `n=4`).

**검사 선 집합 (고정):**

| 선 ID | 정의 |
|-------|------|
| R1~R4 | 행 `i` (i=1..4), 열 1~4 |
| C1~C4 | 열 `j` (j=1..4), 행 1~4 |
| D1 | (1,1)(2,2)(3,3)(4,4) |
| D2 | (1,4)(2,3)(3,2)(4,1) |

---

## 1.3 핵심 유스케이스(도메인 관점)

| UC-ID | 이름 | 전제 | 주요 단계 | 성공 | 실패 |
|-------|------|------|-----------|------|------|
| **UC-D01** | 빈칸 순서 확정 | P-1 | `EmptyCellLocator.locateOrdered(grid)` → `(cellA, cellB)` | 2개 좌표 | 빈칸 수 ≠ 2 |
| **UC-D02** | 누락 숫자 쌍 확정 | P-2,P-3,P-4 | `MissingNumberResolver.resolve(grid)` → `(n1,n2)`, `n1<n2` | 한 쌍 | 누락 수 ≠ 2 |
| **UC-D03** | 완성 마방진 판정 | 격자에 0 없음 | `MagicSquareValidator.validate(fullGrid)` | `VALID` / 위반 유형 | — |
| **UC-D04** | 배치 시도 A | UC-D01,D02 | 복사 격자에 `cellA=n1`, `cellB=n2` → UC-D03 | 마방진 | `NOT_MAGIC` |
| **UC-D05** | 배치 시도 B | UC-D04 실패 | `cellA=n2`, `cellB=n1` → UC-D03 | 마방진 | `NOT_MAGIC` |
| **UC-D06** | 퍼즐 해 반환 | UC-D04 또는 D05 성공 | `CompletionSolver`가 O-4/O-5에 따라 `int[6]` 구성 | `[r1,c1,n1,r2,c2,n2]` | `NO_VALID_COMPLETION` |

**도메인 시퀀스 (정상):**

```text
Grid(in) → [P-1..P-3 검증] → UC-D01 → UC-D02 → UC-D04 → (성공 시 종료)
                                              ↓ 실패
                                            UC-D05 → (성공 시 종료 / 실패 시 NO_VALID_COMPLETION)
```

---

## 1.4 Domain API(내부 계약)

> 시그니처는 의사 표기. **구현 코드 없음.**

### `EmptyCellLocator`

| 메서드 | 입력 | 출력 | 실패 조건 |
|--------|------|------|-----------|
| `locateOrdered(Grid g)` | `Grid` | `(Cell first, Cell second)` | `emptyCount != 2` → `INVALID_EMPTY_COUNT` |

### `MissingNumberResolver`

| 메서드 | 입력 | 출력 | 실패 조건 |
|--------|------|------|-----------|
| `resolve(Grid g)` | `Grid` | `(int n1, int n2)` with `n1<n2` | non-zero 중복 → `DUPLICATE_VALUE`; 범위 위반 → `OUT_OF_RANGE`; 누락 수 개수 ≠ 2 → `INVALID_MISSING_SET` |

### `MagicSquareValidator`

| 메서드 | 입력 | 출력 | 실패 조건 |
|--------|------|------|-----------|
| `validateComplete(Grid g)` | 0 없는 `Grid` | `ValidationResult { valid, violations[] }` | `valid=false` 시 `violations`에 `LINE_SUM`, `NUMBER_SET` 등 **최소 1개** |

### `CompletionSolver`

| 메서드 | 입력 | 출력 | 실패 조건 |
|--------|------|------|-----------|
| `solve(Grid g)` | P-1~P-3 만족 `Grid` | `SolveResult { int[6] solution }` | 전제 위반 시 locator/resolver 실패 전파; UC-D04·D05 모두 실패 → `NO_VALID_COMPLETION` |

### `Grid`

| 메서드 | 입력 | 출력 | 실패 조건 |
|--------|------|------|-----------|
| `fromIntMatrix(int[][] m)` | 4×4 | `Grid` | 행/열 ≠ 4 → `INVALID_DIMENSION` |
| `withCellFilled(Grid g, Cell c, int v)` | — | 새 `Grid` (불변) | `v` 범위 1~16 |

### Domain 실패 코드 (고정)

| 코드 | 의미 |
|------|------|
| `INVALID_DIMENSION` | 4×4 아님 |
| `INVALID_EMPTY_COUNT` | 빈칸 수 ≠ 2 |
| `OUT_OF_RANGE` | 0 외 값이 1~16 밖 |
| `DUPLICATE_VALUE` | 0 제외 중복 |
| `INVALID_MISSING_SET` | 누락 수 2개 아님 |
| `NO_VALID_COMPLETION` | 두 배치 모두 비마방진 |

---

## 1.5 Domain 단위 테스트 설계(RED 우선)

### 테스트 네이밍

`Domain_<클래스>_<행위>_<조건>_[INV-ID]`

### 정상 케이스

| Test-ID | 대상 | 입력 요약 | 기대 | 보호 Invariant |
|---------|------|-----------|------|----------------|
| **DT-001** | `CompletionSolver.solve` | 알려진 4×4, 빈칸 2개, 해 존재 | `int[6]` 길이 6; O-4 순서 | O-1~O-5, I-3 |
| **DT-002** | `CompletionSolver.solve` | 시도 A 실패·B 성공 fixture | `[r1,c1,n2,r2,c2,n1]` | O-5 |
| **DT-003** | `EmptyCellLocator` | 빈칸 (2,3),(4,1) | 첫=(2,3), 둘=(4,1) | O-1,O-2 |
| **DT-004** | `MissingNumberResolver` | 14개 수 고정 | `n1<n2`, 집합 P-4 | P-4 |
| **DT-005** | `MagicSquareValidator` | 완성 유효 마방진 | `valid=true` | I-2,I-3,V-1 |
| **DT-006** | `CompletionSolver.solve` | 동일 입력 2회 호출 | 바이트 동일 `int[6]` | V-3 |

### 비정상 케이스

| Test-ID | 대상 | 입력 요약 | 기대 실패 | 보호 Invariant |
|---------|------|-----------|-----------|----------------|
| **DT-101** | `Grid.fromIntMatrix` | 3×4 | `INVALID_DIMENSION` | I-1 |
| **DT-102** | `EmptyCellLocator` | 빈칸 1개 | `INVALID_EMPTY_COUNT` | P-1 |
| **DT-103** | `EmptyCellLocator` | 빈칸 3개 | `INVALID_EMPTY_COUNT` | P-1 |
| **DT-104** | `MissingNumberResolver` | non-zero 중복 7 | `DUPLICATE_VALUE` | P-3 |
| **DT-105** | `MissingNumberResolver` | 값 17 | `OUT_OF_RANGE` | P-2 |
| **DT-106** | `CompletionSolver.solve` | 두 배치 모두 비마방진 fixture | `NO_VALID_COMPLETION` | O-6 |
| **DT-107** | `MagicSquareValidator` | 합만 맞고 17 중복(완성 격자) | `valid=false`, `NUMBER_SET` | I-2 |

### 엣지 케이스

| Test-ID | 대상 | 입력 요약 | 기대 | 보호 Invariant |
|---------|------|-----------|------|----------------|
| **DT-201** | `EmptyCellLocator` | 빈칸 (1,1),(1,2) 인접 | 스캔 순서 (1,1)→(1,2) | O-1 |
| **DT-202** | `EmptyCellLocator` | 빈칸 (4,4),(3,4) | 행 우선: (3,4)가 첫 | O-1 |
| **DT-203** | `CompletionSolver` | `n1+1=n2` 연속 누락 수 | O-3 정렬 유지 | O-3 |
| **DT-204** | `LineSumCalculator` | 한 행 합 33 | `validateComplete` → `LINE_SUM` | I-3 |
| **DT-205** | `MagicSquareValidator` | 대각 1개만 틀림 | `violations`에 D1 또는 D2 | V-1 |

### RED 우선 순서 (Logic Track)

| 순서 | Test-ID | 이유 |
|------|---------|------|
| 1 | DT-003, DT-101~103 | 빈칸·크기 경계 고정 |
| 2 | DT-004, DT-104~105 | 누락 수·중복 |
| 3 | DT-005, DT-107, DT-204~205 | 마방진 판정 |
| 4 | DT-001, DT-002, DT-006 | Solver 통합 |
| 5 | DT-106 | 해 없음 |

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

| SCN-ID | 흐름 | 단계 |
|--------|------|------|
| **UI-S01** | 정상 해결 | (1) `int[4][4]` 입력 → (2) Boundary 검증 통과 → (3) Application/Domain `solve` → (4) `int[6]` 반환 |
| **UI-S02** | 구조 오류 | (1) 입력 → (2) Boundary 검증 실패 → (3) `ErrorSchema` 반환, Domain 미호출 |
| **UI-S03** | Domain 해 없음 | (1) 통과 → (2) Domain `NO_VALID_COMPLETION` → (3) 표준 에러 메시지 |
| **UI-S04** | 저장 후 재실행 | (1) Repository `load` → (2) UI-S01 → (3) 선택: `save` 결과 |

**Boundary 책임:** 형식·개수·범위·중복·출력 배열 길이·좌표 1-index 범위. **마방진 수학 판정은 Domain.**

---

## 2.2 UI 계약(외부 계약)

### Input schema

| 필드 | 타입 | 규칙 | 위반 코드 |
|------|------|------|-----------|
| `matrix` | `int[4][4]` | 필수 | `E_DIM_ROWS`, `E_DIM_COLS` |
| `matrix[r][c]` | `int` | `0` 또는 `1..16` | `E_CELL_RANGE` |
| 빈칸 | — | `count(0)==2` | `E_EMPTY_COUNT` |
| 중복 | — | 0 제외 유일 | `E_DUPLICATE` |

**검증 순서 (고정):**

1. `matrix == null` → `E_NULL_INPUT`
2. `matrix.length != 4` → `E_DIM_ROWS`
3. 각 행 `matrix[i].length != 4` → `E_DIM_COLS`
4. 셀 범위 → `E_CELL_RANGE`
5. 빈칸 개수 → `E_EMPTY_COUNT`
6. 중복 → `E_DUPLICATE`

### Output schema (성공)

| 필드 | 타입 | 규칙 |
|------|------|------|
| `result` | `int[6]` | `[r1,c1,n1,r2,c2,n2]` |
| `r1,c1,r2,c2` | `int` | 각 `1..4` |
| `n1,n2` | `int` | 각 `1..16`, `n1!=n2` |
| 의미 | — | Domain 반환값 **재정렬 금지** |

### Error schema

| 필드 | 타입 | 규칙 |
|------|------|------|
| `code` | `string` | 코드표 **대소문자 정확히** |
| `message` | `string` | §2.4 문구 **바이트 동일** |

| code | Domain 매핑 | Domain 호출 |
|------|-------------|---------------|
| `E_NULL_INPUT` | — | 없음 |
| `E_DIM_ROWS` | `INVALID_DIMENSION` | 없음 |
| `E_DIM_COLS` | `INVALID_DIMENSION` | 없음 |
| `E_CELL_RANGE` | `OUT_OF_RANGE` | 없음 |
| `E_EMPTY_COUNT` | `INVALID_EMPTY_COUNT` | 없음 |
| `E_DUPLICATE` | `DUPLICATE_VALUE` | 없음 |
| `E_NO_SOLUTION` | `NO_VALID_COMPLETION` | 있음 |
| `E_INTERNAL` | 미매핑 Domain 예외 | 있음 |

### Boundary Port

| 연산 | 입력 | 출력 |
|------|------|------|
| `solvePuzzle(int[][] matrix)` | Input schema | `Success(int[6])` \| `Error(code,message)` |

---

## 2.3 UI 레벨 테스트(Contract-first, RED 우선)

**전제:** `CompletionSolver`(또는 Application Port)는 **Mock**.

| Test-ID | 유형 | Mock 설정 | Boundary 입력 | 기대 |
|---------|------|-----------|---------------|------|
| **UT-001** | 정상 | `solve` → `[2,3,5,4,1,12]` | 유효 4×4 | 동일 `int[6]` |
| **UT-002** | 형식 | 미호출 | `null` | `E_NULL_INPUT` |
| **UT-003** | 형식 | 미호출 | 3×4 | `E_DIM_ROWS` |
| **UT-004** | 형식 | 미호출 | 한 행 길이 3 | `E_DIM_COLS` |
| **UT-005** | 형식 | 미호출 | 셀 17 | `E_CELL_RANGE` |
| **UT-006** | 형식 | 미호출 | 빈칸 1개 | `E_EMPTY_COUNT` |
| **UT-007** | 형식 | 미호출 | 빈칸 3개 | `E_EMPTY_COUNT` |
| **UT-008** | 형식 | 미호출 | non-zero 7 중복 | `E_DUPLICATE` |
| **UT-009** | Domain 실패 | `NO_VALID_COMPLETION` | 유효 형식 | `E_NO_SOLUTION` |
| **UT-010** | 반환 포맷 | `solve` → 6원소 | 유효 | `length==6` |
| **UT-011** | 좌표 가드 | Mock `r=0` | — | `E_INTERNAL` 또는 출력 가드 실패 |
| **UT-012** | 결정성 | Mock 고정 | 동일 입력 2회 | 동일 출력 |

**RED 우선 순서 (UI Track):** UT-002~008 → UT-001 → UT-009~012.

---

## 2.4 UX/출력 규칙

### 성공 출력 (텍스트 Boundary)

| 항목 | 규칙 |
|------|------|
| 형식 | `r1,c1,n1,r2,c2,n2` (쉼표 구분, 공백 없음) |
| 예시 | `2,3,5,4,1,12` |

### 에러 메시지 표준 (문구 고정)

| code | message (정확히 일치) |
|------|------------------------|
| `E_NULL_INPUT` | `입력 행렬이 null입니다.` |
| `E_DIM_ROWS` | `행 개수는 4여야 합니다.` |
| `E_DIM_COLS` | `각 행의 열 개수는 4여야 합니다.` |
| `E_CELL_RANGE` | `셀 값은 0 또는 1~16이어야 합니다.` |
| `E_EMPTY_COUNT` | `빈칸(0)은 정확히 2개여야 합니다.` |
| `E_DUPLICATE` | `0을 제외한 값은 중복될 수 없습니다.` |
| `E_NO_SOLUTION` | `두 빈칸을 채워도 마방진이 되지 않습니다.` |
| `E_INTERNAL` | `내부 오류가 발생했습니다.` |

### 에러 출력 형식

| 항목 | 규칙 |
|------|------|
| 형식 | `ERROR:<code>:<message>` |
| 예시 | `ERROR:E_EMPTY_COUNT:빈칸(0)은 정확히 2개여야 합니다.` |

---

# 3) Data Layer 설계

## 3.1 목적 정의

| 항목 | 내용 |
|------|------|
| **목적** | 퍼즐 입력·실행 결과 **세션 간 재현**; Repository로 Infrastructure 교체 연습 |
| **범위** | `int[4][4]` 저장·로드; (선택) 마지막 `int[6]` |
| **비범위** | RDBMS, 쿼리, 마이그레이션, 동시성, 암호화 |

---

## 3.2 인터페이스 계약

### `MatrixRepository` (Port)

| 메서드 | 입력 | 출력 | 실패 |
|--------|------|------|------|
| `save(String id, PersistedPuzzle record)` | `id` non-blank | `void` | `E_STORAGE_WRITE` |
| `load(String id)` | `id` | `PersistedPuzzle` | `E_STORAGE_NOT_FOUND`, `E_STORAGE_FORMAT` |
| `exists(String id)` | `id` | `boolean` | — |
| `delete(String id)` | `id` | `void` | `E_STORAGE_NOT_FOUND` (선택) |

### `PersistedPuzzle`

| 필드 | 타입 | 규칙 |
|------|------|------|
| `matrix` | `int[4][4]` | UI Input schema와 동일 |
| `lastResult` | `int[6]` \| null | 있으면 길이 6 |
| `savedAt` | ISO-8601 string | 선택 |

**의존성:** Domain은 `MatrixRepository`를 **참조하지 않음**.

---

## 3.3 구현 옵션 비교

| 기준 | 옵션 A: InMemory | 옵션 B: File (JSON) |
|------|------------------|---------------------|
| 저장소 | `Map<String,PersistedPuzzle>` | `{baseDir}/{id}.json` |
| 재시작 후 | 소실 | 유지 |
| 테스트 속도 | 빠름 | I/O 느림 |

**추천: 옵션 A (InMemory) 1차, 옵션 B 2차 Epic**

- TDD 목표가 **레이어 분리**에 있음
- File은 동일 Port로 교체 후 Integration 1건 추가

---

## 3.4 Data 레이어 테스트

| Test-ID | 대상 | 시나리오 | 기대 |
|---------|------|----------|------|
| **ST-001** | InMemory | `save`→`load` | `matrix` 동일 |
| **ST-002** | `load` | 없는 `id` | `E_STORAGE_NOT_FOUND` |
| **ST-003** | `save` | `id=""` | `E_INVALID_ID` |
| **ST-004** | File | 잘못된 JSON | `E_STORAGE_FORMAT` |
| **ST-005** | `save` | `lastResult` 길이 7 | `E_INVALID_RECORD` |
| **ST-006** | `load` | 빈칸 수 | 저장 시점과 동일 2개 |
| **ST-007** | `exists` | 저장 전/후 | `false`→`true` |

---

# 4) Integration & Verification

## 4.1 통합 경로 정의

```text
[ Caller ]
    ↓
[ PuzzleBoundary ]  ← UI Track
    ↓
[ SolvePuzzleUseCase ]  ← Application (선택)
    ↓
[ CompletionSolver + Domain Services ]  ← Logic Track
    ↑ (no dependency)
[ MatrixRepository Port ]
    ↑ implements
[ InMemoryMatrixRepository | FileMatrixRepository ]
```

**경로 A (필수):** `PuzzleBoundary` → `SolvePuzzleUseCase` → `CompletionSolver`

**경로 B (선택):** `load` → solve → `save`

---

## 4.2 통합 테스트 시나리오

### 정상 (≥2)

| IT-ID | 경로 | 기대 |
|-------|------|------|
| **IT-001** | A | fixture 해 존재, 시도 A 성공 → golden `int[6]` |
| **IT-002** | A | 시도 A 실패·B 성공 → 스왑된 6-tuple |
| **IT-003** | B | save→load→solve = IT-001 동일 |

### 실패 (≥3)

| IT-ID | 경로 | 기대 |
|-------|------|------|
| **IT-101** | A | 빈칸 3개 → `ERROR:E_EMPTY_COUNT:...` |
| **IT-102** | A | 해 불가능 → `ERROR:E_NO_SOLUTION:...` |
| **IT-103** | B | 없는 id → `ERROR:E_STORAGE_NOT_FOUND:저장된 퍼즐을 찾을 수 없습니다.` |
| **IT-104** | B | JSON 깨짐 → `E_STORAGE_FORMAT` |
| **IT-105** | A | 5×5 → `E_DIM_ROWS` |

---

## 4.3 회귀 보호 규칙

| 규칙 ID | 내용 |
|---------|------|
| **RG-01** | UI schema 변경 시 UT-* 전부 선행 수정 |
| **RG-02** | `int[6]` 순서·1-index 변경 금지 |
| **RG-03** | 에러 `message` 문구 변경 금지 (버전 bump 시만) |
| **RG-04** | Domain 실패 코드 enum 삭제·이름 변경 금지 |
| **RG-05** | 기존 테스트 삭제 금지 |
| **RG-06** | Refactor 브랜치는 테스트 추가/삭제 없이 Green 유지 |

---

## 4.4 커버리지 목표

| Component | 목표 | 측정 범위 |
|-----------|------|-----------|
| Domain Logic | **≥ 95%** line | Solver, Validator, Locator, Resolver |
| UI Boundary | **≥ 85%** line | `PuzzleBoundary`, validation chain |
| Data | **≥ 80%** line | `InMemoryMatrixRepository` (+ File Epic) |

---

## 4.5 Traceability Matrix

| Concept | Rule | Use Case | Contract | Test | Component |
|---------|------|----------|----------|------|-----------|
| I-1 | 4×4 only | UC-D01~D06 | Input schema | DT-101, UT-003~004, IT-105 | `Grid`, `PuzzleBoundary` |
| I-2 | 1~16 순열 | UC-D03 | `validateComplete` | DT-005, DT-107 | `MagicSquareValidator` |
| I-3 | 10 lines = 34 | UC-D03~D05 | `MagicConstant` | DT-204~205, DT-001 | `MagicSquareValidator` |
| P-1 | 2 zeros | UC-D01 | `E_EMPTY_COUNT` | DT-102~103, UT-006~007 | `EmptyCellLocator` |
| P-2 | 0 or 1~16 | UC-D02 | `E_CELL_RANGE` | DT-105, UT-005 | `PuzzleBoundary` |
| P-3 | No dup | UC-D02 | `E_DUPLICATE` | DT-104, UT-008 | `MissingNumberResolver` |
| O-1~O-5 | Scan & assign | UC-D04~D06 | `int[6]` | DT-001~002, IT-001~002 | `CompletionSolver` |
| O-6 | No solution | UC-D05 | `E_NO_SOLUTION` | DT-106, IT-102 | `CompletionSolver` |
| V-3 | Deterministic | UC-D06 | Same in→out | DT-006, UT-012 | `CompletionSolver` |
| Storage | Matrix unchanged | load | `PersistedPuzzle` | ST-001, IT-003 | `MatrixRepository` |

---

## 부록 A — Dual-Track · 브랜치 정렬

| 브랜치 | Logic Track | UI Track | Data Track |
|--------|-------------|----------|------------|
| **spec** | §1.4 API, §1.5 | §2.2~2.4, UT 목록 | §3.2~3.4 |
| **red** | DT-001,003,101~105 | UT-002~008 | ST-002~004 |
| **green** | DT-001,005 | UT-001 | ST-001 |
| **refactor** | 커버리지 95% | RG-03, 85% | Port 추출 |

---

## 부록 B — 기존 문제 정의와의 관계

| 항목 | 본 설계 | `01_Problem_Definition_Report` |
|------|---------|--------------------------------|
| 초점 | 빈칸 2개 채우기 + `int[6]` | 일반 판정·피드백 |
| 공통 | I-1~I-3, 합 34, 1~16 | 동일 불변 재사용 |
| 차이 | V-4 미완성 일반 케이스 **배제** | 빈칸 수 가변 |

---

*본 보고서는 Dual-Track TDD · Clean Architecture 설계 산출물이며, 구현 코드를 포함하지 않는다.*
