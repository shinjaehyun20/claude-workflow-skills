# Claude Workflow Skills

> Claude Code에서 반복 작업을 **실행·검증·복구·증거 기반 종료**까지 진행하도록 돕는 공개 워크플로우 스킬 모음입니다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills-6B5CE7)](https://code.claude.com/docs/en/skills)
[![Skills](https://img.shields.io/badge/skills-3-00A86B)](#제공-스킬)
[![Validate](https://github.com/shinjaehyun20/claude-workflow-skills/workflows/Validate%20marketplace/badge.svg)](https://github.com/shinjaehyun20/claude-workflow-skills/actions/workflows/validate.yml)
[![Python Support](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](#)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

![Claude Code 스킬 모음](docs/assets/hero.svg)

## 무엇이 다른가

이 저장소는 단순한 프롬프트 모음이 아닙니다. 각 스킬은 프로덕션 수준의 자율 실행을 목표로 다음 항목들을 엄격히 명시합니다.

- **실행 컨텍스트**: 언제 사용하고, 언제 사용하지 않는지 명확한 분기 기준 정의
- **입출력 계약**: 필요한 입력(Arguments)과 기대 산출물(Artifacts)의 스키마 명시
- **행동 절차**: 예외나 실패 시 최소한의 자율 수리와 롤백을 수행하는 복구 시나리오
- **완료 정의**: 행동 fixture 대조 및 physical evidence(파일 크기, 해시 등) 기반의 종료 검증

공개 배포 전에 저작권·범용화·민감정보·정적 검사와 fresh-session 행동 smoke를 자동 점검하여, 에이전트의 단순 자화자찬식 종료 선언을 차단합니다.

## 제공 스킬

| 스킬 | 설명 | 사용 가이드 |
| --- | --- | --- |
| [`keepworking-loop`](skills/keepworking-loop/) | 목표를 고정하고 실행·검증·최소 수리·재검증 자율 루프를 실행합니다. | [자세히 보기](skills/keepworking-loop/README.md) |
| [`session-to-skill`](skills/session-to-skill/) | 검증된 대화 세션 로그를 재사용 가능한 Claude Code 스킬로 자동 추출 및 일반화합니다. | [자세히 보기](skills/session-to-skill/README.md) |
| [`weekly-report-evidence`](skills/weekly-report-evidence/) | 원본 업무 기록과 이전 계획을 정량적으로 대조해 근거 기반 주간보고를 생성합니다. | [자세히 보기](skills/weekly-report-evidence/README.md) |

## 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/shinjaehyun20/claude-workflow-skills.git
cd claude-workflow-skills
```

### 2. 프로젝트 로컬 설치

각 스킬은 개별적으로 프로젝트에 로컬 설치하여 활용할 수 있습니다.

```bash
mkdir -p .claude/skills
cp -R skills/weekly-report-evidence .claude/skills/
```

Claude Code 세션 내에서 다음과 같이 즉각 기동할 수 있습니다.

```text
/weekly-report-evidence 이번 주 업무 로그와 지난주 계획을 대조해 팀 주간보고를 작성해줘.
```

스킬마다 독립 설치할 수 있습니다. 처음 설치하는 경우 [시작 가이드](docs/getting-started.md)를, 설치·제거 세부 절차는 [설치 가이드](docs/INSTALLATION.md)를 참고하세요.

## 🛠️ 로컬 개발 및 유효성 검사

이 저장소는 고품질의 기여 및 배포 상태를 유지하기 위해 자동화된 유효성 검사 검증기(`Validate Repository`)를 내장하고 있습니다.

로컬에서 수정한 스킬이나 새로 추가한 스킬을 기여(PR)하기 전에 반드시 다음 검증 도구를 실행하십시오.

```bash
# 전체 저장소 정적 검사 및 스킬 계약 무결성 검증
python tools/validate_repo.py
```

### 주요 검증 항목
- **민감정보 유출 방지 (Security Guardrails)**: 하드코딩된 API Key, 토큰, 비밀번호 및 로컬 전용 Windows/Unix 절대 경로가 포함되어 있는지 실시간 스캔합니다.
- **스킬 무결성 계약 (Skill Section Contract)**: 모든 `SKILL.md` 문서가 필수 7대 섹션(`## 언제 사용하면 좋은가`, `## 사용하지 않는 경우`, `## 입력`, `## 산출물`, `## 워크플로우`, `## 실패와 복구`, `## Anti-rationalization`)을 충족하는지 검증합니다.
- **Fixture 및 Expected JSON 대조**: 기여된 스킬의 기대 행동 대화 시나리오(`fixtures/*-conversation.md`)가 완료 조건 스키마(`expected/*-contract.json`)와 완벽히 일치하는지 무결성을 검사합니다.

## 품질과 공개 정책

- 직접 제작하고 검증된 소유 자산만 공개 배포의 대상이 됩니다.
- 개인 식별자, 비공개 클라이언트 도메인 정보 및 독자 런타임 의존성은 범용화 과정에서 철저히 격리 또는 제거됩니다.
- 자세한 내용은 [저작권·범용화 정책](docs/AUTHORSHIP-AND-GENERALIZATION-POLICY.md), [누적 릴리스 파이프라인](docs/MULTI-SKILL-RELEASE-PIPELINE.md), 및 [기여 가이드](CONTRIBUTING.md)를 참고해 주십시오.

## 라이선스

이 저장소의 모든 리소스는 [MIT License](LICENSE)로 배포됩니다. 누구나 상업적/비상업적 목적으로 자유롭게 변형하여 배포 및 사용할 수 있습니다.
