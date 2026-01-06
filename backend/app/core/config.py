import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 환경 변수 로딩
#
# 프로젝트 루트의 `backend/.env` 를 우선 시도하고, 없으면 현재 작업 디렉터리의
# `.env` 를 폴백으로 사용합니다. 이 코드는 로컬 개발 환경에서 `.env` 파일을
# 명시적으로 로드해 `os.environ` 에 값을 채우기 위해 존재합니다.
# ---------------------------------------------------------------------------
current_file = os.path.abspath(__file__)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file)))), "backend", ".env")

if not os.path.exists(env_path):
    env_path = ".env"

print(f"DEBUG: Loading env from: {env_path}, Exists: {os.path.exists(env_path)}")

# 수동으로 파일을 읽어 환경변수로 설정 (간단한 파싱)
if os.path.exists(env_path):
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"DEBUG: File content length: {len(content)}")
            
            f.seek(0)
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"DEBUG: Failed to read .env file: {e}")

load_dotenv(env_path, override=True)

# 디버그: 일부 중요한 키 값 존재 여부 출력
key = os.getenv("OPENAI_API_KEY")
print(f"DEBUG: Config loaded key from env: {key[:10] if key else 'None'}")


class Settings(BaseSettings):
    """
    애플리케이션 설정 (pydantic 기반)

    - `DATABASE_URL` : SQLAlchemy(Async) 연결 문자열
    - `OPENAI_API_KEY` : 외부 API 키 (환경변수에서 읽음)
    """
    PROJECT_NAME: str = "DocAssist"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database: 기본값은 로컬 포스트그레스(개발용)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/docassist"

    # OpenAI API 키는 환경 변수에서 읽습니다.
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
