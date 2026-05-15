from datetime import datetime
from jose import jwt

from src.redis.redis import redis_client
from src.config import settings


async def revoke_token(token: str):

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    jti = payload["jti"]
    exp = payload["exp"]

    ttl = exp - int(datetime.utcnow().timestamp())

    await redis_client.set(
        f"revoked:{jti}",
        "true",
        ex=ttl
    )


async def is_token_revoked(jti: str):

    result = await redis_client.get(
        f"revoked:{jti}"
    )

    return result is not None