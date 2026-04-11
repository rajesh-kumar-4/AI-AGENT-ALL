from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .config import settings
from .exceptions import UnauthorizedException

bearer_scheme = HTTPBearer(auto_error=False)


def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )

    secret = settings.api_key
    if credentials.credentials != secret:
        raise UnauthorizedException("Invalid API token.")

    return credentials.credentials
