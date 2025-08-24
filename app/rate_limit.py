
import time
from fastapi import Request, HTTPException, status

# 简单内存版：令牌桶/固定窗口（单实例适用）
# 生产建议使用 Redis + 滑动窗口算法

class SimpleRateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.buckets: dict[str, tuple[int, float]] = {}

    def check(self, key: str):
        now = time.time()
        count, start = self.buckets.get(key, (0, now))
        if now - start > self.window:
            # reset window
            self.buckets[key] = (1, now)
            return
        if count + 1 > self.limit:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")
        self.buckets[key] = (count + 1, start)

rate_limiter = SimpleRateLimiter(limit=60, window_seconds=60)

async def rate_limit_dependency(request: Request):
    client_ip = request.client.host if request.client else "anonymous"
    key = f"{client_ip}:{request.url.path}"
    rate_limiter.check(key)
