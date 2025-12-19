# Text Project

Vue 3 + Vite + TypeScript 기반 프론트엔드 프로젝트

## 기술 스택

- **프론트엔드**: Vue 3 + Vite + TypeScript
- **백엔드**: FastAPI (Python)
- **데이터베이스**: PostgreSQL

## 시작하기

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

개발 서버는 `http://localhost:3000`에서 실행됩니다.

### 빌드

```bash
npm run build
```

### 미리보기

```bash
npm run preview
```

## 프로젝트 구조

```
textProject/
├── src/
│   ├── pages/
│   │   └── DashboardHome.vue    # 대시보드 홈 화면
│   ├── App.vue                   # 루트 컴포넌트
│   ├── main.ts                   # 프로그램 시작점
│   ├── style.css                 # 전역 스타일
│   └── vite-env.d.ts            # TypeScript 타입 정의
├── index.html                    # HTML 진입점
├── package.json                  # 프로젝트 설정
├── vite.config.ts               # Vite 설정
├── tsconfig.json                 # TypeScript 설정
└── PROJECT_STRUCTURE.md          # 상세 파일 설명서
```

## 📚 더 자세한 설명

각 파일의 역할과 코드 설명은 **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** 파일을 참고하세요.

