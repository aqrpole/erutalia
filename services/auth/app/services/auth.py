# services/auth-service/app/services/auth.py
from datetime                     import datetime, timedelta
from typing                       import Optional
from repositories.user_repository import UserRepository
from schemas.token                import Token
from core.security                import create_access_token, create_refresh_token, verify_token
from models.user                  import RefreshToken
from core.config                  import settings

class AuthService:
    def __init__ (self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def login (self, email: str, password: str) -> Optional[Token]:
        user = await self.user_repo.authenticate_user (email, password)

        if not user:
            return None

        # Update last login
        await self.user_repo.update_last_login (user.id)

        # Create tokens
        token_data    = {"sub": user.id, "username": user.username, "role": user.role}
        access_token  = create_access_token (token_data)
        refresh_token = create_refresh_token (token_data)

        # Store refresh token (you'd implement this)
        await self.store_refresh_token (user.id, refresh_token)

        return Token (
            access_token =access_token,
            token_type   ="bearer",
            expires_in   =settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token
        )

    async def refresh_token (self, refresh_token: str) -> Optional[Token]:
        payload = verify_token (refresh_token, token_type="refresh")

        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get ("sub")
        user    = await self.user_repo.get_user_by_id (user_id)
        if not user:
            return None

        # Verify refresh token is valid in database
        if not await self.verify_refresh_token (user_id, refresh_token):
            return None

        # Create new tokens
        token_data        = {"sub": user.id, "username": user.username, "role": user.role}
        new_access_token  = create_access_token (token_data)
        new_refresh_token = create_refresh_token (token_data)

        # Update refresh token
        await self.update_refresh_token (user_id, refresh_token, new_refresh_token)

        return Token(
            access_token =new_access_token,
            token_type   ="bearer",
            refresh_token=new_refresh_token
        )

    async def store_refresh_token(self, user_id: str, token: str):
        # Implementation for storing refresh tokens
        pass
    
    async def verify_refresh_token(self, user_id: str, token: str) -> bool:
        # Implementation for verifying refresh tokens
        return True
    
    async def update_refresh_token(self, user_id: str, old_token: str, new_token: str):
        # Implementation for updating refresh tokens
        pass
