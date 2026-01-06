from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 비동기 SQLAlchemy 엔진 생성
# - `settings.DATABASE_URL` 에서 DB 연결 문자열을 읽어옵니다.
# - `echo=True` 는 SQL 로그를 출력하는 데 사용됩니다(디버그용).
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 비동기 세션 팩토리
# - `class_=AsyncSession` 로 비동기 세션을 사용하도록 설정합니다.
# - `expire_on_commit=False` 는 커밋 후에 객체가 만료되어 추가적인 조회 시 에러가 발생하는 것을 방지합니다.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Declarative base for ORM models
Base = declarative_base()


async def get_db():
    """
    FastAPI 의존성으로 사용되는 비동기 DB 세션 생성기

    사용 예:
        async def endpoint(db: AsyncSession = Depends(get_db)):
            await db.execute(...)

    세션은 컨텍스트 매니저로 열리고, 종료 시 안전하게 닫힙니다.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
