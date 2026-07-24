# Claude Workflow Skills

> Claude Code에서 바로 설치해 사용할 수 있는 공개용 워크플로우 스킬 모음입니다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills-6B5CE7)](https://docs.anthropic.com/en/docs/claude-code)
[![Skills](https://img.shields.io/badge/skills-1-00A86B)](#제공-스킬)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

![Claude Code 스킬 모음](docs/assets/hero.svg)

## 제공 스킬

| 스킬 | 무엇을 할 수 있나요? | 사용 가이드 |
| --- | --- | --- |
| `session-to-skill` | 반복해서 쓸 만한 대화와 작업 절차를 새로운 Claude Code 스킬로 정리합니다. | [자세히 보기](skills/session-to-skill/README.md) |

스킬은 각각 독립적으로 설치할 수 있습니다. 앞으로 새로운 스킬이 추가되면 이 목록에서 필요한 것만 골라 사용하면 됩니다.

## 빠른 시작

### 1. 저장소 받기

```bash
git clone https://github.com/shinjaehyun20/claude-workflow-skills.git
cd claude-workflow-skills
```

이 저장소는 공개 배포용입니다. GitHub 계정 없이도 clone할 수 있습니다.

### 2. 스킬 설치

설치할 스킬 이름을 지정합니다.

```bash
SKILL_NAME=session-to-skill
```

현재 프로젝트에만 설치하려면:

```bash
mkdir -p .claude/skills
cp -R "skills/$SKILL_NAME" .claude/skills/
```

모든 Claude Code 프로젝트에서 사용하려면:

```bash
mkdir -p ~/.claude/skills
cp -R "skills/$SKILL_NAME" ~/.claude/skills/
```

동일한 이름의 스킬이 이미 있다면 덮어쓰기 전에 기존 파일과 비교하세요. 운영체제별 설치·제거 방법은 [설치 가이드](docs/INSTALLATION.md)를 참고하세요.

## 사용 예시

`session-to-skill`을 설치한 뒤 Claude Code에서 자연어로 요청할 수 있습니다.

```text
이 세션에서 반복해서 쓸 수 있는 작업 절차를 스킬로 만들어줘.
```

또는 스킬 이름을 직접 지정합니다.

```text
/session-to-skill 현재 세션의 검증·복구 과정을 재사용 가능한 스킬로 정리해줘.
```

결과를 저장하기 전에는 Claude가 제안한 이름, 사용 조건, 단계, 파일 경로를 검토하세요.

## 스킬 디렉터리

각 스킬은 다음 두 파일을 제공합니다.

```text
skills/<skill-name>/
├── SKILL.md    # Claude Code가 읽는 스킬 정의
└── README.md   # 사용법과 예시
```

## 문서

- [설치 및 제거](docs/INSTALLATION.md)
- [변경 이력](CHANGELOG.md)
- [기여 안내](CONTRIBUTING.md)

## 이용 범위

이 저장소의 스킬과 문서는 MIT License로 공개 배포됩니다. 누구나 사용, 복사, 수정, 재배포할 수 있으며, 실제 업무 데이터·개인정보·비공개 프로젝트 맥락은 각 사용자가 별도로 제거하고 검증해야 합니다. 자세한 내용은 [MIT License](LICENSE)를 확인하세요.
