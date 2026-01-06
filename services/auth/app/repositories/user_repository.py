# services/auth-service/app/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy             import select, update, delete
from sqlalchemy.sql         import func
from models.user            import User, RefreshToken
from schemas.user           import UserCreate, UserUpdate
from core.security          import get_password_hash, verify_password
from typing                 import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id (self, user_id: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            role=user_data.role,
            hashed_password=hashed_password
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email (email)

        if not user:
            return None
        if not verify_password (password, user.hashed_password):
            return None
        return user

    async def update_last_login(self, user_id: str):
        stmt = update(User).where(User.id == user_id).values(last_login=func.now())
        await self.session.execute(stmt)
        await self.session.commit()

    async def revoke_refresh_token (self, user_id: str, token: str) -> None:
        await self.session.execute (
            delete (RefreshToken).where (
                RefreshToken.user_id == user_id,
                RefreshToken.token   == token
            )
        )
        await self.session.commit ()

    async def store_refresh_token (self, user_id: str, token: str):
        # remove existing token(s) for this user
        await self.session.execute (
            delete (RefreshToken).where (RefreshToken.user_id == user_id)
        )

        refresh_token = RefreshToken (
            user_id = user_id,
            token   = token
        )

        self.session.add (refresh_token)
        await self.session.commit ()

    async def verify_refresh_token (self, user_id: str, token: str) -> bool:
        result = await self.session.execute (
            select (RefreshToken).where (
                RefreshToken.user_id == user_id,
                RefreshToken.token   == token
            )
        )
        return result.scalar_one_or_none() is not None

    async def update_refresh_token (self, user_id: str, old_token: str,
                                    new_token: str):
        await self.session.execute (
            delete (RefreshToken).where (
                RefreshToken.user_id == user_id,
                RefreshToken.token   == old_token
            )
        )

        self.session.add (
            RefreshToken (user_id=user_id, token=new_token)
        )
        await self.session.commit ()

    async def delete_user (self, user_id: str) -> None:
        await self.session.execute (
            delete (User).where (User.id == user_id)
        )
        await self.session.commit ()
