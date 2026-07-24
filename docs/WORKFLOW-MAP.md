# Workflow Map

## Repository 흐름: multi-skill catalog, standalone first

```text
Claude 원본 스킬(read-only)
  → 직접 제작 근거 확인
  → 반복 가능성·독립 trigger 판정
  → release_batch 1~2개 선택
  → portable override
  → skills/<skill-name> 누적
  → registry·카탈로그 갱신
  → 스킬별 사용 가이드·fixture
  → 정적 검증
  → Claude Code behavior smoke
  → public GitHub push·fresh clone 검증
```

직접 제작 여부, 범용화 승인, 전체 배포 목록의 정본은 `config/skill-registry.json`입니다. `config/selection.json`은 현재 release batch만 나타냅니다. 외부·adapted·forked·출처 미확정 스킬은 이 흐름에 진입하지 않습니다.

## 현재 카탈로그 예시: session-to-skill

```text
입력
  ├─ 현재 대화 또는 transcript
  ├─ 원하는 작업 범위
  └─ 선택: 이름, 설치 범위, 검증 로그

처리
  ├─ 트리거·목적 추출
  ├─ 도구·단계·산출물 추출
  ├─ 실패·수리·검증 추출
  ├─ 기존 스킬 중복 확인
  └─ 개인정보·환경 의존성 제거

출력
  ├─ SKILL.md
  ├─ 사용 가이드
  ├─ 선택: references/scripts
  └─ 검증 결과
```

## 플러그인 승격 조건

관련 스킬이 각자 아래 게이트를 통과한 뒤에만 묶습니다.

- standalone 설치 가능
- 자연어·명시 호출 가능
- fixture 행동 smoke 통과
- 입력·산출물 handoff 명시
- 단독 사용과 묶음 사용의 차이 문서화
- plugin 설치·업데이트·제거 별도 검증

현재 plugin count는 0입니다.
