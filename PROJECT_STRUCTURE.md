# 프로젝트 구조 및 파일 설명

이 문서는 프로젝트의 각 파일이 무엇을 하는지, 어떻게 작동하는지 쉽게 설명합니다.

## 📁 전체 프로젝트 구조

```
textProject/
├── src/                          # 소스 코드 폴더
│   ├── pages/                    # 페이지 컴포넌트들 (화면 단위)
│   │   └── DashboardHome.vue    # 대시보드 홈 화면
│   ├── App.vue                   # 최상위 루트 컴포넌트
│   ├── main.ts                   # 프로그램 시작점
│   ├── style.css                 # 전역 스타일 (색상 변수 등)
│   └── vite-env.d.ts            # TypeScript 타입 정의
├── index.html                    # HTML 진입점
├── package.json                  # 프로젝트 설정 및 라이브러리 목록
├── vite.config.ts               # Vite 빌드 도구 설정
├── tsconfig.json                 # TypeScript 설정
└── README.md                     # 프로젝트 설명서
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

**역할**: Vue 앱을 시작하고 라우터(페이지 이동)를 설정합니다.

**코드 설명**:
```typescript
// Vue 앱 생성
const app = createApp(App)

// 라우터 설정 (어떤 URL에 어떤 페이지를 보여줄지)
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DashboardHome }  // "/" 경로 = DashboardHome 페이지
  ]
})

// 라우터를 앱에 연결
app.use(router)

// HTML의 <div id="app">에 Vue 앱을 마운트 (붙임)
app.mount('#app')
```

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

### 4. `src/pages/DashboardHome.vue` - 대시보드 홈 화면

**역할**: 실제 대시보드 화면을 보여주는 페이지 컴포넌트입니다.

**구조**:
- `<template>`: 화면에 보이는 HTML 구조
- `<script setup>`: 데이터와 로직 (TypeScript)
- `<style scoped>`: 이 컴포넌트만의 스타일

**주요 기능**:

#### 4-1. 통계 카드 (stats-grid)
```vue
<div class="stats-grid">
  <div class="stat-card">
    <!-- 총 사용자, 총 매출, 주문 수, 평균 주문 금액 -->
  </div>
</div>
```
- 4개의 통계 카드를 그리드로 배치
- 각 카드에는 아이콘, 숫자, 변화율이 표시됨

#### 4-2. 데이터 정의 (script 부분)
```typescript
// 통계 데이터 (나중에 백엔드 API에서 가져올 예정)
const stats = ref({
  totalUsers: 12453,        // 총 사용자 수
  totalRevenue: 245000000,  // 총 매출
  totalOrders: 3421,        // 주문 수
  avgOrderValue: 71500      // 평균 주문 금액
})

// 최근 활동 목록
const recentActivities = ref([...])
```
- `ref()`: Vue의 반응형 데이터 (값이 바뀌면 화면도 자동 업데이트)
- 현재는 하드코딩된 데이터, 나중에 백엔드 API로 교체 예정

#### 4-3. 최근 활동 목록
```vue
<div v-for="activity in recentActivities" :key="activity.id">
  <!-- 각 활동 항목 표시 -->
</div>
```
- `v-for`: 배열을 반복해서 화면에 표시
- 주문, 회원가입, 결제 등의 활동을 리스트로 표시

**비유**: 실제 방(페이지)입니다. 여기서 통계와 활동을 볼 수 있습니다.

---

### 5. `src/style.css` - 전역 스타일

**역할**: 프로젝트 전체에서 사용하는 색상, 폰트 등의 스타일 변수를 정의합니다.

**주요 내용**:
```css
:root {
  --primary-color: #6366f1;    /* 메인 색상 (보라색) */
  --success-color: #10b981;    /* 성공 색상 (초록색) */
  --bg-color: #f9fafb;         /* 배경색 */
  --text-primary: #111827;     /* 텍스트 색상 */
}
```

**비유**: 건물 전체의 색상 팔레트와 디자인 가이드입니다.

---

### 6. `package.json` - 프로젝트 설정 파일

**역할**: 프로젝트에 필요한 라이브러리와 실행 명령어를 정의합니다.

**주요 내용**:
```json
{
  "dependencies": {
    "vue": "^3.4.0",           // Vue 프레임워크
    "vue-router": "^4.2.5"     // 페이지 라우팅 (이동)
  },
  "scripts": {
    "dev": "vite",              // 개발 서버 실행
    "build": "vue-tsc && vite build"  // 배포용 빌드
  }
}
```

**비유**: 건물을 짓기 위한 도구 목록과 사용 설명서입니다.

---

### 7. `vite.config.ts` - 빌드 도구 설정

**역할**: Vite(빌드 도구)의 동작 방식을 설정합니다.

**주요 내용**:
```typescript
export default defineConfig({
  plugins: [vue()],  // Vue 플러그인 사용
  server: {
    port: 3000,       // 개발 서버 포트
    proxy: {
      '/api': {
        target: 'http://localhost:8000'  // 백엔드 API 주소
      }
    }
  }
})
```

**설명**:
- `port: 3000`: 프론트엔드는 3000번 포트에서 실행
- `proxy`: `/api`로 시작하는 요청을 백엔드(8000번 포트)로 전달
  - 예: `http://localhost:3000/api/users` → `http://localhost:8000/api/users`

**비유**: 건물의 전기, 수도, 인터넷 연결 설정입니다.

---

### 8. `tsconfig.json` - TypeScript 설정

**역할**: TypeScript 컴파일러의 동작 방식을 설정합니다.

**주요 내용**:
- 타입 체크 규칙
- 파일 경로 별칭 (`@/` = `src/`)
- 엄격한 타입 검사 활성화

**비유**: 건물의 안전 규칙과 건축 기준입니다.

---

## 🔄 데이터 흐름 (나중에 백엔드 연동 시)

```
1. 사용자가 페이지 접속
   ↓
2. DashboardHome.vue가 로드됨
   ↓
3. 컴포넌트가 마운트되면 API 호출
   ↓
4. 백엔드(FastAPI)에서 데이터 요청
   ↓
5. PostgreSQL에서 데이터 조회
   ↓
6. 데이터를 JSON으로 반환
   ↓
7. Vue 컴포넌트에서 데이터 받아서 화면에 표시
```

**예시 코드 (나중에 추가할 부분)**:
```typescript
// DashboardHome.vue의 script 부분
import { onMounted } from 'vue'

onMounted(async () => {
  // 페이지가 로드되면 API 호출
  const response = await fetch('/api/dashboard/stats')
  const data = await response.json()
  stats.value = data  // 받은 데이터로 업데이트
})
```

---

## 📝 파일 네이밍 규칙

- **페이지 컴포넌트**: `src/pages/` 폴더에 `PascalCase.vue` 형식
  - 예: `DashboardHome.vue`, `UserList.vue`, `Settings.vue`
- **일반 컴포넌트**: `src/components/` 폴더에 `PascalCase.vue` 형식
  - 예: `Button.vue`, `Card.vue`, `Modal.vue`
- **유틸리티 함수**: `src/utils/` 폴더에 `camelCase.ts` 형식
  - 예: `api.ts`, `formatDate.ts`

---

## 🚀 다음 단계

1. **백엔드 API 연동**: `DashboardHome.vue`에서 실제 API 호출 추가
2. **추가 페이지**: 다른 페이지들도 `src/pages/`에 추가
3. **공통 컴포넌트**: 재사용 가능한 컴포넌트는 `src/components/`에 추가
4. **상태 관리**: 복잡해지면 Pinia 같은 상태 관리 라이브러리 추가

---

## 💡 핵심 개념 정리

- **컴포넌트**: 화면의 한 부분을 독립적으로 만든 것 (재사용 가능)
- **페이지**: 하나의 완전한 화면 (여러 컴포넌트로 구성)
- **라우터**: URL에 따라 다른 페이지를 보여주는 것
- **반응형 데이터**: `ref()`로 만든 데이터는 값이 바뀌면 화면도 자동 업데이트
- **Props**: 부모 컴포넌트에서 자식 컴포넌트로 데이터 전달
- **Events**: 자식 컴포넌트에서 부모 컴포넌트로 이벤트 전달

