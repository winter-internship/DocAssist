# 개발 진행 현황 보고서 (Development Status Report)

**날짜**: 2026년 1월 2일
**작성자**: AI Assistant

## 1. 개요
본 문서는 DocAssist 프로젝트의 백엔드 핵심 기능 개발 및 프론트엔드 연동 1차 완료 상태를 기술합니다.
FastAPI 기반의 백엔드 구축, PostgreSQL(pgvector)를 활용한 RAG 파이프라인 구현, 그리고 Vue.js 프론트엔드와의 연동이 주요 성과입니다.

## 2. 주요 달성 사항

### 2.1 백엔드 아키텍처 구축
- **Framework**: FastAPI (Async support)
- **Database**: PostgreSQL 16 + `pgvector` extension
- **ORM**: SQLAlchemy 2.0 (AsyncSession 사용)
- **Migration**: Alembic을 통한 스키마 버전 관리
- **Structure**: `app/api` (라우터), `app/services` (비즈니스 로직), `app/models` (DB 모델), `app/schemas` (Pydantic DTO)의 계층적 구조 확립

### 2.2 핵심 기능 구현
1.  **사용자 관리 (Auth)**
    - JWT 기반 인증 시스템 구축 (`OAuth2PasswordBearer`)
    - Argon2 알고리즘을 사용한 비밀번호 해싱
    - 회원가입, 로그인, 내 정보 조회 API 구현

2.  **문서 관리 (Document)**
    - 파일 업로드 및 로컬 스토리지 저장 (확장성을 위한 S3 인터페이스 고려)
    - 문서 메타데이터 DB 저장 및 Soft Delete 구현
    - **비동기 문서 처리 워커**: 업로드 직후 백그라운드 태스크(`BackgroundTasks`)로 텍스트 추출 및 임베딩 생성 작업 위임

3.  **RAG 파이프라인 (Retrieval-Augmented Generation)**
    - **Document Processor**: `PyMuPDF`로 PDF 텍스트 추출, `tiktoken`으로 토큰 기반 청킹 수행.
    - **Embedding**: OpenAI `text-embedding-3-small` 모델을 사용하여 벡터 생성.
    - **Vector Search**: `pgvector`의 코사인 유사도(`<=>`) 연산자를 사용하여 사용자 질문과 가장 관련성 높은 문서 청크 검색.
    - **LLM Integration**: 검색된 컨텍스트를 프롬프트에 주입하여 GPT-4o(또는 3.5)가 정확한 답변을 생성하도록 유도.

### 2.3 프론트엔드 연동
- **Client**: Axios 인터셉터를 통한 JWT 토큰 자동 주입 및 에러 처리.
- **State Management**: Pinia를 사용한 사용자 인증 상태 관리 (`auth.store.ts`).
- **UI Integration**:
    - 로그인/회원가입 폼 연동 및 유효성 검사.
    - 대시보드 사용자 정보 표시.
    - 문서 업로드 페이지 연동 및 업로드 후 상세 페이지 이동 로직 구현.

## 3. 테스트 및 검증
모든 핵심 기능에 대해 `pytest` 및 `playwright`를 사용한 테스트를 수행했습니다.

| 구분 | 테스트 항목 | 상태 | 비고 |
| :--- | :--- | :---: | :--- |
| **Backend** | 사용자 인증 (Signup/Login) | ✅ Pass | 중복 이메일 처리, 토큰 발급 확인 |
| **Backend** | 문서 CRUD | ✅ Pass | 업로드, 조회, Soft Delete 검증 |
| **Backend** | 문서 처리 워커 | ✅ Pass | PDF 파싱, 임베딩 DB 저장 확인 (비동기 세션 이슈 해결) |
| **Backend** | RAG 흐름 | ✅ Pass | 특정 지식("달의 수도") 주입 후 검색 기반 답변 생성 확인 |
| **E2E** | 전체 사용자 시나리오 | ✅ Pass | Playwright 사용: 가입 -> 로그인 -> 홈 -> 업로드 이동 확인 |

## 4. 기술적 이슈 및 해결
- **DB 세션 관리**: `pytest-asyncio`와 SQLAlchemy `AsyncSession` 사용 시 이벤트 루프 충돌 및 트랜잭션 롤백 문제가 발생했으나, `conftest.py`의 fixture scope 조정(`function`)과 `expire_on_commit=False` 설정을 통해 해결함.
- **환경 변수 로딩**: `.env` 파일 로딩 문제로 `pydantic-settings` 설정과 경로를 명시적으로 지정하여 해결.
- **RAG 정확도**: 초기 단순 LLM 호출에서, 벡터 검색 로직을 추가하여 문서 기반 답변의 정확도를 확보함.

## 5. 향후 계획 (Next Steps)
1.  **Task 22: 문서 비교 및 채팅 UI 고도화**
    - 업로드된 문서의 원문과 분석 결과(요약/번역)를 나란히 보여주는 뷰어 구현.
    - 채팅 메시지의 실시간 업데이트 (현재는 폴링 방식 고려, 필요 시 WebSocket 도입 검토).
2.  **용어집(Glossary) 기능**: 문서 내 전문 용어 자동 추출 및 툴팁 표시 기능 구현.
3.  **배포 환경 구성**: Docker Compose를 활용한 프로덕션 배포 설정.

---
*문서 작성일: 2026-01-02*


