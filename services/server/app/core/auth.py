# services/api-server/app/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from app.services.auth_client import AuthClient

security = HTTPBearer()
auth_client = AuthClient()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Dependency to get current user from JWT token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    token = credentials.credentials
    user_data = await auth_client.validate_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user_data

async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
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

# Specific role dependencies
require_admin = require_role("admin")
require_editor = require_role("editor") 
require_user = require_role("user")
require_viewer = require_role("viewer")