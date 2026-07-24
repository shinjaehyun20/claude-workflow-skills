# Changelog

All notable changes follow Keep a Changelog principles.

## [Unreleased]

### Changed

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

Git 이력에는 초기 private prototype이 남아 있으며, 공개 전환 전 history sanitation을 별도 수행합니다.

## [0.1.0-alpha] - 2026-07-24

### Added

- Private prototype with three skills-only plugins and eleven portability-reviewed skills.
- Read-only importer, source hashes, validator, and repository documentation.

### Limitation

- 이 버전은 저장소·manifest 정적 검증용 prototype이었으며 스킬별 실제 Claude Code 실행 검증은 완료하지 않았습니다.
