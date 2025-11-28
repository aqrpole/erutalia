# services/server/app/services/ollama_client.py
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from app.core.config import settings

# Import the Bedrock client
try:
    from app.services.bedrock_client import generate_bedrock_response
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False
    logging.warning("Bedrock client not available")

logger = logging.getLogger(__name__)

# Global session variable
_http_session = None

async def get_session():
    """Get or create HTTP session"""
    global _http_session
    if _http_session is None:
        _http_session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {settings.OLLAMA_API_KEY}"}
        )
    return _http_session

async def generate_response(prompt: str, context: List[Dict[str, Any]] = None) -> str:
    """Generate response using either Bedrock or Ollama as fallback"""
    # Try Bedrock first if enabled and available
    if settings.USE_BEDROCK and BEDROCK_AVAILABLE:
        try:
            logger.info("Using Bedrock for response generation")
            response = await generate_bedrock_response(prompt, context)
            return response
        except Exception as e:
            logger.warning(f"Bedrock failed: {e}")
            if not settings.FALLBACK_TO_OLLAMA:
                raise

    # Fallback to Ollama
    logger.info("Falling back to Ollama for response generation")
    return await generate_ollama_response(prompt, context)

async def generate_ollama_response(prompt: str, context: List[Dict[str, Any]] = None) -> str:
    """Generate response using Ollama"""
    session = await get_session()

    if context:
        context_text = "\n".join([doc.get("text", doc.get("content", "")) for doc in context])
        enhanced_prompt = f"Context: {context_text}\n\nUser Question: {prompt}"
    else:
        enhanced_prompt = prompt

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": enhanced_prompt,
        "stream": False,
        "context": []
    }

    try:
        async with session.post(f"{settings.OLLAMA_AWS_URL}/api/generate", json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("response", "")
            else:
                logger.error(f"Ollama API error: {response.status}")
                raise Exception(f"Ollama API returned {response.status}")
    except Exception as e:
        logger.error(f"Ollama request failed: {str(e)}")
        raise

async def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings for text using Ollama"""
    session = await get_session()

    payload = {
        "model": settings.EMBEDDING_MODEL,
        "prompt": text
    }

    try:
        async with session.post(f"{settings.OLLAMA_AWS_URL}/api/embeddings", json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("embedding", [])
            else:
                logger.error(f"Ollama embeddings error: {response.status}")
                raise Exception(f"Ollama embeddings returned {response.status}")
    except Exception as e:
        logger.error(f"Ollama embeddings failed: {str(e)}")
        raise

async def health_check() -> bool:
    """Check if Ollama service is healthy"""
    try:
        session = await get_session()
        async with session.get(f"{settings.OLLAMA_AWS_URL}/api/tags") as response:
            return response.status == 200
    except Exception as e:
        logger.error(f"Ollama health check failed: {str(e)}")
        return False

async def close_session():
    """Close the HTTP session"""
    global _http_session
    if _http_session:
        await _http_session.close()
        _http_session = None
