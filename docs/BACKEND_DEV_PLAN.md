# DocAssist 백엔드 개발 계획 (FastAPI)

## 1. 프로젝트 초기 설정 (Foundation)
- [x] **Task 11: FastAPI 프로젝트 구조 및 환경 설정**
    - [x] 프로젝트 디렉토리 구조 생성 (`app/`, `tests/`, `scripts/` 등)
    - [x] `requirements.txt` 작성 및 의존성 설치 (FastAPI, SQLAlchemy, Pydantic 등)
    - [x] 환경 변수 관리 설정 (`.env`, `config.py` - pydantic-settings)
    - [x] Git 설정 (`.gitignore`)

- [x] **Task 12: 데이터베이스 및 Docker 환경 구성**
    - [x] `docker-compose.yml` 작성 (PostgreSQL + pgvector, pgAdmin)
    - [x] SQLAlchemy 비동기 세션 설정 (`app/db/session.py`, `AsyncSession`)
    - [x] Alembic 마이그레이션 환경 설정 (`alembic init`, `env.py` 수정)

## 2. 데이터 모델링 (Domain Modeling)
- [x] **Task 13: 사용자 및 인증 도메인 모델**
    - [x] `User` 모델 정의 (UUID, Email, PasswordHash, Role)
    - [x] `PasswordReset`, `TermAgreement` 모델 정의

- [x] **Task 14: 문서 및 지식 관리 도메인 모델**
    - [x] `Document` 모델 정의 (File Metadata, S3 Key, Status)
    - [x] `DocumentJob` 모델 정의 (비동기 작업 추적)
    - [x] `DocumentEmbedding` 모델 정의 (pgvector 컬럼 포함)
    - [x] `DocumentAnalysis`, `GlossaryTerm` 모델 정의

- [x] **Task 15: 채팅 및 시스템 도메인 모델**
    - [x] `ChatSession`, `ChatMessage` 모델 정의
    - [x] `SupportTicket`, `SystemLog` 모델 정의
    - [x] Alembic 마이그레이션 스크립트 생성 및 적용

## 3. 핵심 API 구현 (Core Features)
- [x] **Task 16: 인증 및 사용자 관리 API**
    - [x] JWT 토큰 발행 및 검증 유틸리티 (`core/security.py`)
    - [x] 로그인/회원가입 엔드포인트 (`/auth/signup`, `/auth/login`)
    - [x] 내 정보 조회 및 수정 엔드포인트 (`/users/me`)
    - [x] 단위/통합 테스트 작성 (`tests/api/v1/test_auth.py`)

- [x] **Task 17: 문서 관리 API**
    - [x] 파일 업로드 및 메타데이터 저장 (`/documents/upload`)
    - [x] 문서 목록 및 상세 조회 (`/documents/`, `/documents/{id}`)
    - [x] 문서 삭제 (Soft Delete)
    - [x] 테스트 코드 작성 (`tests/api/v1/test_documents.py`)

- [x] **Task 18: 채팅 및 Q&A API**
    - [x] 채팅 세션 생성 및 목록 조회 (`/chat/sessions`)
    - [x] 메시지 전송 및 이력 조회 (`/chat/sessions/{id}/messages`)
    - [x] 기본 LLM 연동 구조 설계 (`RAGService`)
    - [x] 테스트 코드 작성 (`tests/api/v1/test_chat.py`)

## 4. AI/RAG 파이프라인 구현 (Advanced Features)
- [x] **Task 19: 문서 처리 워커 (Document Processor)**
    - [x] PDF/텍스트 파일 파싱 및 텍스트 추출 (`DocumentProcessor`)
    - [x] 텍스트 청킹(Chunking) 로직 구현
    - [x] OpenAI Embedding API 연동
    - [x] 백그라운드 태스크 연동 (FastAPI BackgroundTasks) 및 DB 저장
    - [x] 처리 로직 테스트 (`tests/api/v1/test_document_processing.py`)

- [x] **Task 20: RAG 검색 및 답변 생성 최적화**
    - [x] `pgvector` 기반 코사인 유사도 검색 로직 구현 (`RAGService.retrieve_context`)
    - [x] 검색된 컨텍스트를 활용한 LLM 프롬프트 구성
    - [x] 채팅 API와 RAG 서비스 연동
    - [x] RAG 흐름 통합 테스트 (`tests/api/v1/test_rag.py`)

## 5. 프론트엔드 연동 및 고도화 (Integration)
- [x] **Task 21: 프론트엔드 기본 연동**
    - [x] Axios 및 Pinia(상태관리) 설정
    - [x] 로그인/회원가입 페이지 연동
    - [x] 문서 업로드 페이지 연동
    - [x] Playwright E2E 테스트 (회원가입 -> 로그인 -> 홈 진입)

- [x] **Task 22: 문서 비교 및 채팅 페이지 고도화**
    - [x] `DocComparePage` 문서 상세 및 채팅 연동
    - [x] `DashboardHome` 문서 요약 및 목록 API 연동
    - [x] `DrivePage` 문서 목록, 필터링, 삭제 API 연동

- [x] **Task 24: 프론트엔드 하드코딩 제거 및 API 완전 연동 (New)**
    - [x] `ProfilePage.vue` 사용자 정보 수정 API 연동
    - [x] `QaPage.vue` 전체 채팅 세션 목록 조회 및 이어하기 연동
    - [x] 공통 상수 (`constants/`) 분리 (문서 상태, 에러 메시지 등)
    - [x] 하드코딩된 더미 데이터 전면 제거 및 로딩 상태 처리

- [ ] **Task 23: 시스템 관리 및 안정화**
    - [ ] 에러 핸들링 및 로깅 강화
    - [ ] 배포 환경 구성 (Docker Compose prod 모드)
    - [ ] 최종 QA 및 버그 수정
