# services/auth/app/services/user.py
from datetime                     import datetime, timedelta
from typing                       import Optional
from repositories.user_repository import UserRepository
from schemas.token                import Token
from core.security                import create_access_token, create_refresh_token, verify_token
from models.user                  import RefreshToken
from core.config                  import settings

class UserService:
    def __init__ (self, user_repo):
        self.user_repo = user_repo

    async def delete_user (self, user_id: str) -> bool:
        user = await self.user_repo.get_user_by_id (user_id)
        if not user:
            return False

        await self.user_repo.delete_user (user_id)
        return True
