from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from jwt import PyJWTError
from pydantic import ValidationError

from src.auth.schemas import TokenPayload
from src.config import settings
from src.users.models import User


def create_access_token(user: User, not_expire: bool = False):
    if not_expire:
        expire = datetime.utcnow() + timedelta(days=36500)
    else:
        expire = datetime.utcnow() + timedelta(seconds=15)

    encoded_jwt = jwt.encode(
        {"exp": expire, "user_id": str(user.id)},
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def get_token_data(token: str) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])
        token_data = TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data
