from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status


class RateLimiter:
    def __init__(
        self,
        max_requests: int,
        window_seconds: int
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self._requests = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> None:
        now = monotonic()

        with self._lock:
            request_times = self._requests[key]

            while (
                request_times
                and now - request_times[0] >= self.window_seconds
            ):
                request_times.popleft()

            if len(request_times) >= self.max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later.",
                    headers={
                        "Retry-After": str(self.window_seconds)
                    }
                )

            request_times.append(now)


def get_client_ip(request: Request) -> str:
    if request.client is None:
        return "unknown"

    return request.client.host


login_rate_limiter = RateLimiter(
    max_requests=5,
    window_seconds=60
)

register_rate_limiter = RateLimiter(
    max_requests=5,
    window_seconds=60
)

question_rate_limiter = RateLimiter(
    max_requests=30,
    window_seconds=60
)

answer_rate_limiter = RateLimiter(
    max_requests=120,
    window_seconds=60
)

result_rate_limiter = RateLimiter(
    max_requests=20,
    window_seconds=60
)