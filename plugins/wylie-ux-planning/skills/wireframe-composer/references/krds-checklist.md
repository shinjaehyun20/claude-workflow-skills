# KRDS 준수 체크리스트 및 컴포넌트 가이드

> 기준: 행정안전부 한국형 디자인 시스템 (KRDS) — https://krds.go.kr
> 공공 사이트 여부 확인 후 적용. 비공공 프로젝트는 참고 수준으로 사용.

---

## 1. KRDS 준수 사전 판별

아래 항목 중 하나라도 해당하면 KRDS 전면 적용 대상이다.

- [ ] 발주처가 중앙부처 / 지방자치단체 / 공공기관인가
- [ ] RFP 또는 계약에 "공공 UI 가이드라인", "KRDS", "행정안전부 표준" 언급이 있는가
- [ ] .go.kr / .or.kr 도메인을 사용하는가
- [ ] 예산이 국가/지방 재정에서 지원되는가

→ 하나라도 해당 시: **KRDS 전면 적용 (필수)**
→ 해당 없음: KRDS 부분 참조 (권장 수준)

---

## 2. KRDS 준수 점검 항목 (ASIS 분석용)

### 2-1. 기초 인프라

| 점검 항목 | 준수 기준 | 점검 결과 |
|---------|---------|---------|
| 정부 공통 헤더 적용 | 로고, 서비스명, GNB 구조 준수 | ✓ / ✗ / 부분 |
| 정부 공통 푸터 적용 | 기관명, 저작권, 관련 사이트 링크 | ✓ / ✗ / 부분 |
| 공공 서체 사용 | 나눔고딕 / 나눔바른고딕 / 공공 라이선스 서체 | ✓ / ✗ |
| 공공 색상 팔레트 | KRDS 주요 색상 토큰 사용 여부 | ✓ / ✗ |
| 그리드 시스템 | 1200px 컨텐츠 영역, 12컬럼 기준 | ✓ / ✗ |

### 2-2. 컴포넌트 준수

| 컴포넌트 | KRDS 기준 | 현행 | 준수 여부 |
|---------|---------|------|---------|
| 버튼 | Primary / Secondary / Ghost 3단계, 최소 높이 44px | | |
| 인풋 | 라벨 상단 배치, 에러 메시지 하단, 필수 asterisk | | |
| 테이블 | 헤더 고정, 반응형 처리, 정렬 기능 | | |
| 드롭다운/셀렉트 | 키보드 접근 가능, aria-expanded 적용 | | |
| 모달/다이얼로그 | 포커스 트랩, ESC 닫기, 배경 scroll-lock | | |
| 알림/토스트 | role="alert", 자동 사라짐 3~5초 | | |
| 페이지네이션 | 현재 페이지 강조, aria-current 적용 | | |
| 탭 | role="tablist", aria-selected, 키보드 방향키 | | |
| 아코디언 | aria-expanded, 콘텐츠 영역 id 연결 | | |
| 브레드크럼 | aria-label="경로", 현재 위치 aria-current="page" | | |

### 2-3. 접근성 (KWCAG 2.2 연계)

| 항목 | 기준 | 점검 결과 |
|------|------|---------|
| html lang 속성 | `<html lang="ko">` 필수 | |
| 페이지 title | 서비스명 + 현재 페이지명 | |
| skip navigation | 본문 바로가기 링크 최상단 | |
| 제목 계층 (H1~H6) | 페이지당 H1 1개, 계층 건너뜀 없음 | |
| 이미지 alt | 기능 이미지: 기능 설명, 장식 이미지: alt="" | |
| 폼 label 연결 | 모든 input에 label 또는 aria-label | |
| 색상 대비율 | 일반 텍스트 4.5:1, 큰 텍스트 3:1 이상 | |
| 키보드 접근 | 모든 기능 키보드만으로 가능 | |
| 포커스 표시 | outline 제거 금지, 명확한 포커스 링 | |
| 터치 영역 | 최소 44×44px | |
| user-scalable | 확대 차단 금지 (`user-scalable=no` 금지) | |
| 오류 안내 | 오류 원인·수정 방법 텍스트로 제공 | |

---

## 3. KRDS 미준수 항목 → 개선안 매핑

| 미준수 항목 | 개선 방향 | 개선 ID 예시 | 우선순위 |
|-----------|---------|------------|---------|
| 정부 공통 헤더 미적용 | KRDS 헤더 컴포넌트 교체 | IMP-KRDS-01 | 🔴 |
| 버튼 높이 44px 미달 | KRDS Button 컴포넌트 적용 | IMP-KRDS-02 | 🔴 |
| 인풋 라벨 좌측 배치 | KRDS Form Input 레이아웃 적용 | IMP-KRDS-03 | 🟠 |
| 모달 포커스 트랩 없음 | KRDS Modal 컴포넌트 교체 | IMP-KRDS-04 | 🔴 |
| 공공 서체 미사용 | 나눔고딕/나눔바른고딕 전환 | IMP-KRDS-05 | 🟠 |
| 색상 대비 미달 | KRDS 색상 토큰 기준 재정의 | IMP-KRDS-06 | 🔴 |
| skip nav 없음 | 최상단 본문 바로가기 링크 추가 | IMP-KRDS-07 | 🔴 |
| 페이지 title 미설정 | 페이지별 title 규칙 정의 및 적용 | IMP-KRDS-08 | 🟠 |

---

## 4. KRDS 색상 토큰 기준 (주요)

| 토큰명 | 용도 | Hex |
|-------|------|-----|
| --blue-700 | Primary 버튼, 주요 강조 | #0047AB |
| --blue-500 | 링크, 보조 강조 | #1976D2 |
| --gray-900 | 기본 텍스트 | #1A1A1A |
| --gray-600 | 보조 텍스트 | #5E5E5E |
| --gray-100 | 배경, 비활성 | #F5F5F5 |
| --red-600 | 오류, 필수 표시 | #D32F2F |
| --green-600 | 성공, 완료 | #388E3C |
| --orange-500 | 경고 | #F57C00 |

> ⚠️ 위 값은 KRDS 공식 문서(https://krds.go.kr) 기준이며, 버전 업데이트 시 공식 사이트 재확인 필요.

---

## 5. KRDS 컴포넌트 → 와이어프레임 매핑

와이어프레임 작성 시 아래 컴포넌트 명칭을 주석에 명시한다.

| KRDS 컴포넌트명 | 와이어프레임 주석 표기 | 사용 화면 유형 |
|--------------|------------------|--------------|
| Button | `[KRDS] Button / Primary / h:48px` | 전체 |
| Button | `[KRDS] Button / Secondary / h:40px` | 전체 |
| Input | `[KRDS] Input / Text / w:100%` | TYPE-D, E |
| Select | `[KRDS] Select / Default` | TYPE-D, E |
| Checkbox | `[KRDS] Checkbox` | TYPE-D, E |
| Radio | `[KRDS] Radio` | TYPE-D, E |
| Table | `[KRDS] Table / Sortable` | TYPE-B, G |
| Pagination | `[KRDS] Pagination / 10 per page` | TYPE-B |
| Tab | `[KRDS] Tab / Horizontal` | TYPE-A, B |
| Modal | `[KRDS] Modal / Confirm` | 전체 |
| Alert | `[KRDS] Alert / Error` | 전체 |
| Toast | `[KRDS] Toast / Success / 3s` | 전체 |
| Breadcrumb | `[KRDS] Breadcrumb` | TYPE-B~F |
| Step Indicator | `[KRDS] Step / 3-step` | TYPE-E |
| Badge | `[KRDS] Badge / Status` | TYPE-B, G |
| Accordion | `[KRDS] Accordion` | TYPE-F |
| Tooltip | `[KRDS] Tooltip` | TYPE-D, E |
| File Upload | `[KRDS] FileUpload / Single` | TYPE-D |
