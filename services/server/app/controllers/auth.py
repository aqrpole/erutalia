from fastapi import APIRouter, Depends
from datetime import datetime
from app.schemas import HealthResponse
from app.services.auth_client import AuthClient

router = APIRouter()  # This line is crucial
auth_client = AuthClient()

@router.get("/login")
async def login():
    return {"message": "Login endpoint"}

@router.post("/register")
async def register():
    return {"message": "Register endpoint"}

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
        "auth_service": "unknown"
    }
    # TODO: Check database (already checked in lifespan)
    
    # Check Auth Service
    try:
        auth_healthy = await auth_client.health_check()
        services["auth_service"] = "healthy" if auth_healthy else "unhealthy"
    except Exception as e:
        services["auth_service"] = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if all("healthy" in status for status in services.values()) else "degraded"
    
    return {
        "status": overall_status,
        "services": services,
        "timestamp": datetime.now()
    }
