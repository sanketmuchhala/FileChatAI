from typing import List, Tuple
from openai import OpenAI
from vector_store import VectorStore

class ChatHandler:
    """Handles chat interactions with document context."""
    
    def __init__(self, api_key: str, vector_store: VectorStore):
        """
        Initialize the chat handler.
        
        Args:
            api_key: DeepSeek API key
            vector_store: Vector store containing document embeddings
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.vector_store = vector_store
        # Using DeepSeek's chat model which is cost-effective and powerful
        self.model = "deepseek-chat"
    
    def generate_response(self, user_query: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Generate a response to user query using retrieved document context.
        
        Args:
            user_query: User's question or message
            top_k: Number of document chunks to retrieve for context
            
        Returns:
            Tuple of (response_text, source_chunks)
            
        Raises:
            Exception: If response generation fails
        """
        try:
            # Retrieve relevant document chunks
            similar_docs = self.vector_store.similarity_search(user_query, top_k=top_k)
            
            if not similar_docs:
                return "I couldn't find any relevant information in the document to answer your question.", []
            
            # Extract document chunks and their similarity scores
            context_chunks = []
            source_chunks = []
            
            for doc, similarity in similar_docs:
                # Only include chunks with reasonable similarity (> 0.1)
                if similarity > 0.1:
                    context_chunks.append(doc)
                    source_chunks.append(doc)
            
            if not context_chunks:
                return "I couldn't find sufficiently relevant information in the document to answer your question confidently.", []
            
            # Create context string
            context = "\n\n".join([f"Context {i+1}: {chunk}" for i, chunk in enumerate(context_chunks)])
            
            # Create the prompt
            system_prompt = """You are a helpful AI assistant that answers questions based on provided document context. 

Instructions:
1. Answer the user's question using ONLY the information provided in the context
2. If the context doesn't contain enough information to answer the question, say so clearly
3. Be accurate and cite relevant parts of the context in your response
4. If the user's question is not related to the document content, politely redirect them to ask about the document
5. Provide clear, concise, and helpful answers
6. Do not make up information that is not in the provided context"""

            user_prompt = f"""Context from the document:
{context}

User Question: {user_query}

Please answer the user's question based on the provided context. If the context doesn't contain relevant information, please say so clearly."""

            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more focused responses
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            
            return response_text, source_chunks
            
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def _format_context(self, documents: List[Tuple[str, float]]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            documents: List of (document_chunk, similarity_score) tuples
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant context found."
        
        context_parts = []
        for i, (doc, score) in enumerate(documents, 1):
            context_parts.append(f"[Context {i}] (Relevance: {score:.2f})\n{doc}")
        
        return "\n\n".join(context_parts)
