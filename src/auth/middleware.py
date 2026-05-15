from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from src.auth.revoke import is_token_revoked
from src.config import settings


class JWTAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        public_routes = [
            "/auth/login",
            "/auth/register"
        ]

        if request.url.path in public_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Missing token"
            )

        try:
            scheme, token = auth_header.split()

            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid auth scheme"
                )

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            jti = payload.get("jti")

            if await is_token_revoked(jti):
                raise HTTPException(
                    status_code=401,
                    detail="Token revoked"
                )

            request.state.user = payload

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return await call_next(request)