# Portability Architecture

## Goal

같은 업무 의도를 유지하면서 사용자, OS, 디렉터리, 도구, 계정이 달라도 안전하게 실행한다.

## Four layers

### 1. Workflow contract

각 스킬은 입력, 단계, 산출물, 검증, 다음 단계만 정의한다. 특정 에이전트 이름이나 내부 runtime 소유권을 전제로 하지 않는다.

### 2. Environment adapter

- 입력 경로: 사용자 제공 또는 현재 프로젝트 기준
- 출력 경로: 사용자 제공 또는 프로젝트의 `output/<skill>/`
- Python: Windows `python`, macOS/Linux `python3` 가능
- 문서·브라우저 도구: 현재 환경에서 사용 가능한 동등 도구 선택

### 3. Optional capability

Figma 로그인, PPTX 생성, 브라우저 자동화처럼 모든 환경에 없는 기능은 optional이다. 없을 때는:

1. 지원되는 중간 산출물을 생성한다.
2. 미생성 항목과 이유를 명시한다.
3. 수동 입력 또는 export fallback을 제공한다.

### 4. Safety and verification

- 원본 read-only
- 파일 이동 전 dry-run
- 외부 전송·게시·댓글·삭제는 명시 승인
- 해시, 구조, 렌더, 비밀값 검증

## Deliberately excluded from v0.1

- hooks
- MCP server configuration
- OAuth and cookies
- undocumented private APIs
- automatic upload, send, publish, or submission
- project/client-specific absolute paths
- Hermes, Codex, Gemini, OpenClaw, or muse ownership contracts

## Environment matrix

| Capability | Required | Fallback |
|---|---|---|
| Claude Code | yes | none |
| Git | install/update only | ZIP distribution |
| Python 3.9+ | folder organizer | manual classification |
| Browser access | benchmark/design review | user-provided screenshots/exports |
| PPTX tooling | optional output | HTML + screen-list + layout spec |
| Figma session | optional | exported PNG/PDF |

## Publication rule

A skill is portable only when its core workflow still produces a useful, verifiable result without the optional capabilities.
