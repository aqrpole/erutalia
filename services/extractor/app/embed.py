# services/extractor/app/embed.py
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for text documents"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """Load the embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not available, using fallback embeddings")
            self.model = None

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if self.model is None:
            self.load_model()

        if self.model is None:
            # Fallback: return random embeddings if model not available
            return np.random.randn(384).tolist()

        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Fallback to random embeddings
            return np.random.randn(384).tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if self.model is None:
            self.load_model()

        if self.model is None:
            # Fallback: return random embeddings
            return [np.random.randn(384).tolist() for _ in texts]

        try:
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [np.random.randn(384).tolist() for _ in texts]

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        if self.model is None:
            self.load_model()

        if self.model is None:
            return 384  # Default dimension for fallback

        return self.model.get_sentence_embedding_dimension()

    def process_document_with_embeddings(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a document and generate embeddings with metadata"""
        embedding = self.generate_embedding(text)

        result = {
            "text": text,
            "embedding": embedding,
            "embedding_dimension": len(embedding),
            "text_length": len(text)
        }

        if metadata:
            result.update(metadata)

        return result

    def process_chunks(self, chunks: List[str], metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Process text chunks and generate embeddings for each chunk"""
        embeddings = self.generate_embeddings_batch(chunks)

        results = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            result = {
                "chunk_id": i,
                "text": chunk,
                "embedding": embedding,
                "embedding_dimension": len(embedding),
                "text_length": len(chunk)
            }

            if metadata:
                result.update(metadata)

            results.append(result)

        return results
