# 프로젝트 구조 및 파일 설명

이 문서는 프론트엔드(`frontend/`) 디렉토리의 각 파일이 무엇을 하는지, 어떻게 작동하는지 설명합니다.

## 📁 프론트엔드 구조

```
frontend/
├── src/                          # 소스 코드 폴더
│   ├── api/                      # 백엔드 API 통신 모듈 (axios, services)
│   ├── constants/                # 상수 정의
│   ├── pages/                    # 페이지 컴포넌트들 (화면 단위)
│   ├── components/               # 재사용 가능한 UI 컴포넌트 (현재는 pages 내부에 일부 포함)
│   ├── router/                   # 라우팅 설정 (index.ts)
│   ├── stores/                   # 상태 관리 (Pinia - auth.ts)
│   ├── App.vue                   # 최상위 루트 컴포넌트
│   ├── main.ts                   # 프로그램 시작점
│   ├── style.css                 # 전역 스타일
│   └── vite-env.d.ts            # TypeScript 타입 정의
├── index.html                    # HTML 진입점
├── package.json                  # 프로젝트 설정 및 라이브러리 목록
├── vite.config.ts               # Vite 빌드 도구 설정
└── tsconfig.json                 # TypeScript 설정
```

---

## 📄 각 파일 상세 설명

### 1. `index.html` - 웹페이지의 뼈대

**역할**: 브라우저가 처음 읽는 HTML 파일입니다. 웹사이트의 기본 구조를 정의합니다.

**주요 내용**:
- `<div id="app">`: Vue 앱이 여기에 렌더링됩니다
- `<script src="/src/main.ts">`: 프로그램 시작점을 연결합니다

**비유**: 집의 기초와 뼈대입니다. 여기에 Vue 앱이 들어갑니다.

---

### 2. `src/main.ts` - 프로그램 시작점

**역할**: Vue 앱을 시작하고 라우터(페이지 이동)와 Pinia(상태 관리)를 설정합니다.

**비유**: 건물의 전기 배선과 계단입니다. 어떤 방(페이지)으로 갈지 정해줍니다.

---

### 3. `src/App.vue` - 최상위 컴포넌트

**역할**: 모든 페이지를 감싸는 최상위 컴포넌트입니다.

**코드 설명**:
```vue
<template>
  <div id="app">
    <router-view />  <!-- 여기에 현재 페이지가 표시됩니다 -->
  </div>
</template>
```

**비유**: 건물의 외벽과 지붕입니다. 모든 방(페이지)을 감쌉니다.

---

### 4. `src/pages/` - 페이지 컴포넌트

각 페이지는 `src/pages/` 디렉토리에 위치합니다.

*   **`DashboardHome.vue`**: 메인 대시보드. 최근 문서, 활동 내역, 통계를 보여줍니다.
*   **`DocComparePage.vue`**: 문서 상세 보기 및 비교 페이지. 원문과 AI 분석 내용을 나란히 보여줍니다.
*   **`QaPage.vue`**: 문서 기반 Q&A 채팅 페이지.
*   **`UploadPage.vue`**: 문서 업로드 페이지.
*   **`ProfilePage.vue`**: 사용자 프로필 설정 페이지.
*   **`DrivePage.vue`**: 내 문서함(드라이브) 페이지.
*   **`LoginPage.vue` / `SignupPage.vue`**: 인증 관련 페이지.

---

### 5. `src/api/` - API 통신

백엔드 서버와의 통신을 담당하는 파일들입니다.

*   **`axios.ts`**: Axios 인스턴스 설정 (Base URL, 인터셉터 등).
*   **`document.service.ts`**: 문서 관련 API 호출 함수 모음.
*   **`chat.service.ts`**: 채팅 관련 API 호출 함수 모음.

---

### 6. `vite.config.ts` - 빌드 도구 설정

**역할**: Vite(빌드 도구)의 동작 방식을 설정합니다.

**주요 내용**:
*   포트 설정 (`3000`)
*   프록시 설정 (`/api` 요청을 백엔드로 전달)

---

## 🔄 데이터 흐름

```
1. 사용자가 페이지 접속
   ↓
2. Vue 컴포넌트(Page) 로드
   ↓
3. onMounted에서 Service 호출 (예: documentService.getDocuments())
   ↓
4. Axios가 백엔드 API 요청 (GET /api/v1/documents)
   ↓
5. 백엔드 응답 (JSON)
   ↓
6. Vue 컴포넌트가 데이터를 받아 화면 업데이트
```

