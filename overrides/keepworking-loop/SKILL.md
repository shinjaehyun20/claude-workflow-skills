---
name: keepworking-loop
description: >
  Turn a concrete task into a bounded execution loop: lock the goal, act, verify,
  repair failures, re-verify, and report evidence. Use when the user asks to
  finish, continue, fix, verify, or stop giving plans and execute.
user-invocable: true
argument-hint: "[task and expected finished state]"
metadata:
  version: "0.1.0"
  author: "Jaehyun Shin"
  license: "MIT"
  dependencies: "none"
---

# Keep Working Loop

Use this skill to finish one bounded action unit with evidence. It is not a request to run forever: it means make the smallest useful change, prove its result, repair the observed failure if needed, and stop at the stated close gate.

## 언제 사용하면 좋은가

- 사용자가 실행·수정·검증까지 끝내라고 요청할 때
- 구현이나 설정 변경 뒤 실제 동작을 확인해야 할 때
- 테스트 또는 검증에서 실패가 나와 최소 수리가 필요할 때
- 조사 결과를 적용 가능한 산출물로 이어가야 할 때
- 작업이 계획·상태 보고에서 멈추지 않아야 할 때

대표 호출 예시:

- `이 기능을 끝까지 구현하고 검증해줘`
- `테스트가 깨졌으니 고치고 다시 확인해줘`
- `계속 작업해서 완료 조건을 충족해줘`
- `계획 말고 실제로 적용해줘`
- `이 변경이 동작하는지 확인하고 문제면 수리해줘`

## 사용하지 않는 경우

- 사용자가 질문·아이디어·설계·검토만 명시했을 때
- 대상 시스템, 승인 범위, 또는 완료 조건이 없어 안전한 실행 단위를 정할 수 없을 때
- 삭제, 결제, 공개 게시, 권한 변경, 비밀정보 입력처럼 별도 승인이 필요한 작업일 때
- 외부 시스템의 성공 여부를 현재 권한으로 검증할 수 없는데 추측으로 완료를 선언해야 할 때

## 다른 스킬과의 구분

`keepworking-loop`은 일반적인 계획 작성, 단일 테스트 실행, 또는 단순 상태 보고용 스킬이 아니다. 이 스킬은 하나의 bounded action unit에서 **실행 결과를 verifier로 확인하고, 관찰된 실패만 최소 수리한 뒤 같은 verifier로 재확인**해야 할 때 사용한다. 기존 프로젝트에 같은 이름의 운영 스킬이 있다면 설치하지 말고 이 패키지를 `keepworking-loop` 이름으로 명시 호출한다.

## 입력

필수 입력:

1. 해결할 작업 또는 결함
2. 관찰 가능한 완료 조건
3. 수정 가능한 대상 또는 실행 권한

선택 입력:

- 정본 파일·URL·로그·테스트 명령
- 제외 범위와 위험 경계
- 검증기 또는 예상 결과
- 사용자 승인 없이 수행하면 안 되는 작업

입력이 부족하면 추측으로 채우지 않는다. 읽을 수 있는 정본과 현재 상태를 먼저 확인하고, 결과를 바꾸는 정보만 짧게 요청한다.

## 산출물

완료 보고에는 다음을 남긴다.

```text
- 완료한 action unit
- 변경 또는 실행한 대상
- verifier와 실제 결과
- 수리한 failure signature (있다면)
- 남은 위험, 승인 필요 항목, 또는 접근 제한
```

파일을 만들거나 바꾼 경우에는 정확한 경로와 검증 명령을 포함한다. 외부 반영은 실제 read-back이 없으면 완료로 표현하지 않는다.

## 워크플로우

### Step 1. 목표와 close gate 잠금

한 문장으로 다음을 정한다.

```text
goal -> scope -> expected finished state -> verifier
```

완료 조건은 "좋아 보임"이 아니라 테스트 통과, 생성물 존재, 응답 값, 렌더 확인, 또는 사용자가 승인한 관찰 가능한 상태여야 한다.

### Step 2. 정본과 현재 상태 확인

- 대상 파일, 서비스, 로그, 또는 사용자가 준 링크를 먼저 읽는다.
- 기존 구현·테스트·문서·명령을 찾아 재사용 가능 여부를 확인한다.
- 수정 대상과 검증 대상이 같은 정본을 가리키는지 확인한다.
- 알 수 없는 사실은 가정하지 않는다.

### Step 3. 가장 작은 실행 단위 수행

- 작업을 simple, medium, complex로 나눈다.
- simple 또는 medium은 local bounded loop로 바로 처리한다.
- complex 작업은 독립적인 부분만 분리하고, 최종 수락과 검증은 한 곳에서 수행한다.
- 사용자 승인 경계를 넘는 외부 전송, 삭제, 공개, 권한 변경은 실행하지 않는다.

### Step 4. 즉시 검증

가장 약한 검증부터 시작하지 않는다. 가능한 경우 실제 동작에 가까운 verifier를 우선한다.

```text
build or syntax check -> focused test -> integration or runtime check -> read-back
```

검증 결과와 failure signature를 기록한다. 실행했다는 사실은 성공 증거가 아니다.

### Step 5. repair -> re-verify

검증이 실패하면 다음 순서로 진행한다.

1. 실패 메시지와 재현 조건을 고정한다.
2. 가장 작은 원인 가설을 세운다.
3. 그 가설에 필요한 최소 수리만 적용한다.
4. 같은 verifier 또는 더 강한 verifier를 다시 실행한다.
5. 같은 실패를 반복하면 범위를 넓히거나 사용자 승인·입력을 요청한다.

### Step 6. close gate

다음이 모두 충족될 때만 action unit을 닫는다.

- 완료 조건이 충족됨
- verifier 결과가 있음
- 대상 정본이 맞음
- 외부 반영 여부가 실제 read-back으로 구분됨
- 남은 위험과 미수행 범위가 명시됨

## 실패와 복구

| 실패 신호 | 최소 복구 |
|---|---|
| 대상이나 정본이 불명확함 | 읽을 수 있는 원본을 먼저 확인하고 결정적인 정보만 요청한다 |
| 테스트가 실패함 | 실패 메시지를 고정하고 최소 변경 후 같은 테스트를 재실행한다 |
| 변경은 했지만 실제 동작이 불명확함 | 더 강한 runtime, integration, render, 또는 read-back 검증으로 올린다 |
| 권한 또는 승인 경계에 막힘 | 막힌 action과 가능한 읽기·검증을 분리하고 승인 필요 항목만 보고한다 |
| 같은 수리가 반복 실패함 | 원인 범위를 재분류하고 새로운 증거 없이 같은 변경을 반복하지 않는다 |
| 외부 반영을 확인할 수 없음 | `staged` 또는 `applied`로만 표현하고 `verified`로 과장하지 않는다 |

## Anti-rationalization

- 계획을 많이 썼다고 실행이 완료된 것은 아니다.
- 명령이 종료됐다고 요구사항이 충족된 것은 아니다.
- 한 번의 실패 원인 추측으로 여러 파일을 바꾸지 않는다.
- 정적 검사만 통과했다고 runtime 동작을 주장하지 않는다.
- 다른 작업의 성공 증거를 현재 대상의 완료 증거로 재사용하지 않는다.
- 불확실한 외부 반영을 성공으로 표현하지 않는다.
- 사용자의 승인 경계를 속도 때문에 우회하지 않는다.
