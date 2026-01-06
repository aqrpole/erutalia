# services/auth/app/controllers/user.py
from fastapi                      import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio       import AsyncSession
from repositories.user_repository import UserRepository
from core.database                import get_db
from schemas.user                 import UserResponse
from services.user                import UserService
from fastapi                      import status
from core.security                import require_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    # You'd implement pagination here
    return {"users": [], "skip": skip, "limit": limit}

@router.delete ("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user (
    user_id: str,
    _: dict          = Depends (require_admin), #admin-only
    db: AsyncSession = Depends (get_db)
):
    user_repo    = UserRepository (db)
    user_service = UserService (user_repo)

    deleted = await user_service.delete_user (user_id)
    if not deleted:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "User not found"
        )
