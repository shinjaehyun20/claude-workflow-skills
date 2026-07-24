---
name: supplied-scan
description: 고객 제공 파일과 기준 폴더를 패턴 검색이 아닌 전수 목록으로 점검하고 누락·번호·확장자 범위를 검증하는 스킬.
---

# Supplied Source Scan

## 절차

1. 대상 루트 아래의 모든 파일을 재귀적으로 목록화한다.
2. 상대 경로, 확장자, 크기, 수정 시각을 기록한다.
3. 필요 시 SHA-256을 계산한다.
4. 문서 번호 또는 연번이 있으면 최대 번호와 실제 목록을 대조한다.
5. 예상 확장자(`.xlsx`, `.pptx`, `.docx`, `.hwp`, `.hwpx`, `.pdf` 등)의 포함 여부를 명시한다.
6. 누락·중복·이름 충돌은 `[확인 필요]`로 기록한다. 찾지 못한 파일을 없다고 단정하지 않는다.

## 포터블 실행 예시

macOS/Linux:
```bash
find "<target-root>" -type f -print
```

Windows PowerShell:
```powershell
Get-ChildItem -LiteralPath "<target-root>" -File -Recurse
```

Python 표준 라이브러리도 사용할 수 있다. 어떤 방법이든 숨김 파일 처리와 심볼릭 링크 정책을 결과에 적는다.

## 출력

`supplied-inventory.md` 또는 `supplied-inventory.json`에 스캔 루트, 실행 시각, 파일 수, 확장자 분포, 누락 의심, 중복 의심을 기록한다.
