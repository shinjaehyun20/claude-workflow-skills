# Session fixture: verified CSV cleanup workflow

User: 고객에게 받은 CSV를 원본 보존하면서 정리해줘.
Assistant: 원본 SHA-256을 기록하고 작업 사본을 만들겠습니다.
Tool result: source hash recorded; working copy created.
Assistant: UTF-8 인코딩과 헤더 중복을 검사했습니다. 중복 헤더 1개를 제거했습니다.
User: 원본은 절대 수정하면 안 돼. 결과 행 수도 확인해줘.
Assistant: 원본과 결과 파일의 해시, 행 수, 필수 헤더를 비교하겠습니다.
Tool result: source unchanged; output rows=120; required headers present; parse passed.
User: 다음에도 재사용할 수 있게 이 절차를 스킬로 만들어줘.

Expected reusable pattern:
- preserve source and record source hash
- work on a copy
- normalize encoding and duplicate headers
- verify row count, required headers, parseability, and source immutability
