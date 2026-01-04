import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# .env 파일을 명시적으로 로드합니다.
current_file = os.path.abspath(__file__)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file)))), "backend", ".env")

if not os.path.exists(env_path):
    env_path = ".env"

print(f"DEBUG: Loading env from: {env_path}, Exists: {os.path.exists(env_path)}")

# 수동 로딩 (폴백)
if os.path.exists(env_path):
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"DEBUG: File content length: {len(content)}")
            # print(f"DEBUG: File content preview: {content[:50]}...")
            
            f.seek(0)
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
                    # print(f"DEBUG: Manually set env var: {key}")
    except Exception as e:
        print(f"DEBUG: Failed to read .env file: {e}")

load_dotenv(env_path, override=True)

# 디버그: 로드된 키 확인 (일부만 출력)
key = os.getenv("OPENAI_API_KEY")
print(f"DEBUG: Config loaded key from env: {key[:10] if key else 'None'}")

class Settings(BaseSettings):
    PROJECT_NAME: str = "DocAssist"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/docassist"

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore" 
    )

settings = Settings()
