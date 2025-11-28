"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from datetime import datetime
from app.schemas import HealthResponse
from app.services.auth_client import health_check as auth_health_check
from app.services.ollama_client import health_check as ollama_health_check
from app.services.bedrock_client import health_check as bedrock_health_check

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service dependencies"""
    services = {
        "api_server": "healthy",
        "database": "healthy", 
        "auth_service": "unknown",
        "ollama_service": "unknown",
        "bedrock_service": "unknown"
    }
    
    # Check Auth Service
    try:
        auth_healthy = await auth_health_check()
        services["auth_service"] = "healthy" if auth_healthy else "unhealthy"
    except Exception as e:
        services["auth_service"] = f"unhealthy: {str(e)}"
    
    # Check Ollama Service
    try:
        ollama_healthy = await ollama_health_check()
        services["ollama_service"] = "healthy" if ollama_healthy else "unhealthy"
    except Exception as e:
        services["ollama_service"] = f"unhealthy: {str(e)}"
    
    # Check Bedrock Service
    try:
        bedrock_healthy = await bedrock_health_check()
        services["bedrock_service"] = "healthy" if bedrock_healthy else "unhealthy"
    except Exception as e:
        services["bedrock_service"] = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if all("healthy" in status for status in services.values()) else "degraded"
    
    return {
        "status": overall_status,
        "services": services,
        "timestamp": datetime.now()
    }