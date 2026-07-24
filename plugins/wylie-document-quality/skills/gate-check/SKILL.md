---
name: gate-check
description: 사용자 전달 직전 문서 산출물의 구조, 내용, 렌더, 경로, 원본 보호, 비밀값을 통합 검증하고 실패 시 전달을 차단하는 스킬.
user-invocable: false
---

# Delivery Gate Check

## 공통 게이트

- [ ] 기준 파일·버전·SHA-256이 기록됨
- [ ] 원본 해시가 시작 시점과 동일함
- [ ] 변경 범위가 사용자 요청 안에 있음
- [ ] 절대경로, 개인정보, 토큰, 비밀번호, 쿠키가 없음
- [ ] 임시 파일과 중간 렌더가 납품 폴더에 없음
- [ ] 결과 파일이 실제로 열리고 예상 개수·구조와 일치함

## 형식별 게이트

### PPTX
- 슬라이드 수, 순서, 레이아웃, 이미지 참조가 유효함
- 렌더에서 텍스트 잘림·겹침·폰트 대체가 없음

### XLSX
- 시트명·순서, 헤더, 수식, 셀 형식, 병합 영역이 의도대로임

### DOCX/HWPX
- 섹션·스타일·표·이미지가 유효하고 변환/열기 검증을 통과함

### PDF
- 페이지 수, 폰트, 이미지, 링크, 텍스트 추출 가능 여부를 확인함

## 출력

```text
[gate-check] structure: PASS
[gate-check] render: PASS
[gate-check] source-immutability: PASS
[gate-check] secret-scan: PASS
[gate-check] overall: PASS
```

하나라도 실패하면 실패 위치와 최소 수정안을 제시하고 같은 검증을 다시 실행한다.
