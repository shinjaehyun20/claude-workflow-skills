# Workflow Map

## 1. UX planning

```text
project evidence
  └─ public-portal-benchmark
       output: benchmark-report.md
       └─ asis-tobe-analysis
            output: tobe-analysis-report.md, screen-requirements.md
            └─ wireframe-composer
                 output: screen-list.md, interaction-map.md, wireframes
                 └─ design-spec-review
                      output: design-review-report, review-ledger
```

### Handoff contract

- Benchmark → TO-BE: URL, 확인일, 비교표, 시사점 ID
- TO-BE → Wireframe: 문제 ID, 개선 ID, 화면 ID, 수용 기준
- Wireframe → Design review: 기준 버전, 화면 목록, 상태·인터랙션, 렌더

## 2. Document quality

```text
supplied-scan
  └─ supplied-immutability
       └─ base-decision
            └─ artifact-style
                 └─ gate-check
```

각 단계는 이전 단계의 evidence를 입력으로 받는다. `gate-check`는 앞 단계 누락을 자동으로 면책하지 않는다.

## 3. Project operations

- `wylie-folder-organizer`: 문서 구조를 분석하고 dry-run 분류를 만든다.
- `proposal-review`: RFP와 제안서를 심사위원 관점으로 검토한다.

두 스킬은 같은 플러그인에 있지만 자동 연쇄하지 않는다. 파일 정리가 제안서 평가의 선행 조건은 아니기 때문이다.

## Excluded boundary

내부 runtime 소유권과 미완료 자동화를 포함한 delivery-lifecycle은 범용화가 끝날 때까지 v0.1에서 제외한다. 공개 가능한 계약은 입력·산출·게이트가 독립적으로 검증될 때만 추가한다.
