# Installation

## 1. 저장소 받기

```bash
git clone https://github.com/shinjaehyun20/claude-workflow-skills.git
cd claude-workflow-skills
```

저장소는 공개 배포용입니다. GitHub 계정 없이도 clone할 수 있습니다.

## 2. 스킬 선택

[README의 스킬 카탈로그](../README.md#스킬-카탈로그) 또는 `config/skill-registry.json`에서 설치할 스킬 이름을 확인합니다.

```bash
SKILL_NAME=session-to-skill
```

앞으로 새 스킬이 추가되어도 같은 명령에서 `SKILL_NAME`만 바꾸면 됩니다.

## 3. 개별 스킬 설치

### 프로젝트 전용 — 권장

대상 프로젝트 루트에서:

```bash
mkdir -p .claude/skills
cp -R "<repo>/skills/$SKILL_NAME" .claude/skills/
```

프로젝트에만 적용되므로 다른 Claude Code 작업에 영향을 주지 않습니다.

### 사용자 전역

```bash
mkdir -p ~/.claude/skills
cp -R "<repo>/skills/$SKILL_NAME" ~/.claude/skills/
```

동일한 이름이 이미 있으면 덮어쓰지 말고 먼저 diff를 확인합니다.

## 4. 사용법 확인

각 스킬의 상세 호출법은 다음 파일에 있습니다.

```text
skills/<skill-name>/README.md
```

예: `session-to-skill`

```text
이 세션을 스킬로 만들어줘.
```

```text
/session-to-skill 현재 세션의 검증·복구 워크플로우
```

처음에는 원본 파일을 변경하지 않는 저위험 입력으로 행동 계약을 확인하는 것을 권장합니다.

## 5. 저장소 검증

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

확인 항목:

1. registry에 등록된 전체 배포 스킬과 `skills/` 디렉터리 일치
2. 현재 `release_batch`가 직접 제작·범용화 gate를 통과함
3. 원본 SHA-256 불변
4. frontmatter와 디렉터리명 일치
5. 사용 가이드와 fixture contract 존재
6. 개인 경로·고객 식별자·자격정보 없음

## 6. 제거

프로젝트 전용:

```bash
rm -rf ".claude/skills/$SKILL_NAME"
```

사용자 전역:

```bash
rm -rf "$HOME/.claude/skills/$SKILL_NAME"
```

삭제 전 사용자 작성 변경이 있는지 diff 또는 백업으로 확인합니다.

## 플러그인 설치

현재 버전에는 플러그인이 없습니다. 독립 검증이 누적되고 workflow handoff가 확인된 관련 스킬만 나중에 별도 plugin으로 묶습니다.
