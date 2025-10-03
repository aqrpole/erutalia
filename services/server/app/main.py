import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.logging import setup_logging
from app.core.database import init_db, close_db

# Setup logging
logger = setup_logging()

# Import routers with error handling
try:
    from app.controllers.health import router as health_router
    health_available = True
except ImportError as e:
    logger.warning(f"Health router not available: {e}")
    health_available = False

try:
    from app.controllers.auth import router as auth_router
    auth_available = True
except ImportError as e:
    logger.warning(f"Auth router not available: {e}")
    auth_available = False

try:
    from app.controllers.chat import router as chat_router
    chat_available = True
except ImportError as e:
    logger.warning(f"Chat router not available: {e}")
    chat_available = False

try:
    from app.controllers.conversations import router as conversations_router
    conversations_available = True
except ImportError as e:
    logger.warning(f"Conversations router not available: {e}")
    conversations_available = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting University LLM Chatbot API Server")
    
    # Initialize database connection with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await init_db()
            logger.info("Database connection established successfully")
            break
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)  # Wait 2 seconds before retry
            else:
                logger.error("All database connection attempts failed. Starting without database.")
    
    logger.info("API Server started successfully")
    
    yield    
    logger.info("API Server started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down API Server")
    await close_db()

# Create FastAPI app
app = FastAPI(
    title="University LLM Chatbot API",
    description="API server for University LLM Chatbot with Qdrant and Ollama integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for Next.js build)
app.mount("/static", StaticFiles(directory="public"), name="static")

# Include available routers
if health_available:
    app.include_router(health_router, prefix="/api/v1", tags=["health"])
    logger.info("Health router included")

if auth_available:
    app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
    logger.info("Auth router included")

if chat_available:
    app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
    logger.info("Chat router included")

if conversations_available:
    app.include_router(conversations_router, prefix="/api/v1", tags=["conversations"])
    logger.info("Conversations router included")

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}", extra={"status_code": exc.status_code})
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

@app.get("/")
async def root():
    return {"message": "University LLM Chatbot API", "version": "1.0.0"}

@app.get("/ping")
async def root():
    return {"message": "pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None
    )
