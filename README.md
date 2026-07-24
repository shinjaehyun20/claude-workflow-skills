# Wylie Claude Workflow Skills

> 저장소 소유자가 **직접 제작했다고 확인한** Claude Code 스킬만 범용화해 하루 1~2개씩 독립 검증하고, 함께 쓰는 스킬만 나중에 플러그인으로 묶는 private 저장소입니다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-standalone%20skills-6B5CE7)](https://docs.anthropic.com/en/docs/claude-code)
[![Skills](https://img.shields.io/badge/validated%20skills-1-00A86B)](#현재-스킬)
[![Plugins](https://img.shields.io/badge/plugins-deferred-lightgrey)](#플러그인-원칙)
[![Validation](https://img.shields.io/badge/validation-local%20%2B%20CI-00A86B)](tools/validate_repo.py)

![하루 한두 개씩 검증하는 Claude Code 스킬 저장소](docs/assets/hero.svg)

## 현재 스킬

### [`session-to-skill`](skills/session-to-skill/)

대화에서 실제로 성공하고 검증된 절차를 추출해 재사용 가능한 `SKILL.md`로 만듭니다.

**언제 좋은가**

- 긴 세션의 시행착오와 해결 절차를 재사용하고 싶을 때
- 팀원이 같은 입력·산출물·검증 순서를 따라야 할 때
- 반복 업무를 새 Claude Code 스킬로 승격할 때

**호출 예시**

```text
이 세션을 스킬로 만들어줘.
```

```text
/session-to-skill 현재 세션의 검증·복구 워크플로우
```

자세한 사용법, 비사용 시점, 입력·출력, 실패 복구는 [스킬별 사용 가이드](skills/session-to-skill/README.md)를 참고하세요.

## 설치

저장소를 clone한 뒤 필요한 스킬 하나만 복사합니다.

### 프로젝트 전용 설치

```bash
mkdir -p .claude/skills
cp -R <repo>/skills/session-to-skill .claude/skills/
```

### 사용자 전역 설치

```bash
mkdir -p ~/.claude/skills
cp -R <repo>/skills/session-to-skill ~/.claude/skills/
```

사용자 전역 설치는 기존 동일 이름 스킬을 확인한 뒤 진행하세요. 자세한 내용은 [설치 가이드](docs/INSTALLATION.md)에 있습니다.

## 스킬 우선 배포 원칙

```text
원본 인벤토리
  → 직접 제작 근거 확인
  → 오늘의 스킬 1~2개 선택
  → 읽기 전용 복제
  → 비식별화·범용화·플로우 정본화
  → 스킬별 사용 가이드
  → 구조 검증
  → 실제 Claude Code 저위험 smoke
  → private push
```

현재 원본 top-level 스킬은 298개지만, 이는 직접 제작 수가 아니라 설치된 사용자 영역의 전체 수입니다. `config/skill-registry.json`에서 `owner-authored`로 확인되고 범용화 gate를 통과한 스킬만 선택합니다. 현재 배포 대상은 `session-to-skill` 1개입니다.

자세한 기준과 정본 흐름은 [직접 제작·범용화 정책](docs/AUTHORSHIP-AND-GENERALIZATION-POLICY.md)을 참고하세요.

## 플러그인 원칙

플러그인은 아직 배포하지 않습니다. 다음 조건이 갖춰졌을 때만 관련 스킬을 묶습니다.

1. 각 스킬이 독립 설치·호출·실행 검증을 통과함
2. 함께 쓸 때 입력·산출물 handoff가 명확함
3. 따로 설치해도 핵심 기능이 유지됨
4. plugin manifest와 설치·업데이트·제거 smoke가 별도로 통과함

따라서 사용자는 **개별 스킬만 선택**하거나, 나중에 **업무 흐름 플러그인으로 함께 설치**할 수 있습니다.

## 원본 보호

- 원본: `~/.claude/skills` — 읽기 전용
- 배포본: 이 저장소의 `skills/`
- 검토 수정본: `overrides/`
- 원본·배포본 SHA-256: `docs/analysis/source-manifest.json`
- 토큰, 쿠키, OAuth 상태, 고객정보, 개인 절대경로는 배포 금지

## 유지보수자 검증

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

정적 PASS와 실제 Claude Code smoke PASS는 별도 증거로 관리합니다. 현재 검증 범위는 [session-to-skill 검증 기록](docs/verification/session-to-skill.md)에 기록합니다.

## 상태

- 저장소: private
- 배포 모드: standalone-skill-first
- 오늘 검증 대상: 1개
- 플러그인: 보류
- 공개 전환: 별도 승인 필요
