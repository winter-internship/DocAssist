import asyncio
import os
import sys
from openai import AsyncOpenAI

# Add project root to path to load config
sys.path.append(os.getcwd())

from app.core.config import settings

async def test_openai():
    print(f"DEBUG: Loaded API Key: {settings.OPENAI_API_KEY[:10]}..." if settings.OPENAI_API_KEY else "DEBUG: No API Key loaded")
    
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello, is this working?"}],
            max_tokens=10
        )
        print(f"SUCCESS: OpenAI Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"ERROR: OpenAI API call failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_openai())


