# Portability Architecture

## Goal

한 세션에서 검증된 업무 패턴을 특정 사용자, 경로, 고객, OS에 묶지 않고 Claude Code 스킬로 재사용합니다.

## session-to-skill portability

### Input adapter

- 현재 세션
- 사용자가 지정한 transcript/log
- 프로젝트 내부 evidence 파일

### Output adapter

- 프로젝트 전용: `<project>/.claude/skills/<name>/`
- 사용자 전역: `~/.claude/skills/<name>/` — 명시 승인 필요
- 검토용: 지정 staging/output

### Generalization rules

- 개인 절대경로 → `<project>`, `~`, 환경변수
- 고객·프로젝트 고유명 → 역할 또는 placeholder
- 외부 런타임 명령 → Claude Code에서 실제 지원되는 단계만 유지
- 토큰·쿠키·OAuth·session id → 삭제, 예시값도 보존 금지
- 실행되지 않은 아이디어 → `skill candidate`, 검증된 절차와 분리

## Optional assets

`references/`와 `scripts/`는 실제 재사용 가치와 검증 증거가 있을 때만 추가합니다. 빈 폴더나 추정 스크립트는 만들지 않습니다.

## Plugin boundary

스킬은 먼저 standalone으로 검증합니다. 플러그인은 설치 편의와 workflow handoff를 제공하는 후속 배포 수단이며, plugin schema validation이 개별 스킬 행동 검증을 대체하지 않습니다.

## Excluded

- hooks
- MCP configuration
- OAuth/cookies
- 자동 외부 전송·게시·삭제
- 고객별 절대경로
- 다른 AI 런타임의 identity·권한·설정
