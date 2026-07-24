# Publication Checklist

## Daily scope

- [ ] 선택 스킬이 `config/skill-registry.json`에서 `owner-authored`로 확인됨
- [ ] third-party/adapted/forked/unknown 스킬이 포함되지 않음
- [ ] 범용화 상태가 `generalized`이고 publication eligible임
- [ ] 오늘 선택한 스킬이 1~2개 이하
- [ ] 각 스킬이 이전 검증 대상과 독립적으로 설명됨
- [ ] plugin bundling은 standalone 검증 뒤로 보류됨

## Source protection

- [ ] `python tools/import_and_analyze.py` passes
- [ ] Source immutability is `PASS`
- [ ] 모든 원본 `SKILL.md`에 source SHA-256 존재
- [ ] Claude Code 원본과 비대상 런타임 원본 무변경

## Per-skill documentation

- [ ] 언제 사용하면 좋은지
- [ ] 언제 사용하지 않는지
- [ ] 자연어·명시 호출 예시
- [ ] 입력·산출물·의존성
- [ ] 개인정보·경로 portability
- [ ] 실패·복구
- [ ] 제한사항

## Verification layers

- [ ] Frontmatter와 디렉터리명 일치
- [ ] JSON/Python/링크/위험 문자열 정적 검사
- [ ] fixture contract 존재
- [ ] 실제 Claude Code에서 저위험 fixture smoke 실행
- [ ] 필수 응답 marker 확인
- [ ] 원본 source hash 재확인

## Remote

- [ ] Repository is private
- [ ] Default branch is `main`
- [ ] GitHub Actions green
- [ ] Remote HEAD equals local HEAD
- [ ] Remote clone에서 validator 재실행

## Plugin phase — 현재 해당 없음

- [ ] 관련 스킬 standalone 검증 완료
- [ ] 묶음 사용과 단독 사용 차이 문서화
- [ ] plugin manifest validation
- [ ] 설치·업데이트·제거 smoke

## Public transition — 별도 승인

- [ ] 라이선스 확정
- [ ] 초기 private prototype이 남은 Git history sanitation
- [ ] 원격 가시성 전환 후 raw 파일·README 재검증
