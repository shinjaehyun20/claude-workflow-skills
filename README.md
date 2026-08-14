# Claude Workflow Skills

> Claude Code에서 반복 작업을 **실행·검증·복구·증거 기반 종료**까지 진행하도록 돕는 공개 워크플로우 스킬 모음입니다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills-6B5CE7)](https://code.claude.com/docs/en/skills)
[![Skills](https://img.shields.io/badge/skills-2-00A86B)](#제공-스킬)
[![Validate](https://github.com/shinjaehyun20/claude-workflow-skills/workflows/Validate%20marketplace/badge.svg)](https://github.com/shinjaehyun20/claude-workflow-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

![Claude Code 스킬 모음](docs/assets/hero.svg)

## 무엇이 다른가

이 저장소는 프롬프트 모음이 아닙니다. 각 스킬은 다음을 명시합니다.

- 언제 사용하고, 언제 사용하지 않는지
- 필요한 입력과 기대 산출물
- 작업 순서와 실패·복구 절차
- 검증 방법과 완료 주장에 필요한 증거

공개 배포 전에는 저작권·범용화·민감정보·정적 검증·행동 fixture를 점검합니다. 설치된 스킬 수나 성공적인 명령 종료만으로 품질을 주장하지 않습니다.

## 제공 스킬

| 스킬 | 무엇을 할 수 있나요? | 사용 가이드 |
| --- | --- | --- |
| [`session-to-skill`](skills/session-to-skill/) | 검증된 대화 세션을 재사용 가능한 Claude Code 스킬로 정리합니다. | [자세히 보기](skills/session-to-skill/README.md) |
| [`weekly-report-evidence`](skills/weekly-report-evidence/) | 직전 계획과 현재 원본을 대조해 근거 기반 주간보고를 작성합니다. | [자세히 보기](skills/weekly-report-evidence/README.md) |

## 빠른 시작

### 1. 저장소 받기

```bash
git clone https://github.com/shinjaehyun20/claude-workflow-skills.git
cd claude-workflow-skills
```

### 2. 필요한 스킬만 프로젝트에 설치

```bash
mkdir -p .claude/skills
cp -R skills/weekly-report-evidence .claude/skills/
```

Claude Code에서 다음처럼 호출합니다.

```text
/weekly-report-evidence 이번 주 업무 로그와 지난주 계획을 대조해 팀 주간보고를 작성해줘.
```

스킬마다 독립 설치할 수 있습니다. 전역 설치는 기존 동명 스킬과의 차이를 확인한 뒤, 사용자가 명시적으로 원할 때만 선택하세요. 처음 설치하는 경우 [시작 가이드](docs/getting-started.md)를, 설치·제거 세부 절차는 [설치 가이드](docs/INSTALLATION.md)를 참고하세요.

## 품질과 공개 정책

- 직접 제작이 확인된 자산만 공개 후보가 됩니다.
- 개인명, 고객 정보, 절대 경로, 자격증명, 비공개 런타임 결합은 일반화 단계에서 제거합니다.
- 각 스킬에는 fixture와 기대 행동 계약이 있어야 합니다.
- 공개 배포 전에 정적 검사와 fresh-session 행동 smoke를 분리해 통과해야 합니다.
- 이 저장소는 Claude Code 우선입니다. 다른 도구와의 호환성은 실제 adapter 검증 전에는 약속하지 않습니다.

자세한 기준은 [저작권·범용화 정책](docs/AUTHORSHIP-AND-GENERALIZATION-POLICY.md), [누적 릴리스 파이프라인](docs/MULTI-SKILL-RELEASE-PIPELINE.md), [기여 안내](CONTRIBUTING.md)에서 확인할 수 있습니다.

## 이용 범위

이 저장소의 스킬과 문서는 MIT License로 공개 배포됩니다. 누구나 사용, 복사, 수정, 재배포할 수 있으며, 실제 업무 데이터·개인정보·비공개 프로젝트 맥락은 각 사용자가 별도로 제거하고 검증해야 합니다. 자세한 내용은 [MIT License](LICENSE)를 확인하세요.
