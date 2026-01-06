import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from app.core.config import settings


async def test_connection():
    url = settings.DATABASE_URL
    print(f"Testing DB connection to: {url}")
    engine = create_async_engine(url, echo=False)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.scalar()
            print(f"Query result: {row}")
            if row == 1:
                print("DB connection successful (SELECT 1 returned 1).")
            else:
                print("DB connected but unexpected result from SELECT 1.")
    except Exception as e:
        print("DB connection failed:", repr(e))
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())
