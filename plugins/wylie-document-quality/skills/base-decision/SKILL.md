---
name: base-decision
description: 문서 작업의 기준 파일을 송부본, 공식 템플릿, 승인된 최신본 순으로 판정하고 임시본 사용을 차단하는 스킬.
---

# Base Decision

## 우선순위

1. 발주처·고객이 제공한 원본
2. 공식 양식 또는 승인된 템플릿
3. 승인된 최신 정본
4. 그 밖의 파일은 사용자 확인 후 사용

## 절차

1. 후보 파일을 전수 목록화한다.
2. 각 후보의 경로, 수정 시각, 버전 표기, 크기, SHA-256을 기록한다.
3. 작업본·임시본·추출본·변환본을 제외한다.
4. 문서 번호, 버전, 시트/슬라이드/섹션 수, ID 체계를 비교한다.
5. 선택 근거를 `base-decision.md`에 남긴다.
6. 원본은 읽기 전용으로 유지하고 별도 작업본을 만든다.

## 출력 형식

```markdown
# Base Decision
- selected: <portable path>
- class: supplied | official-template | approved-canonical
- version: <value or unknown>
- sha256: <hash>
- rejected candidates: <reason>
- approved mutation scope: <scope>
```

## 차단 조건

- 기준 파일을 특정할 수 없음
- 임시본 외 후보가 없음
- 버전 또는 문서 번호 충돌이 해결되지 않음
- 원본 직접 수정이 요구되지만 명시적 승인이 없음
