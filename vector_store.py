import numpy as np
from typing import List, Tuple, Union
import google.generativeai as genai
import streamlit as st

class VectorStore:
    """Handles document embeddings and similarity search."""
    
    def __init__(self, api_key: str):
        """
        Initialize the vector store.
        
        Args:
            api_key: Google Gemini API key for embeddings
        """
        genai.configure(api_key=api_key)
        self.model = 'models/text-embedding-004'
        self.documents = []
        self.embeddings = []
    
    def add_documents(self, documents: List[str]) -> None:
        """
        Add documents to the vector store and generate embeddings.
        
        Args:
            documents: List of document chunks to add
            
        Raises:
            Exception: If embedding generation fails
        """
        try:
            # Generate embeddings for all documents
            embeddings = self._generate_embeddings(documents)
            
            # Store documents and embeddings
            self.documents = documents
            self.embeddings = embeddings
            
        except Exception as e:
            raise Exception(f"Failed to add documents to vector store: {str(e)}")
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Google Gemini.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            Exception: If API call fails
        """
        try:
            embeddings = []
            for text in texts:
                # Generate embedding for each text
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            
            return embeddings
            
        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")
    
    def similarity_search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Find the most similar documents to a query.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of tuples (document, similarity_score)
            
        Raises:
            Exception: If search fails or no documents are stored
        """
        if not self.documents or not self.embeddings:
            raise Exception("No documents in vector store. Please upload and process a document first.")
        
        try:
            # Generate embedding for query
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = result['embedding']
            
            # Calculate cosine similarities
            similarities = []
            for i, doc_embedding in enumerate(self.embeddings):
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append((self.documents[i], similarity))
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            raise Exception(f"Failed to perform similarity search: {str(e)}")
    
    def _cosine_similarity(self, vec1: Union[List[float], np.ndarray], vec2: Union[List[float], np.ndarray]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score between -1 and 1
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        # Calculate dot product
        dot_product = np.dot(vec1, vec2)
        
        # Calculate magnitudes
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        return float(similarity)
    
    def get_document_count(self) -> int:
        """Get the number of documents in the store."""
        return len(self.documents)
    
    def clear(self) -> None:
        """Clear all documents and embeddings from the store."""
        self.documents = []
        self.embeddings = []
