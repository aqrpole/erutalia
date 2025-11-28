# services/server/app/services/auth_client.py
import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Global client instance
_auth_client = None

def get_auth_client(base_url: str = "http://localhost:8001") -> httpx.AsyncClient:
    """Get or create auth service client"""
    global _auth_client
    if _auth_client is None:
        _auth_client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
    return _auth_client

async def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token with auth service"""
    client = get_auth_client()
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/auth/verify", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Token verification failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Auth service error: {e}")
        return None

async def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user details from auth service"""
    client = get_auth_client()
    try:
        response = await client.get(f"/api/v1/users/{user_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"User fetch failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Auth service error: {e}")
        return None

async def health_check() -> bool:
    """Check if auth service is healthy"""
    client = get_auth_client()
    try:
        response = await client.get("/health")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Auth service health check failed: {e}")
        return False

async def close_auth_client():
    """Close the auth HTTP client"""
    global _auth_client
    if _auth_client:
        await _auth_client.aclose()
        _auth_client = None