# Contributing

## Principles

- 직접 제작이 확인된 `owner-authored` 스킬만 배포 후보로 등록합니다.
- third-party, adapted, forked, unknown 스킬은 이 저장소에 배포하지 않습니다.
- 설치된 스킬 수와 직접 제작한 스킬 수를 동일시하지 않습니다.
- `~/.claude/skills` 원본은 읽기 전용입니다.
- 하루에 1~2개 스킬만 `config/selection.json`에 추가합니다.
- 검토 수정은 `overrides/<skill>/`에서 하고 배포본은 importer가 `skills/<skill>/`에 생성합니다.
- 각 스킬의 standalone 검증이 끝나기 전에는 plugin manifest를 추가하지 않습니다.
- 고객 데이터, 개인 절대경로, 토큰, 쿠키, OAuth 상태, 내부 메시지를 commit하지 않습니다.

## Required per-skill package

1. `SKILL.md`
2. `README.md` — 언제 쓰는지, 언제 쓰지 않는지, 호출법
3. 입력·출력·의존성·제한사항
4. 실패·복구 방법
5. 저위험 fixture와 expected contract
6. source/distribution SHA-256
7. 실제 Claude Code smoke 기록
8. changelog entry

## Development

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

## Pull request gate

- Authorship registry: owner-authored only
- Generalization status: generalized
- Daily release limit: PASS
- Source immutability: PASS
- Standalone skill structure: PASS
- Usage guide: PASS
- Secret/path/client scan: PASS
- Claude Code fixture smoke: PASS
- README/docs updated: PASS

## Plugin gate

플러그인은 관련 standalone 스킬들이 모두 검증된 후 별도 PR로 추가합니다. plugin manifest validation만으로 각 스킬의 실제 사용성이 증명되지는 않습니다.
