# Installation

## 1. 저장소 받기

```bash
git clone https://github.com/shinjaehyun20/wylie-claude-workflow-skills.git
cd wylie-claude-workflow-skills
```

저장소가 private인 동안에는 접근 권한이 있는 계정이 필요합니다.

## 2. 개별 스킬 설치

### 프로젝트 전용 — 권장

대상 프로젝트 루트에서:

```bash
mkdir -p .claude/skills
cp -R <repo>/skills/session-to-skill .claude/skills/
```

프로젝트에만 적용되므로 다른 Claude Code 작업에 영향을 주지 않습니다.

### 사용자 전역

```bash
mkdir -p ~/.claude/skills
cp -R <repo>/skills/session-to-skill ~/.claude/skills/
```

동일한 이름이 이미 있으면 덮어쓰지 말고 먼저 diff를 확인합니다.

## 3. 호출 확인

자연어 호출:

```text
이 세션을 스킬로 만들어줘.
```

명시 호출:

```text
/session-to-skill 현재 세션의 검증·복구 워크플로우
```

처음에는 등록까지 진행하지 말고 분석 결과 형식이 맞는지 저위험 대화로 확인하는 것을 권장합니다.

## 4. 검증

저장소 자체 검증:

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

확인 항목:

1. 원본 SHA-256 불변
2. frontmatter와 디렉터리명 일치
3. 사용 시점·비사용 시점·입력·출력·실패 복구 문서 존재
4. 개인 경로·고객 식별자·자격정보 없음
5. fixture 기반 실제 Claude Code 응답에 필수 분석 항목 존재

## 5. 제거

프로젝트 전용:

```bash
rm -rf .claude/skills/session-to-skill
```

사용자 전역:

```bash
rm -rf ~/.claude/skills/session-to-skill
```

삭제 전 사용자 작성 변경이 있는지 diff 또는 백업으로 확인합니다.

## 플러그인 설치

현재 버전에는 플러그인이 없습니다. 개별 스킬 검증이 누적된 뒤 관련 스킬만 별도 plugin manifest로 묶습니다.
