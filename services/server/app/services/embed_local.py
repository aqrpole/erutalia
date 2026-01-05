# erutalia/services/server/app/services/embed_local.py
import asyncio
import logging
from typing                import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger (__name__)

# Load model once (module-level singleton)
_MODEL_NAME = "all-MiniLM-L6-v2"
_model      = None


def _load_model():
    global _model
    if _model is None:
        logger.info (f"🔹 Loading embedding model: {_MODEL_NAME}")
        _model = SentenceTransformer (_MODEL_NAME)
        return _model


async def generate_embeddings (texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts (async-friendly).
    """
    if not texts:
        return []

    model = _load_model ()
    loop  = asyncio.get_event_loop ()

    embeddings = await loop.run_in_executor (
        None,
        model.encode,
        texts,
    )

    return embeddings.tolist ()

