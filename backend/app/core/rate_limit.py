from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import Depends, HTTPException, Request, status

from app.core.config import Settings, get_settings

_request_log: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def _client_key(request: Request) -> str:
    client_host = request.client.host if request.client else "unknown"
    return f"{client_host}:{request.url.path}"


def require_rate_limit(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> None:
    limit = settings.rate_limit_requests
    window = settings.rate_limit_window_seconds
    if limit <= 0 or window <= 0:
        return

    now = monotonic()
    cutoff = now - window
    key = _client_key(request)

    with _lock:
        timestamps = _request_log[key]
        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

        if len(timestamps) >= limit:
            retry_after = max(1, int(window - (now - timestamps[0])))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(retry_after)},
            )

        timestamps.append(now)
