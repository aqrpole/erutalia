# services/auth-service/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db, close_db
from app.controllers import auth, users
from app.utils.logging import setup_logging

logger = setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
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
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Auth Service started")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    logger.info("Auth Service stopped")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth"}