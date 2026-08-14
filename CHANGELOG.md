# Changelog

All notable changes follow Keep a Changelog principles.

## [Unreleased]

### Added

- `weekly-report-evidence`: 직전 계획, 기간 내 원본 기록, 귀속 검증을 대조해 확인 가능한 사실만 주간보고로 정리하는 standalone 스킬 후보를 추가했습니다.
- 공개용 주간보고 fixture, 기대 행동 계약, 검증 기록을 추가했습니다.

### Changed

- 배포본이 없는 `keepworking-loop`를 공개 카탈로그에서 제외하고, registry 상태를 후보로 되돌려 실제 `skills/` 디렉터리와 일치시켰습니다.
- 배포 대상을 직접 제작이 확인된 `owner-authored` 스킬로 제한했습니다.
- 설치된 사용자 스킬 수와 직접 제작 스킬 수를 분리했습니다.
- 범용화·스킬화·workflow 정본화 판정과 상태 흐름을 문서화했습니다.
- importer와 validator에 authorship registry 및 generalization fail-closed gate를 추가했습니다.
- README를 단일 스킬 소개가 아닌 누적형 multi-skill catalog 진입점으로 재구성했습니다.
- `release_batch`와 누적 `skill-registry`를 분리해 새 배포가 기존 스킬을 삭제하지 않도록 importer·manifest·validator를 수정했습니다.

## [0.2.0-alpha] - 2026-07-24

### Changed

- 배포 순서를 `스킬 단독 검증 → 관련 스킬 플러그인 묶음`으로 교정했습니다.
- 첫 배포 대상을 사용자 애착 스킬 `session-to-skill` 1개로 제한했습니다.
- 스킬별 사용 시점, 비사용 시점, 호출법, 입력·출력, 의존성, 안전, 실패·복구 가이드를 추가했습니다.
- 하루 배포 한도를 1~2개로 validator에 고정했습니다.
- 구조 검사와 실제 Claude Code fixture smoke를 분리해 기록하도록 변경했습니다.

### Removed from current main distribution

- 선행 검증 없이 먼저 묶었던 3개 플러그인과 11개 스킬 배포본
- 공개 저장소에 불필요한 전체 298개 상세 인벤토리

공개 배포 전 민감한 업무 맥락과 비공개 운영 흔적을 제거하는 sanitation을 수행했습니다.

## [0.1.0-alpha] - 2026-07-24

### Added

- Initial local prototype with multiple portability-reviewed skills.
- Read-only importer, source hashes, validator, and repository documentation.

### Limitation

- 이 버전은 저장소·manifest 정적 검증용 prototype이었으며 스킬별 실제 Claude Code 실행 검증은 완료하지 않았습니다.
