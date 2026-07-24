# session-to-skill verification

- Date: 2026-07-24
- Release mode: standalone-skill-first
- Status: **PASS**
- Plugin validation: **not applicable** — 현재 plugin 0개

## Artifact

- Skill: `skills/session-to-skill/SKILL.md`
- Usage guide: `skills/session-to-skill/README.md`
- Fixture: `tests/fixtures/session-to-skill-conversation.md`
- Expected contract: `tests/expected/session-to-skill-contract.json`

## Source protection

- Claude source was read-only.
- Source `SKILL.md` SHA-256: `14076f9da4f924bd88bb7d8f908a783018b2a1cc3208bb4d9f48d47ba7c2065a`
- Distribution `SKILL.md` SHA-256: `9c99ccaf3c2f4cfafd76d4102a829d69a924813eebe6f414cf12691d3b118192`
- Importer source immutability result: `PASS`

## Static validation

```json
{
  "status": "PASS",
  "errors": [],
  "warnings": [],
  "release_mode": "standalone-skill-first",
  "plugins": 0,
  "skills": 1
}
```

검사 범위:

- 하루 선택 한도 1~2개
- frontmatter와 디렉터리명
- 필수 사용·비사용·입력·산출물·실패·복구 절
- 트리거 표현 5개 이상
- 개인 절대경로·고객 식별자·자격정보 패턴
- fixture/expected contract 존재
- source manifest 연결

## Actual Claude Code smoke

격리된 임시 프로젝트의 `.claude/skills/session-to-skill`에 **배포본만 복사**하고 아래 조건으로 실행했습니다.

- explicit invocation: `/session-to-skill`
- no session persistence
- no tools
- plan permission mode
- 파일 생성·등록 금지, Step 4 분석 결과에서 정지

Claude Code debug evidence:

- project skill directory discovered
- `1 unique skills`
- `project: 1`
- `plugin skills: 0`

Behavior contract:

- required markers 8/8: PASS
- forbidden markers 0/3 detected: PASS
- requested stop before file creation: PASS
- process exit: 0

Smoke 응답은 제안 이름, 권장 사용 시점, 트리거 5개, 입력, 워크플로우, 산출물, 검증, 원본 불변, 미확인 항목을 모두 구분했습니다.

## Remote clone verification

GitHub `main`을 새 temp 경로에 shallow clone한 뒤 importer와 validator를 다시 실행했습니다.

- remote skill and guide present: PASS
- plugin/marketplace absent: PASS
- importer source immutability: PASS
- repository validator: PASS
- importer rerun working tree clean: PASS

## Evidence

로컬 운영 증거는 저장소 밖 audit lane에 보관합니다.

- `claude-debug.log`
- `claude-smoke-stdout.json`
- `claude-smoke-stderr.txt`
- `behavior-check.json`

## Known limitation

- 이번 smoke는 분석·제안 단계까지 검증했습니다.
- 실제 사용자 프로젝트 또는 사용자 전역 폴더에 설치·파일 생성하는 단계는 원본 환경 보호를 위해 실행하지 않았습니다.
- 플러그인 설치·업데이트·제거 검증은 관련 standalone 스킬이 누적된 뒤 별도 수행합니다.
