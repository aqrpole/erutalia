# services/server/app/services/qdrant_client.py
import logging
from qdrant_client        import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing               import List, Dict, Any, Optional
import uuid
import asyncio
from functools            import partial

from app.core.config      import settings

logger = logging.getLogger(__name__)

# Global client instance
_qdrant_client = None

def get_qdrant_client () -> QdrantClient:
    """Get or create Qdrant client"""
    global _qdrant_client
    for attempt in range (5):
        try:
            if _qdrant_client is None:
                _qdrant_client = QdrantClient (url=settings.QDRANT_URL)
                logger.info (f"Connected to Qdrant URL at {settings.QDRANT_URL}")
                return _qdrant_client
        except Exception as e:
            logger.warning (f"Qdrant connection retry {attempt+1}/5: {e}")
            #await asyncio.sleep (1) #sleep line
    raise RuntimeError ("Qdrant not reachable after retries")

async def ensure_collection_exists(collection_name: str = "documents", vector_size: int = 384):
    """Create collection if it doesn't exist"""
    client = get_qdrant_client()
    try:
        # Run synchronous Qdrant operations in thread pool
        loop = asyncio.get_event_loop()
        collections = await loop.run_in_executor(None, client.get_collections)
        collection_names = [col.name for col in collections.collections]

        if collection_name not in collection_names:
            await loop.run_in_executor(
                None,
                client.create_collection,
                collection_name,
                VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Created Qdrant collection: {collection_name}")
        else:
            logger.info(f"Qdrant collection already exists: {collection_name}")

    except Exception as e:
        logger.error(f"Error ensuring collection exists: {e}")
        raise

async def store_embeddings(documents: List[Dict[str, Any]], collection_name: str = "documents") -> bool:
    """Store document embeddings in Qdrant"""
    client = get_qdrant_client()
    try:
        loop = asyncio.get_event_loop()

        points = []
        for doc in documents:
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=doc["embedding"],
                payload={
                    "text": doc["text"],
                    "file_path": doc.get("file_path", ""),
                    "file_type": doc.get("file_type", ""),
                    "chunk_id": doc.get("chunk_id", 0),
                    "text_length": doc.get("text_length", 0),
                    "source": doc.get("source", ""),
                    "metadata": doc.get("metadata", {})
                }
            )
            points.append(point)

        # Run upsert in thread pool
        await loop.run_in_executor(
            None,
            client.upsert,
            collection_name,
            points
        )

        logger.info(f"Stored {len(points)} documents in Qdrant collection: {collection_name}")
        return True

    except Exception as e:
        logger.error(f"Error storing embeddings in Qdrant: {e}")
        return False

# async def search_similar(
    # query_embedding: List[float], 
    # limit: int = 5, 
    # collection_name: str = "documents",
    # score_threshold: float = 0.7
# ) -> List[Dict[str, Any]]:
async def search_similar(query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
    """Search for similar documents in Qdrant"""
    client = get_qdrant_client()
    try:
        # loop = asyncio.get_event_loop()

        # Run search in thread pool
        # results = await loop.run_in_executor(
            # None, client.search, collection_name, query_embedding, limit,score_threshold)
        results = client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=limit
        )
        """ similar_docs = []
        for result in results:
            similar_docs.append({
                "id": result.id,
                "score": result.score,
                "content": result.payload.get("text", ""),
                "file_path": result.payload.get("file_path", ""),
                "file_type": result.payload.get("file_type", ""),
                "source": result.payload.get("source", ""),
                "metadata": result.payload.get("metadata", {})
            })

        logger.info(f"Found {len(similar_docs)} similar documents with score >= {score_threshold}")
        return similar_docs """
        return [
            {
                "id": hit.id,
                "content": hit.payload.get("content", ""),
                "source": hit.payload.get("source", ""),
                "score": hit.score
            }
            for hit in results
        ]

    except Exception as e:
        logger.error(f"Qdrant search error: {str(e)}")
        return []

async def health_check() -> bool:
    """Check if Qdrant service is healthy"""
    try:
        client = get_qdrant_client()
        loop = asyncio.get_event_loop()
        # Try to list collections to check health
        await loop.run_in_executor(None, client.get_collections)
        return True
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        return False

async def get_collection_info(collection_name: str = "documents") -> Optional[Dict[str, Any]]:
    """Get information about a collection"""
    client = get_qdrant_client()
    try:
        loop = asyncio.get_event_loop()
        collection_info = await loop.run_in_executor(None, client.get_collection, collection_name)

        return {
            "name": collection_name,
            "vectors_count": collection_info.vectors_count,
            "points_count": collection_info.points_count,
            "segments_count": collection_info.segments_count,
            "status": collection_info.status
        }
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        return None

async def close_qdrant_client():
    """Close the Qdrant client"""
    global _qdrant_client
    if _qdrant_client:
        _qdrant_client = None
