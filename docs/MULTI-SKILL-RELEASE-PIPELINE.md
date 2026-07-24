# Multi-Skill Release Pipeline

이 문서는 직접 제작한 Claude Code 스킬을 하나의 저장소에 안전하게 누적 배포하는 canonical pipeline입니다. 개별 스킬의 사용법이 아니라 **후보 선정부터 원격 재검증까지의 repository 운영 계약**을 정의합니다.

## Source와 state

| 역할 | 정본 |
| --- | --- |
| 읽기 전용 원본 | `${CLAUDE_SKILLS_HOME}` (기본 `~/.claude/skills`) |
| 누적 배포 카탈로그 | `config/skill-registry.json` |
| 현재 처리 배치 | `config/selection.json`의 `release_batch` |
| 범용화 정본 | `overrides/<skill-name>/` |
| 생성 배포본 | `skills/<skill-name>/` |
| 행동 fixture | `tests/fixtures/`, `tests/expected/` |
| 검증 기록 | `docs/verification/<skill-name>.md` |

## 상태 흐름

```text
candidate
  -> authorship-confirmed
  -> generalized
  -> batch-selected
  -> imported
  -> static-validated
  -> behavior-smoked
  -> committed
  -> remote-verified
  -> published
```

각 단계가 통과되지 않으면 다음 상태로 승격하지 않습니다. `third-party`, `adapted`, `forked`, `unknown`, `project-specific`은 배포 경로에서 차단합니다.

## 실행 절차

1. `config/skill-registry.json`에 직접 제작·범용화 근거와 목표 상태를 기록합니다.
2. 이번 변경분만 `config/selection.json`의 `release_batch`에 넣습니다. 하루 최대 2개입니다.
3. 원본을 수정하지 않고 `overrides/<skill-name>/`에 portable source와 guide를 작성합니다.
4. fixture, expected contract, verification record를 추가합니다.
5. 기존 스크립트로 생성·검증합니다.

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
python -m py_compile tools/import_and_analyze.py tools/validate_repo.py
git diff --check
```

6. 격리된 Claude Code 환경에서 자연어 또는 명시 호출 smoke를 실행합니다.
7. 의도한 파일만 commit·push합니다.
8. public remote를 새 임시 디렉터리에 clone하고 같은 importer·validator·compile·diff 검사를 반복합니다.
9. 로컬 HEAD와 remote tip이 일치하고 fresh clone이 clean일 때만 `published`로 닫습니다.

## 불변 조건

- 새 `release_batch`는 기존 published skill을 삭제하지 않습니다.
- Registry, README 카탈로그, 실제 `skills/` 디렉터리는 항상 일치해야 합니다.
- 원본 파일 hash는 작업 전후 동일해야 합니다.
- 개인명·고객명·절대경로·토큰·OAuth/MCP 상태·비밀값이 발견되면 배포를 중단합니다.
- Plugin은 관련 standalone skill이 독립 검증된 뒤에만 별도 승격합니다.
- Public 전환은 별도 승인 없이는 수행하지 않습니다.

## 실패와 복구

| 실패 | 최소 복구 |
| --- | --- |
| Authorship 미확정 | Registry 상태를 `unknown`으로 유지하고 batch에서 제거 |
| 개인정보·환경 종속 발견 | Override만 수정하고 importer부터 재실행 |
| 기존 skill 소실 | Registry/merge 로직을 수리하고 누적 보존 시뮬레이션 재실행 |
| README 카탈로그 누락 | Catalog와 registry를 맞춘 뒤 validator 재실행 |
| Claude smoke 실패 | Failure signature를 검증 기록에 남기고 가장 작은 계약 단위 수리 |
| Remote clone 검증 실패 | 배포 완료로 처리하지 않고 원격 기준으로 repair 후 재검증 |

## Close gate

완료는 다음 증거가 모두 있을 때만 인정합니다.

- importer·validator·Python compile·`git diff --check` 통과
- 스킬별 fixture와 Claude Code behavior smoke 통과
- 누적 published skill 보존 확인
- 원본 hash 불변
- public remote push 및 fresh clone 재검증
- README 카탈로그·Registry·`skills/` 일치
- devlog와 검증 기록에 최종 commit 및 근거 기록
