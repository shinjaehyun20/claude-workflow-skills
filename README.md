# Wylie Claude Workflow Skills

> 직접 제작한 Claude Code 스킬을 범용화하고 검증해 **하나의 저장소에서 누적 관리하는 멀티 스킬 컬렉션**입니다.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-portable%20skills-6B5CE7)](https://docs.anthropic.com/en/docs/claude-code)
[![Catalog](https://img.shields.io/badge/catalog-1%20skill-00A86B)](#스킬-카탈로그)
[![Plugins](https://img.shields.io/badge/plugins-deferred-lightgrey)](#플러그인-경계)
[![Validation](https://img.shields.io/badge/validation-local%20%2B%20CI-00A86B)](tools/validate_repo.py)

![범용 Claude Code 스킬 컬렉션](docs/assets/hero.svg)

## 이 저장소의 구조

이 저장소는 스킬마다 새 repository를 만드는 방식이 아닙니다. 검증이 끝난 스킬을 `skills/<skill-name>/` 아래에 계속 추가합니다.

- **하나의 repository, 여러 standalone skills**
- 각 스킬은 독립 설치·호출·제거 가능
- 공통 품질 기준과 검증기는 repository 단위로 공유
- 연관 스킬의 workflow handoff가 안정된 뒤에만 선택적 plugin으로 묶음
- 배포 카탈로그의 기계 판독 정본은 [`config/skill-registry.json`](config/skill-registry.json)

## 스킬 카탈로그

| 스킬 | 분류 | 설명 | 버전 | 검증 |
| --- | --- | --- | --- | --- |
| [`session-to-skill`](skills/session-to-skill/) | Workflow authoring | 검증된 대화 세션을 재사용 가능한 Claude Code 스킬로 정규화합니다. | 1.0.0 | [기록](docs/verification/session-to-skill.md) |

각 디렉터리에는 실행 계약인 `SKILL.md`와 상세 사용 가이드 `README.md`가 함께 있습니다. 새 스킬은 직접 제작·범용화·standalone 검증 gate를 통과한 뒤 이 표와 registry에 추가됩니다.

## 빠른 시작

### 1. 저장소 받기

```bash
git clone https://github.com/shinjaehyun20/wylie-claude-workflow-skills.git
cd wylie-claude-workflow-skills
```

Private 상태에서는 repository 접근 권한이 있는 계정이 필요합니다.

### 2. 설치할 스킬 선택

카탈로그에서 이름을 고른 뒤 필요한 스킬만 설치합니다.

```bash
SKILL_NAME=session-to-skill
```

프로젝트 전용 설치 — 권장:

```bash
mkdir -p <project>/.claude/skills
cp -R "skills/$SKILL_NAME" <project>/.claude/skills/
```

사용자 전역 설치:

```bash
mkdir -p ~/.claude/skills
cp -R "skills/$SKILL_NAME" ~/.claude/skills/
```

동일 이름 스킬이 이미 있으면 덮어쓰기 전에 diff를 확인하세요. 자세한 설치·호출·제거 절차는 [설치 가이드](docs/INSTALLATION.md)를 참고하세요.

## Repository layout

```text
skills/                     # 누적 배포되는 standalone skills
  <skill-name>/
    SKILL.md
    README.md
overrides/                  # 원본을 직접 수정하지 않는 범용화 정본
config/
  skill-registry.json       # 전체 배포 카탈로그 SSOT
  selection.json            # 현재 검증·배포 release batch
tests/
  fixtures/                 # 스킬별 저위험 입력
  expected/                 # 스킬별 행동 계약
docs/
  verification/             # 스킬별 실제 검증 기록
  analysis/                 # source/distribution manifest
tools/                      # importer와 repository validator
```

## 누적 배포 모델

`release_batch`는 한 번에 검토하는 변경량을 제한할 뿐, repository에 스킬 하나만 유지한다는 뜻이 아닙니다.

```text
직접 제작 후보
  → authorship 확인
  → 범용화
  → standalone package·fixture·guide
  → 실제 Claude Code smoke
  → registry와 skills/에 누적
  → private remote 재검증
```

Importer는 현재 release batch만 갱신하고, registry에 이미 올라간 기존 스킬은 보존합니다. 전체 실행 순서와 실패·복구·종료 조건은 [Multi-Skill Release Pipeline](docs/MULTI-SKILL-RELEASE-PIPELINE.md), 승격 기준은 [직접 제작·범용화 정책](docs/AUTHORSHIP-AND-GENERALIZATION-POLICY.md)을 참고하세요.

## 품질 기준

배포되는 모든 스킬은 다음을 갖춰야 합니다.

1. 저장소 소유자가 직접 제작한 `owner-authored` 스킬
2. 개인명·고객명·절대경로·인증정보를 제거한 범용 계약
3. 사용 시점과 비사용 시점
4. 입력·산출물·의존성·제한사항
5. 실패·복구 절차
6. fixture와 expected behavior contract
7. 원본/배포본 SHA-256 및 source immutability 확인
8. 실제 Claude Code 저위험 smoke 기록

## 플러그인 경계

플러그인은 repository 전체를 자동으로 묶는 기본 배포 단위가 아닙니다. 다음 조건을 충족한 관련 스킬만 별도 plugin으로 구성합니다.

- 각 standalone skill이 독립 검증을 통과함
- 스킬 사이 입력·산출물 handoff가 명확함
- 단독 설치에서도 핵심 기능이 유지됨
- plugin 설치·업데이트·제거 smoke가 별도로 통과함

따라서 사용자는 개별 스킬을 골라 설치할 수 있고, 나중에는 검증된 workflow bundle을 선택할 수 있습니다.

## 유지보수자 검증

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

Validator는 registry·카탈로그·실제 `skills/` 디렉터리·fixture·manifest의 일치 여부와 개인정보·경로·자격정보 위험을 함께 확인합니다.

## 상태

- 저장소: private alpha
- 배포 구조: multi-skill catalog, standalone-first
- 현재 공개된 standalone skill: 1개
- plugin: 0개
- public 전환: 별도 승인 필요
