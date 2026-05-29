# Export Transcript (Conversational Prompt)

## Session Theme
Custom Cursor agent markdown generation for multiple specialist roles.

## Dialogue Transcript

**User:** `.cursor/agents/code-reviewer.md` 파일 생성 요청.  
YAML frontmatter(`name`, `description`, `model: inherit`, `readonly: true`) + 코드 리뷰 지침 본문 작성.

**Assistant:** `code-reviewer.md` 생성, 요청한 frontmatter와 코드 리뷰 원칙/점검 항목/코멘트 방식 반영.

---

**User:** System Optimization Engineer Agent 파일 생성 요청.  
이름 예시 `system-optimization-engineer`, 역할/책임/작업 방식/금지/출력 형식 제공.

**Assistant:** `system-optimization-engineer.md` 생성, 제공된 프롬프트 구조 그대로 반영.

---

**User:** User Experience Expert Agent 파일 생성 요청.  
이름 예시 `ux-design-advisor`, UX 역할/책임/작업 방식/금지/출력 형식 제공.

**Assistant:** `ux-design-advisor.md` 생성, 지시한 섹션 구성으로 반영.

---

**User:** Product Planning Manager Agent 파일 생성 요청.  
이름 예시 `product-planning-manager`, PRD 중심 출력 형식 포함.

**Assistant:** `product-planning-manager.md` 생성, PRD 1~10 섹션 구조 반영.

---

**User:** Backend Developer Agent 파일 생성 요청.  
이름 예시 `backend-developer`, API/보안/테스트/리스크 출력 형식 포함.

**Assistant:** `backend-developer.md` 생성, 백엔드 구현형 역할에 맞는 지침 반영.

---

**User:** Frontend Developer Agent 파일 생성 요청.  
이름 예시 `frontend-developer`, UI 흐름/접근성/브라우저 확인 포함.

**Assistant:** `frontend-developer.md` 생성, 프론트엔드 역할 지침 반영.

---

**User:** Quality Assurance Engineer Agent 파일 생성 요청.  
이름 예시 `quality-assurance-engineer`, QA 리포트 출력 형식 포함.

**Assistant:** `quality-assurance-engineer.md` 생성, 테스트 범위/통과·실패/버그/권고안 구조 반영.

---

**User:** AI Integration Expert Agent 파일 생성 요청.  
이름 예시 `ai-integration-expert`, OpenRouter + DeepSeek 특수 역할 포함.

**Assistant:** `ai-integration-expert.md` 생성, API 보안/오류 처리/rate limit/검증 후처리 반영.

---

**User (current):**  
1) `Report` 폴더에 보고서 생성  
2) 현재까지 프롬프트 전체를 대화형 프롬프트로 `Prompt` 폴더에 export transcript  
파일명은 `05_`로 시작

**Assistant:**  
요청 순서에 맞게 `Report`와 `Prompt`에 `05_` 접두어 파일 생성 완료.

## Export Metadata

- Export Type: Conversational prompt transcript
- Filename Prefix Rule: `05_` applied
- Export Date: 2026-05-28
