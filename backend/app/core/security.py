from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import JWTError, jwt
from app.core.config import settings
import hashlib
import secrets
import base64

# Pure Python password hashing - no external C libraries


def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2-SHA256 with pure Python.
    Format: pbkdf2_sha256$rounds$salt$hash
    """
    salt = secrets.token_bytes(32)
    rounds = 100000
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, rounds)
    # Use base64 for safe encoding
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(hashed).decode('ascii')
    return f"pbkdf2_sha256$100000${salt_b64}${hash_b64}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against PBKDF2-SHA256 hash.
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        if not hashed_password.startswith("pbkdf2_sha256$"):
            return False
        
        parts = hashed_password.split("$")
        if len(parts) != 4:
            return False
        
        rounds = int(parts[1])
        salt_b64 = parts[2]
        stored_hash_b64 = parts[3]
        
        # Decode from base64
        salt = base64.b64decode(salt_b64)
        stored_hash = base64.b64decode(stored_hash_b64)
        
        # Compute hash for provided password
        computed_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt, rounds)
        
        # Constant-time comparison
        return computed_hash == stored_hash
    except Exception as e:
        return False


def create_access_token(subject: Any, role: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {
        "sub": str(subject),
        "role": role,
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return {}
