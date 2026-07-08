from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import X_API_KEY

api_key_header = APIKeyHeader(
    name="X-API-KEY",
    scheme_name="X-API-KEY",
    description="Enter the API key from the X_API_KEY environment variable",
    auto_error=False,
)


def require_api_key(
    api_key: str = Security(api_key_header)
):
    if not X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="X_API_KEY is not configured",
        )

    if api_key != X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-KEY",
        )

    return True