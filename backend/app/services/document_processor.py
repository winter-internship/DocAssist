import fitz  # PyMuPDF
import tiktoken
from typing import List, Dict, Any
import openai
from app.core.config import settings

# openai.api_key는 설정이나 전역에서 설정되지만, 사용을 보장합시다.
# 참고: 최신 openai 버전은 클라이언트 인스턴스를 사용하지만, 일부 패턴에서는 전역 설정이 여전히 지원됩니다.
# 메서드 내부에서 AsyncOpenAI 클라이언트 패턴을 사용하거나 전역 `openai.embeddings.create` 헬퍼를 사용할 것입니다.

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_text(self, file_path: str, file_type: str) -> str:
        """
        파일 타입에 따라 텍스트를 추출합니다.
        """
        text = ""
        file_type = file_type.lower()
        
        if "pdf" in file_type:
            try:
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text() + "\n"
            except Exception as e:
                print(f"Error extracting text from PDF: {e}")
        elif "txt" in file_type:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print(f"Error extracting text from TXT: {e}")
        
        # 나중에 이미지 지원(OCR) 추가 예정
        
        return text

    def chunk_text(self, text: str) -> List[str]:
        """
        토큰 수를 기준으로 텍스트를 청크로 분할합니다.
        """
        if not text:
            return []
            
        tokens = self.encoding.encode(text)
        total_tokens = len(tokens)
        chunks = []
        
        start = 0
        while start < total_tokens:
            end = min(start + self.chunk_size, total_tokens)
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            if end == total_tokens:
                break
            
            start += self.chunk_size - self.chunk_overlap
            
        return chunks

    async def create_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """
        OpenAI API를 사용하여 텍스트 청크에 대한 임베딩을 생성합니다.
        """
        if not chunks:
            return []
            
        embeddings = []
        # 배치 처리: OpenAI 제한은 모델에 따라 보통 요청당 2048 또는 8191 토큰이지만,
        # 여기서는 문자열 리스트를 보냅니다. 청크 리스트가 크지 않다고 가정합니다.
        # 만약 청크 리스트가 매우 크다면, 이 루프도 배치로 처리해야 합니다.
        
        batch_size = 20 # 안전한 배치 크기
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            try:
                response = await self.client.embeddings.create(
                    input=batch,
                    model="text-embedding-3-small"
                )
                embeddings.extend([data.embedding for data in response.data])
            except Exception as e:
                print(f"Error creating embeddings for batch {i}: {e}")
                # None이나 0을 추가? 아니면 중단? 일단 데이터 손실 가능성 있음.
                
        return embeddings

    async def analyze_document(self, text: str) -> Dict[str, Any]:
        """
        LLM을 사용하여 문서를 분석하고 요약, 용어, 문단 설명을 추출합니다.
        """
        if not text:
            return {}

        # 비용/토큰 절약을 위해 분석용 컨텍스트 제한 (앞부분 위주)
        context_text = text[:30000] # 약 7-10k 토큰
        
        system_prompt = """
        You are a smart document assistant. Analyze the provided text and output a JSON object.
        The output must strictly follow this schema:
        {
            "summary": "A concise summary of the entire document (Korean)",
            "terms": [
                {"term": "Term", "definition": "Definition in Korean"}
            ],
            "rules": [
                {"title": "Rule/Condition Title", "desc": "Description of the rule/condition", "source": "Inferred section or context"}
            ],
            "paragraphs": [
                {
                    "original": "Original paragraph text (keep as is from source if possible, or key sentences)",
                    "easy": "Easy explanation in Korean",
                    "bullets": ["Key point 1", "Key point 2"]
                }
            ]
        }
        
        Guidelines:
        1. Extract up to 10 key 'terms' that are technical or specific to the domain.
        2. Extract up to 5 key 'rules' or important conditions found in the text.
        3. For 'paragraphs', select 3-5 representative paragraphs from the text (e.g. from the beginning or key sections) to demonstrate the 'original' vs 'easy' explanation feature. Do not process the entire document text into paragraphs to save output tokens.
        4. All explanations ('easy', 'definition', 'summary') MUST be in Korean.
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this text:\n\n{context_text}..."}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=4000 
            )
            
            content = response.choices[0].message.content
            import json
            return json.loads(content)
        except Exception as e:
            print(f"Error analyzing document: {e}")
            return {}

processor = DocumentProcessor()

