# services/server/app/core/auth.py
from fastapi                  import Depends, HTTPException, status
from fastapi.security         import HTTPBearer, HTTPAuthorizationCredentials
from typing                   import Optional, Dict, Any
from app.services.auth_client import verify_token, get_user  # Change to functional imports
import logging

logger   = logging.getLogger(__name__)
security = HTTPBearer()

async def get_current_user (
    credentials: HTTPAuthorizationCredentials = Depends (security)
)-> Dict[str, Any]:
    """Dependency to get current user from JWT token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail     ="Authorization header missing"
        )

    try:
        token = credentials.credentials
        user_data = await verify_token (token)

        if not user_data:
            raise HTTPException (
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail     ="Invalid or expired token",
                headers    ={"WWW-Authenticate": "Bearer"},
            )

        return user_data
    except Exception as e:
        logger.error (f"Authentication error: {e}")
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail     ="Could not validate credentials",
            headers    ={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    """Dependency to get current active user"""
    # You can add additional checks here if needed
    # For example, check if user is active, verified, etc.
    return current_user

# Role-based access control
def require_role(required_role: str):
    """Factory function to create role-based dependencies"""
    async def role_checker(
        current_user: Dict[str, Any] = Depends(get_current_active_user)
    ) -> Dict[str, Any]:
        user_role = current_user.get("role", "user")

        # Define role hierarchy
        role_hierarchy = {
            "viewer": 1,
            "user": 2,
            "editor": 3,
            "admin": 4
        }

        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role. Current role: {user_role}"
            )

        return current_user

    return role_checker

async def require_user(current_user: dict = Depends(get_current_active_user)):
    """Require user authentication"""
    return current_user

async def require_admin(current_user: dict = Depends(get_current_active_user)):
    """Require admin privileges"""
    # Check if user has admin role
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges"
        )
    return current_user

# Specific role dependencies
require_admin = require_role("admin")
require_editor = require_role("editor") 
require_user = require_role("user")
require_viewer = require_role("viewer")
