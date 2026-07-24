---
name: wylie-folder-organizer
description: 표준 프로젝트 템플릿과 파일명 규칙을 기준으로 문서를 분류한다. 기본은 dry-run이며 승인 전에는 파일을 이동하지 않는다.
---

# Wylie Folder Organizer

## 요구 환경

- Python 3.9 이상
- 표준 라이브러리만 사용
- 외부 API, MCP, 계정 불필요

## Workflow

1. `references/taxonomy.md`에서 표준 폴더 체계를 확인한다.
2. 다른 템플릿을 기준으로 쓸 때는 먼저 `scripts/analyze_template.py <template-root>`로 구조를 분석한다.
3. `scripts/organize_project.py <target-root>`를 **`--apply` 없이** 실행한다.
4. dry-run 결과에서 매칭·미분류·충돌·대상 경로를 검토한다.
5. 규칙이 부족하면 `references/routing-rules.json`을 좁은 키워드부터 보완한다.
6. 사용자 승인을 받은 뒤에만 `--apply`를 실행한다.
7. 이동 전후 파일 수와 해시를 비교하고 JSON report를 보존한다.

## Commands

```bash
python scripts/organize_project.py "<target-root>"
python scripts/organize_project.py "<target-root>" --apply --report "<target-root>/organize-report.json"
python scripts/analyze_template.py "<template-root>"
```

Windows에서는 `python`, macOS/Linux에서는 환경에 따라 `python3`를 사용한다.

## 안전 규칙

- 미분류 파일은 기본적으로 움직이지 않는다.
- 확장자보다 업무 문서 키워드를 우선한다.
- 광범위한 fallback 규칙보다 구체 규칙을 먼저 둔다.
- 기존 파일을 덮어쓰지 않는다.
- 심볼릭 링크와 숨김 파일 처리 결과를 report에 기록한다.
- 중요한 프로젝트에서 `--apply`는 명시적 승인 없이는 금지한다.

## 완료 조건

- dry-run report 검토 완료
- 이동 대상과 제외 대상이 분리됨
- apply 실행 시 전후 파일 수가 일치함
- 오류·충돌·미분류 목록이 남아 있음
