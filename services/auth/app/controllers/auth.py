# services/auth-service/app/controllers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.schemas.token import Token, LoginRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService
from app.repositories.user_repository import UserRepository
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    
    token = await auth_service.login(login_data.username, login_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return token

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    
    token = await auth_service.refresh_token(refresh_token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    return token

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    
    # Check if user exists
    if await user_repo.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if await user_repo.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = await user_repo.create_user(user_data)
    return user

@router.post("/validate")
async def validate_token(token: str = Depends(security)):
    from app.core.security import verify_token
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"valid": True, "user_id": payload.get("sub")}