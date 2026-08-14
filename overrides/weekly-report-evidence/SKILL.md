---
name: weekly-report-evidence
description: >
  Build an evidence-backed weekly report from the prior plan and current work
  records. Use when a user asks for a weekly report, status summary, or
  next-week plan that must separate verified facts from unknowns.
user-invocable: true
argument-hint: "[reporting period, sources, and intended audience]"
metadata:
  version: "0.1.0"
  author: "Jaehyun Shin"
  license: "MIT"
  dependencies: "none"
---

# Evidence-Backed Weekly Report

Use this skill to produce one bounded weekly-report package from evidence, not recollection. It locks the reporting period, records source coverage, reconciles the prior plan, drafts only supported statements, and verifies the saved deliverable.

## 언제 사용하면 좋은가

- `이번 주 업무를 근거와 함께 주간보고로 정리해줘`
- `지난주 계획과 실제 결과를 대조해서 보고서를 작성해줘`
- `업무 로그를 읽고 다음 주 계획까지 정리해줘`
- `상태 보고를 만들어줘. 확인되지 않은 내용은 구분해줘`
- `주간 회고를 보고서 형식으로 작성하고 저장 전 검수해줘`

## 사용하지 않는 경우

- 사용자가 단순한 메모 요약이나 아이디어 목록만 원할 때
- 보고 기간, 원본 기록, 또는 대상 독자가 전혀 없어 사실 검증이 불가능할 때
- 확인되지 않은 성과를 확정 표현으로 바꿔 달라는 요청일 때
- 외부 시스템에 게시, 전송, 또는 승인하는 행위가 별도로 필요한 때

## 입력

필수 입력:

1. 보고 기간과 시간대
2. 하나 이상의 원본 기록 또는 접근 가능한 source location
3. 전달 대상 또는 원하는 보고 형식

선택 입력:

- 직전 주간보고와 다음 주 계획
- 프로젝트 명칭, 상태, 담당 범위
- 저장 경로와 파일명 규칙
- 제외 프로젝트, 민감정보 처리 규칙, 승인 경계
- 특정 수치, 일정, 또는 의사결정의 정본 링크

입력이 부족하면 기억으로 채우지 않는다. 읽을 수 있는 원본을 먼저 확인하고, 결과가 달라지는 정보만 요청한다.

## 산출물

기본 산출물은 다음을 포함한다.

```text
- source coverage ledger
- prior-plan reconciliation table
- weekly report draft
- open questions and evidence gaps
- validation result and saved-file read-back
```

최종 보고서는 일반적으로 다음 순서를 사용한다.

1. 이번 주 주요 업무
2. 다음 주 계획
3. 성과 또는 확인된 변화
4. 이슈와 의존성
5. 제안 또는 결정 필요 사항
6. 비고

조직의 기존 양식이 있으면 그것을 우선한다. 내부 ledger와 원본 경로는 최종 보고서에 자동 노출하지 않는다.

## 워크플로우

### Step 1. 기간과 close gate 고정

다음을 한 문장으로 잠근다.

```text
reporting period -> included sources -> audience -> saved deliverable -> verifier
```

완료는 "그럴듯한 초안"이 아니다. 필수 섹션, 근거 상태, 직전 계획 대조, 저장 read-back이 확인되어야 한다.

### Step 2. source coverage ledger 작성

각 source를 `collected`, `empty`, `unavailable`, `failed`, `not_applicable` 중 하나로 기록한다.

- 직전 보고서 또는 직전 계획
- 기간 내 업무 로그와 회의 기록
- 승인된 업무 메시지 또는 결정 기록
- 산출물 변경 이력이나 버전 기록
- 필요한 경우 일정 또는 메일 기록

source가 비어 있거나 접근 불가한 것은 업무가 없었다는 뜻이 아니다. coverage gap으로 남긴다.

### Step 3. 직전 계획 대조

직전 보고서의 계획을 하나도 빼지 않고 아래 상태로 분류한다.

| 이전 계획 | 현재 근거 | 상태 | 이번 보고서 위치 |
| --- | --- | --- | --- |
| 원문 계획 | source와 날짜 | 완료 / 진행 / 미착수 / 확인 필요 | 섹션과 task |

새 항목은 현재 기간의 근거가 있을 때만 추가한다. 완료된 항목을 자동으로 다음 주 계획으로 이월하지 않는다.

### Step 4. 귀속과 사실 확인

산출물 존재와 사람의 업무 수행을 구분한다.

- 사람의 지시, 검토, 판단, 수정, 승인, 공유처럼 근거가 있는 행동만 개인 업무로 쓴다.
- 자동 생성물, 타인의 작업, 미확정 제안은 검증 없이 개인 성과로 바꾸지 않는다.
- 수치, 수신자, 일정, 완료 상태는 원본에서 확인한다.
- 근거가 부족하면 완료로 쓰지 말고 `확인 필요` 또는 open question으로 남긴다.

### Step 5. 보고서 작성

대상 조직의 직전 등록본 또는 합의된 template를 우선한다.

- task 제목에는 구체 작업물과 실제 조치를 쓴다.
- 첫 줄에는 업무 객체와 확인 결과를 바로 쓴다.
- 추상적인 미사여구보다 짧은 업무 언어를 쓴다.
- 성과, 제안, 이슈를 채우기 위해 사실을 만들지 않는다.
- 진행 중인 task에는 다음 확인 조건이나 목표일을 붙인다.

### Step 6. 검수와 저장

저장 전에 다음을 확인한다.

1. 필수 섹션과 기간이 존재한다.
2. 날짜와 요일, 수치, 프로젝트 상태가 source와 일치한다.
3. 이전 계획의 모든 항목이 대조표에 있다.
4. 타인 업무, 추측한 수신자, 확정되지 않은 결론이 없다.
5. 최종 보고서에 내부 ledger, 경로, 도구 운영어, 자격증명이 없다.
6. 저장 후 파일 존재, 핵심 헤딩, 읽기 가능 여부를 재확인한다.

## 실패와 복구

| 실패 신호 | 최소 복구 |
| --- | --- |
| 직전 계획을 찾을 수 없음 | 보고서 형식은 유지하되 연속성 gap을 명시하고 현재 source만으로 작성 |
| source가 비어 있거나 접근 불가 | 활동 없음으로 단정하지 말고 coverage ledger에 gap으로 기록 |
| 수치나 완료 상태가 충돌 | 더 가까운 원본과 날짜를 확인하고, 해결 전에는 확정 표현을 제거 |
| 개인 성과 귀속이 불명확 | 해당 항목을 보류하거나 확인된 검토·결정 범위로 축소 |
| 저장 검증이 실패 | failure signature를 고정하고 경로·형식·권한 중 최소 원인을 수리한 뒤 다시 읽기 |
| 웹 게시 또는 전송이 필요함 | 로컬 보고서 준비와 외부 반영을 분리하고, 명시 승인과 read-back 전에는 게시 완료로 표현하지 않음 |

## Anti-rationalization

- 최근 대화 요약은 원본 기록을 대체하지 않는다.
- source 하나가 비었다고 그 기간의 업무가 없었다고 결론내리지 않는다.
- 파일 수정시각만으로 누가 업무를 수행했는지 추정하지 않는다.
- AI 또는 자동화가 만든 초안을 개인 성과로 바꾸지 않는다.
- 검증되지 않은 수치를 보기 좋게 반올림하거나 보완하지 않는다.
- 빈 성과·제안 섹션을 그럴듯한 문장으로 채우지 않는다.
- 파일을 저장했다는 사실만으로 외부 전송·게시·승인이 끝났다고 말하지 않는다.
