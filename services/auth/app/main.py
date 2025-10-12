# services/auth-service/app/main.py
import logging
import sys
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import init_db, close_db, check_database_health
from app.controllers.auth import router as auth_router
from app.utils.logging import setup_logging

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Auth Service...")

    # Initialize database with error handling
    db_success = await init_db()
    if not db_success:
        logger.critical("❌ Auth Service cannot start without database connection")
        # Don't start the service if database is not available
        sys.exit(1) # uncomment only if do not want smooth exit

    logger.info("✅ Auth Service started successfully")

    yield

    # Shutdown
    logger.info("🛑 Shutting down Auth Service...")
    await close_db()
    logger.info("✅ Auth Service stopped gracefully")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint with database verification"""
    try:
        db_healthy = await check_database_health()
        if not db_healthy:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "service": "auth",
                    "database": "unavailable",
                    "message": "Database connection failed"
                }
            )

        return {
            "status": "healthy",
            "service": "auth",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"  # You'd use actual timestamp
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "auth",
                "error": str(e)
            }
        )

@app.get("/health/ready")
async def readiness_check():
    """Readiness check for Kubernetes/docker"""
    db_healthy = await check_database_health()
    if db_healthy:
        return {"status": "ready"}
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": "Database unavailable"}
        )

@app.get("/health/live")
async def liveness_check():
    """Liveness check for Kubernetes/docker"""
    return {"status": "alive"}

@app.get("/")
async def root():
    return {"message": "University LLM Chatbot - Auth Service"}

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info"
        )
    except Exception as e:
        logger.critical(f"Failed to start Auth Service: {e}")
        sys.exit(1)
