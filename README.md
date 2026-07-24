# Wylie Claude Workflow Skills

> 개별 프롬프트 모음이 아니라, 실제 업무 단계가 이어지는 **portable Claude Code skills-only marketplace**입니다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills--only-6B5CE7)](https://docs.anthropic.com/en/docs/claude-code)
[![Plugins](https://img.shields.io/badge/plugins-3-0A7CFF)](#플러그인)
[![Skills](https://img.shields.io/badge/skills-11-00A86B)](#플러그인)
[![Validation](https://img.shields.io/badge/validation-local%20%2B%20CI-00A86B)](tools/validate_repo.py)
[![License](https://img.shields.io/badge/license-internal-lightgrey)](LICENSE)

![업무 흐름 중심 Claude Code 스킬 마켓플레이스](docs/assets/hero.svg)

## 왜 만들었나

기존 스킬은 특정 PC 경로, 특정 프로젝트, 다른 AI 런타임, 사내 도구에 결합된 부분이 있었습니다. 이 저장소는 Claude Code 원본을 수정하지 않고 다음 파이프라인으로 배포본만 만듭니다.

```text
원본 인벤토리 → 후보 선택 → 읽기 전용 복제 → 비식별화 → 검토 override → 검증 → 배포
```

원본 298개를 통째로 공개하지 않습니다. 업무 흐름과 독립 실행 가능성을 통과한 11개만 첫 버전에 포함했습니다.

## 플러그인

| 플러그인 | 포함 스킬 | 대표 흐름 |
|---|---:|---|
| `wylie-document-quality` | 5 | 원본 스캔 → 원본 보호 → 베이스 결정 → 서식 적용 → 전달 게이트 |
| `wylie-ux-planning` | 4 | 벤치마킹 → AS-IS/TO-BE → 와이어프레임 → 디자인 정합성 검토 |
| `wylie-project-ops` | 2 | 프로젝트 파일 분류 + 제안서 심사 관점 검토 |

### UX planning workflow

```mermaid
flowchart LR
  A[근거·요구사항] --> B[public-portal-benchmark]
  B --> C[asis-tobe-analysis]
  C --> D[wireframe-composer]
  D --> E[design-spec-review]
  E --> F[수정·확인 요청]
```

## 설치

원격 저장소가 연결된 후 Claude Code에서:

```text
/plugin marketplace add shinjaehyun20/wylie-claude-workflow-skills
/plugin install wylie-ux-planning@wylie-claude-workflow-skills
```

필요한 플러그인만 추가 설치합니다.

```text
/plugin install wylie-document-quality@wylie-claude-workflow-skills
/plugin install wylie-project-ops@wylie-claude-workflow-skills
```

로컬 검토는 저장소 경로를 marketplace로 추가해 수행할 수 있습니다. 자세한 내용은 [설치 가이드](docs/INSTALLATION.md)를 참고하세요.

## 다른 환경에서 동작하는 방식

- 개인 절대경로를 사용하지 않습니다.
- Windows/macOS/Linux 차이는 입력 경로와 실행기에서 흡수합니다.
- 선택 도구가 없으면 지원되는 산출물까지만 만들고 미생성 항목을 명시합니다.
- 외부 API·MCP·OAuth·자동 전송은 v0.1에 포함하지 않습니다.
- 원본 파일은 읽기 전용이며 모든 변경은 사본에 적용합니다.

자세한 설계는 [Portability](docs/PORTABILITY.md)와 [Workflow Map](docs/WORKFLOW-MAP.md)을 확인하세요.

## 유지보수자용 재생성

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

`import_and_analyze.py`는 기본적으로 `~/.claude/skills`를 읽습니다. 다른 원본 경로는 `CLAUDE_SKILLS_HOME` 환경변수로 지정합니다. 실행 후 원본 파일의 SHA-256을 다시 계산해 변경이 없음을 확인합니다.

## 저장소 구조

```text
.claude-plugin/marketplace.json
plugins/<plugin>/
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
overrides/                 # 검토된 portable 배포본
config/selection.json      # 원본에서 가져올 스킬 선택
scripts/                   # 스킬에 포함되는 실행 자산
tools/                     # import·검증 도구
docs/analysis/             # 인벤토리·source hash manifest
```

## 안전과 출처

- Claude Code·Hermes·Codex 원본 스킬을 수정하지 않습니다.
- Codex 이관 스킬은 저장소 publication 품질 절차에만 활용했습니다.
- source/distribution 해시는 [`source-manifest.json`](docs/analysis/source-manifest.json)에 기록됩니다.
- 공개 전 [Publication Checklist](docs/PUBLICATION-CHECKLIST.md)를 모두 통과해야 합니다.

## 상태

`v0.1.0-alpha` 준비 단계입니다. 저장소는 우선 private로 운영하며, 라이선스와 출처 검토 후 공개 범위를 별도로 결정합니다.
