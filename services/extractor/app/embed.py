# services/extractor/app/embed.py
import gc
import numpy as np
from typing import List, Dict, Any
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.utils.idgen import generate_id
from app.config import settings

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for text documents and store in Qdrant"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.qdrant_client = QdrantClient(settings.QDRANT_URL)
        self.embedding_dim = 384  # all-MiniLM-L6-v2 dimension

    def load_model(self):
        """Load the embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            # removing device could make it work for GPU be default
            self.model = SentenceTransformer(self.model_name, device="cpu")
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Loaded embedding model: {self.model_name}, dimension: {self.embedding_dim}")
        except Exception as e:
        #except ImportError:
            #logger.error("sentence-transformers not available. Please install: pip install sentence-transformers")
            logger.error(e)
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if self.model is None:
            self.load_model()

        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 8) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        """
            Generate embeddings for multiple texts in small batches to avoid memory issues.
            Default batch_size=8 is safe for CPU.
        """
        if self.model is None:
            self.load_model()

        embeddings_all = []

        #try:
        #    embeddings = self.model.encode(texts)
        #    return embeddings.tolist()
        #except Exception as e:
        #    logger.error(f"Error generating batch embeddings: {e}")
        #    raise

        try:
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                batch_embeddings = self.model.encode(batch_texts)
                embeddings_all.extend(batch_embeddings.tolist())
            return embeddings_all
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    # CHANGED: Removed async, fixed parameter signature
    def process_chunks(self, chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> bool:
        """Process chunks and store in Qdrant - SYNCHRONOUS VERSION"""
        try:
            collection_name = metadata.get("collection", settings.QDRANT_COLLECTION)
            source = metadata.get("file_path", "unknown")
            batch_size = metadata.get("batch_size", settings.BATCH_SIZE)
            #specific for smaller cpu load
            # Safe embedding batch size (separate from Qdrant upload)
            embedding_batch_size = metadata.get("embedding_batch_size", settings.EMBEDDING_BATCH_SIZE)

            logger.info(f"Processing {len(chunks)} chunks for collection: {collection_name}")

            # Ensure collection exists
            self._ensure_collection(collection_name)

            # Extract text from chunks for embedding
            texts = [chunk["text"] for chunk in chunks]

            # Generate embeddings in batch
            logger.info("Generating embeddings...")
            embeddings = self.generate_embeddings_batch(texts, batch_size=embedding_batch_size)
            logger.info(f"Generated {len(embeddings)} embeddings")

            # Prepare points for Qdrant
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = models.PointStruct(
                    id=generate_id(),
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        "source": source,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "filename": chunk["metadata"]["filename"],
                        "file_type": chunk["metadata"]["file_type"],
                        "file_size": chunk["metadata"]["file_size"]
                    }
                )
                points.append(point)

            # Upload to Qdrant in batches to avoid memory issues
            logger.info(f"Uploading {len(points)} points to Qdrant in batches of {batch_size}...")

            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                try:
                    operation_info = self.qdrant_client.upsert(
                        collection_name=collection_name,
                        points=batch,
                        wait=True  # Wait for confirmation
                    )
                    logger.info(f"✅ Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
                except Exception as e:
                    logger.error(f"❌ Failed to upload batch {i//batch_size + 1}: {str(e)}")
                    return False
                finally:
                    # 🧹 Cleanup memory after each batch
                    del batch
                    gc.collect()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()

            logger.info(f"✅ Successfully processed {len(points)} chunks from {source}")
            return True

        except Exception as e:
            logger.error(f"❌ Chunk processing failed: {str(e)}")
            return False

    # CHANGED: Removed async
    def _ensure_collection(self, collection_name: str):
        """Ensure Qdrant collection exists - SYNCHRONOUS VERSION"""
        try:
            collections = self.qdrant_client.get_collections()
            existing_collections = [col.name for col in collections.collections]
            
            if collection_name not in existing_collections:
                logger.info(f"Creating collection: {collection_name}")
                self.qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=self.embedding_dim,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"✅ Created collection: {collection_name}")
            else:
                logger.info(f"✅ Collection exists: {collection_name}")
                
        except Exception as e:
            logger.error(f"❌ Collection creation failed: {str(e)}")
            raise

    # CHANGED: Removed async
    def check_qdrant_health(self) -> bool:
        """Check if Qdrant is accessible - SYNCHRONOUS VERSION"""
        try:
            collections = self.qdrant_client.get_collections()
            logger.info("✅ Qdrant connection healthy")
            return True
        except Exception as e:
            logger.error(f"❌ Qdrant health check failed: {str(e)}")
            return False

    # CHANGED: Removed async  
    def check_embedding_health(self) -> bool:
        """Check if embedding model is working - SYNCHRONOUS VERSION"""
        try:
            if self.model is None:
                self.load_model()
            # Test embedding generation with small text
            test_embedding = self.generate_embedding("test")
            is_healthy = len(test_embedding) == self.embedding_dim
            if is_healthy:
                logger.info("✅ Embedding model healthy")
            else:
                logger.error("❌ Embedding model returned wrong dimension")
            return is_healthy
        except Exception as e:
            logger.error(f"❌ Embedding health check failed: {str(e)}")
            return False

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        if self.model is None:
            self.load_model()
        return self.embedding_dim
