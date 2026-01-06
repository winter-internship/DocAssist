import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.logging_config import setup_logging
from app.db.session import SessionLocal
from app.db.init_db import init_db

# 로깅 설정 초기화
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup 단계에서 DB 초기화 또는 마이그레이션 관련 작업을 수행합니다.
    # - `init_db` 는 필요한 초기 데이터를 넣거나 스키마를 확인하는 데 사용됩니다.
    logger.info("Initializing database...")
    async with SessionLocal() as db:
        await init_db(db)
    yield
    # Shutdown 단계: 리소스 정리 로직 위치
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 500 에러 발생 시 로그에 스택 트레이스 기록
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please check server logs."},
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to DocAssist API"}
