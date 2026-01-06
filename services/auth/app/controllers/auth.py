# services/auth/app/controllers/auth.py
from fastapi                      import APIRouter, Depends, HTTPException, status
from fastapi.security             import HTTPBearer
from schemas.token                import Token, LoginRequest, RefreshTokenRequest
from schemas.user                 import UserCreate, UserResponse
from services.auth                import AuthService
from repositories.user_repository import UserRepository
from core.database                import get_db
from sqlalchemy.ext.asyncio       import AsyncSession
import logging

router   = APIRouter ()
security = HTTPBearer ()

@router.post ("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user_repo    = UserRepository (db)
    auth_service = AuthService (user_repo)

    import logging
    logging.info (f"[LOGIN]---------------- Attempt email={login_data.email} pass={login_data.password}")
    token = await auth_service.login (login_data.email, login_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return token

@router.post ("/refresh", response_model=Token)
async def refresh_token (
    request: RefreshTokenRequest,  # Accept body not query param
    db     : AsyncSession = Depends (get_db)
):
    user_repo    = UserRepository (db)
    auth_service = AuthService (user_repo)

    import logging
    logging.info (f"rfersh -------------------- token body check : {refresh_token} {request.refresh_token} ")
    token = await auth_service.refresh_token (request.refresh_token)
    if not token:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail     ="Invalid refresh token"
        )

    return token

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    import logging
    logging.info (f"Received password: {user_data.password} (length: {len(user_data.password)})")

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

    try:
        user = await user_repo.create_user(user_data)
    except ValueError as e:
        # This will catch bcrypt 72-byte limit error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail     =str(e)
        )
    except Exception as e:
        logging.exception (f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail     =f"Registration failed: {str(e)}"
        )
    return user

@router.post ("/validate")
async def validate_token (token: str = Depends (security)):
    from core.security import verify_token

    payload = verify_token (token.credentials, token_type="refresh")
    if not payload:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail     ="Invalid token"
        )
    return {"valid": True, "user_id": payload.get ("sub")}

@router.post ("/logout", status_code=204)
async def logout (
    request : RefreshTokenRequest,
    db      : AsyncSession = Depends (get_db)
):
    auth_service = AuthService (UserRepository (db))
    await auth_service.logout (request.refresh_token)

    return {"message": "Logged out successfully"}
