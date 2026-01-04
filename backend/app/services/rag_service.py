from typing import List, Optional
from uuid import UUID
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.schemas.chat import ChatMessageCreate
from app.models.document import DocumentEmbedding
from app.services.document_processor import processor

class RAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = "gpt-4o"

    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for query."""
        # Use processor to ensure same model/parameters
        embeddings = await processor.create_embeddings([text])
        return embeddings[0] if embeddings else []

    async def retrieve_context(self, db: AsyncSession, query: str, document_id: Optional[UUID] = None, top_k: int = 5) -> str:
        """Retrieve relevant context from vector store."""
        query_embedding = await self.get_embedding(query)
        if not query_embedding:
            return ""

        # Use pgvector cosine distance operator (<=>)
        stmt = select(DocumentEmbedding).order_by(
            DocumentEmbedding.embedding.cosine_distance(query_embedding)
        ).limit(top_k)
        
        if document_id:
            stmt = stmt.filter(DocumentEmbedding.document_id == document_id)
            
        result = await db.execute(stmt)
        embeddings = result.scalars().all()
        
        # Construct context text with some references if needed
        context_parts = []
        for emb in embeddings:
            context_parts.append(emb.chunk_content)
            
        return "\n\n---\n\n".join(context_parts)

    async def get_chat_completion(
        self,
        db: AsyncSession,
        query: str,
        messages: List[dict],
        document_id: Optional[UUID] = None,
        model: Optional[str] = None,
        user_settings: dict = None
    ) -> ChatMessageCreate:
        
        # 1. Retrieve Context
        # Only retrieve if there's a specific document or if we implement global search
        # For now, let's assume we always search if document_id is provided, 
        # or maybe we should search across all docs if none provided?
        # Let's search if document_id is provided for focused Q&A.
        
        context = ""
        if document_id:
            context = await self.retrieve_context(db, query, document_id)
        
        # 2. Construct System Message with User Settings
        system_message_content = "You are a helpful assistant designed to answer questions about documents."
        
        # Apply Comprehension Aid Settings
        if user_settings and 'assist' in user_settings:
            assist = user_settings['assist']
            level = assist.get('level', 'mid')
            term_depth = assist.get('termDepth', 3)
            
            # Level: low, mid, high
            if level == 'high':
                system_message_content += "\n[Tone: Very Easy] Use extremely simple language suitable for a layman or middle school student. Avoid complex sentences. Use analogies where helpful."
            elif level == 'low':
                system_message_content += "\n[Tone: Professional] Use precise, professional language. Assume the user is knowledgeable."
            else: # mid
                system_message_content += "\n[Tone: Standard] Use clear, standard polite Korean."

            # Term Depth: 1-5
            try:
                depth = int(term_depth)
            except:
                depth = 3
                
            if depth >= 4:
                system_message_content += "\n[Terms: Detailed] When using technical terms, provide detailed definitions and context."
            elif depth <= 2:
                system_message_content += "\n[Terms: Concise] Keep term explanations brief and to the point."

        
        if context:
            system_message_content += (
                "\n\nHere is the relevant context from the document:\n"
                f"{context}\n\n"
                "Instructions:\n"
                "1. Answer the user's question based ONLY on the provided context.\n"
                "2. If the answer is not in the context, say you don't know.\n"
                "3. Cite the context implicitly by referring to the information."
            )
        else:
            system_message_content += "\n\nAnswer the user's question to the best of your ability."

        # Add system message to the beginning
        # Assuming 'messages' contains history excluding the current query? 
        # No, 'messages' passed here usually includes history. 
        # We need to prepend system message.
        
        full_messages = [{"role": "system", "content": system_message_content}] + messages

        try:
            response = await self.client.chat.completions.create(
                model=model or self.model_name,
                messages=full_messages,
                temperature=0.7,
                max_tokens=1000,
            )
            
            assistant_message_content = response.choices[0].message.content
            
            return ChatMessageCreate(
                role="assistant",
                content=assistant_message_content,
                model_name=model or self.model_name,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                citations=[] 
            )
        except Exception as e:
            print(f"ERROR: OpenAI API call failed: {e}")
            return ChatMessageCreate(
                role="assistant",
                content=f"Sorry, I encountered an error while processing your request: {str(e)}",
                model_name=model or self.model_name,
                prompt_tokens=0,
                completion_tokens=0
            )

rag_service = RAGService()
