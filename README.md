# DocAssist (AI 기반 문서 이해 보조 시스템)

복잡한 전문 문서를 AI가 분석하여 요약, 용어 설명, 문단별 해설을 제공하는 문서 이해 보조 플랫폼입니다.

## 🛠 기술 스택

- **Frontend**: Vue 3, Vite, TypeScript, Pinia, Axios
- **Backend**: FastAPI (Python 3.12), SQLAlchemy (Async), Pydantic
- **Database**: PostgreSQL (with pgvector for Vector Search)
- **AI**: OpenAI API (GPT-4o, Text Embedding 3)
- **Infrastructure**: Docker, Docker Compose

## 🚀 시작하기 (로컬 개발 환경)

이 프로젝트는 백엔드와 프론트엔드가 분리되어 있으며, 데이터베이스는 Docker 컨테이너로 실행됩니다.

### 1. 사전 요구 사항
- Docker & Docker Compose
- Node.js v20 이상
- Python 3.12 이상

### 2. 환경 변수 설정
`backend` 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력하세요.

```bash
# backend/.env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5454/docassist
SECRET_KEY=your_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
OPENAI_API_KEY=sk-... (여기에 OpenAI API Key 입력)
```

### 3. 데이터베이스 실행
Docker를 사용하여 PostgreSQL(pgvector 포함) 데이터베이스를 실행합니다.

```bash
cd backend
docker-compose up -d db
```
*   DB 포트: `5454` (로컬 충돌 방지)
*   Admin 페이지(pgAdmin): `http://localhost:5050` (Email: `admin@admin.com`, PW: `admin`)

### 4. 백엔드 서버 실행
```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# DB 마이그레이션 (최초 1회)
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
서버가 `http://localhost:8000`에서 실행됩니다. (Swagger UI: `http://localhost:8000/docs`)

### 5. 프론트엔드 서버 실행
새 터미널을 열고 실행하세요.

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev -- --port 3000
```
브라우저에서 `http://localhost:3000`으로 접속합니다.

---

## 🐳 Docker로 한 번에 실행하기 (배포 모드)

개발 환경 설정 없이 Docker만으로 전체 서비스를 실행할 수 있습니다.

```bash
# 루트 디렉토리에서 실행 (OPENAI_API_KEY 환경변수 설정 필요)
export OPENAI_API_KEY=sk-...
docker-compose -f docker-compose.prod.yml up -d --build
```

- **프론트엔드**: `http://localhost:80`
- **백엔드 API**: `http://localhost:8000`

## 📂 프로젝트 구조

```
DocAssist/
├── backend/            # FastAPI 백엔드
│   ├── app/            # 애플리케이션 핵심 로직 (API, Models, Services)
│   ├── alembic/        # DB 마이그레이션 스크립트
│   ├── tests/          # Pytest 테스트 코드
│   └── Dockerfile      # 백엔드 이미지 빌드 설정
├── frontend/           # Vue 3 프론트엔드
│   ├── src/            # 소스 코드 (Pages, Components, Stores, API)
│   ├── public/         # 정적 리소스
│   └── Dockerfile      # 프론트엔드 이미지 빌드 설정 (Nginx)
├── docs/               # 개발 문서 및 기획서 (DB Schema, API Spec)
└── docker-compose.prod.yml # 프로덕션 배포용 설정
```

## 🧪 테스트 실행

### 백엔드 단위/통합 테스트
```bash
cd backend
pytest
```

## 📚 더 자세한 설명
각 파일의 역할과 상세 코드 설명은 **[docs/FRONTEND_STRUCTURE.md](./docs/FRONTEND_STRUCTURE.md)** 또는 `docs/` 폴더를 참고하세요.
