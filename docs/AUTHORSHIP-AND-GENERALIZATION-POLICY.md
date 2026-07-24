# Authorship and Generalization Policy

## 배포 대상

이 저장소에는 **저장소 소유자가 직접 제작했다고 확인한 Claude Code 스킬만** 올립니다.

- 허용: `owner-authored`
- 제외: third-party, adapted, forked, unknown
- Claude 사용자 영역에 설치되어 있다는 사실만으로 직접 제작한 스킬로 판정하지 않음
- 작성자 근거가 불명확하면 release selection에 넣지 않음

전체 누적 배포 카탈로그의 정본은 `config/skill-registry.json`입니다. `config/selection.json`의 `release_batch`는 이번에 갱신할 스킬만 가리키며, 모든 항목은 registry gate를 통과해야 합니다.

## 범용화 게이트

직접 제작한 스킬이라도 개인 환경 그대로 배포하지 않습니다. 다음 조건을 모두 충족해야 `generalized`로 승인합니다.

1. 개인명, 고객명, 개인 절대경로, 인증정보를 제거하거나 변수화
2. 특정 프로젝트의 일회성 절차를 재사용 가능한 trigger와 입력 계약으로 변환
3. 특정 런타임의 비공개 hook·MCP·조직 전용 에이전트에 대한 강제 의존 제거
4. 입력, 산출물, 의존성, 실패·복구, 검증 방법 명시
5. 독립 fixture에서 원본 데이터를 변경하지 않는 저위험 smoke 통과

## 정본 흐름

```text
candidate
  → owner-authored 확인
  → 반복 가능성·독립 trigger 판정
  → generalized override 작성
  → standalone package 생성
  → static validation
  → Claude Code behavior smoke
  → public-ready publish
  → 관련 standalone 누적 후 plugin eligibility 검토
```

### 상태 정의

- `candidate`: 직접 제작 여부와 재사용성을 아직 확인하지 않음
- `authorship-confirmed`: 직접 제작 근거 확인
- `generalization-ready`: 범용 override와 사용 계약 완료
- `standalone-verified`: 정적 검사와 실제 behavior smoke 통과
- `public-ready`: 공개 배포용 문서·라이선스·검증 통과
- `plugin-eligible`: 관련 standalone 간 handoff와 plugin smoke까지 통과

상태를 건너뛰지 않습니다. 외부 스킬을 참고해 새로 작성한 경우에도 원본과 실질적으로 같은 adapted/forked 산출물이면 이 저장소의 배포 대상이 아닙니다.

## 스킬화와 플로우 정본화 판정

- 독립 trigger, 입력, 산출물, verifier가 안정적이면 **standalone skill**로 승격
- 여러 스킬이 순서대로 handoff하지만 각각 단독 가치가 있으면 **workflow 문서 + 선택적 plugin**으로 정본화
- 단순 체크리스트이거나 독립 호출 가치가 없으면 새 스킬을 만들지 않고 기존 스킬의 `references/` 또는 workflow 문서로 유지
- 같은 목적의 스킬이 이미 있으면 새 이름을 만들지 않고 기존 정본에 병합

## 검증 계약

`tools/import_and_analyze.py`와 `tools/validate_repo.py`는 다음을 차단합니다.

- registry에 없는 release selection
- `owner-authored`가 아닌 스킬
- `generalized`가 아닌 스킬
- `publication_eligible`이 true가 아닌 스킬

이 gate는 문서 선언이 아니라 importer 실행 이전의 강제 조건입니다.

Importer는 `release_batch`만 새로 복제·갱신하고, registry에서 `publication_eligible: true`인 기존 배포 스킬과 provenance manifest는 보존합니다. 따라서 새 release가 이전 스킬을 교체하지 않고 같은 repository에 누적됩니다.