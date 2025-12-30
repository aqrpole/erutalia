# services/auth-service/app/core/security.py
from datetime        import datetime, timedelta
from typing          import Optional
from jose            import JWTError, jwt
from passlib.context import CryptContext
from core.config     import settings
import hashlib

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prehash (password: str) -> str:
    # Convert any-length password to fixed-length input (32 bytes) for bcrypt
    # (max 72 bytes)
    return hashlib.sha256 (password.encode ("utf-8")).hexdigest ()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #return pwd_context.verify(plain_password, hashed_password)
    return pwd_context.verify (_prehash (plain_password), hashed_password)

def get_password_hash(password: str) -> str:
    import logging
    logging.info (f"Hashing password: {password!r} length={len(password)}")
    return pwd_context.hash (_prehash (password))
    #return pwd_context.hash(password)

# JWT Token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token (token: str, token_type: Optional[str] = None):
    try:
        import logging
        logging.info (f"jwt------------------------ module is: {jwt}")
        payload = jwt.decode (
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            #audience  ="erutalia-api",
            #issuer    ="auth-service"
        )

        if token_type == "refresh" and payload.get ("type") != "refresh":
            return None

        return payload
    except JWTError:
        return None
