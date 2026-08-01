"""
Rate limiter with backoff, delay, and random jitter support.
"""

import asyncio
import random
import time
from typing import Callable, Optional, TypeVar, Any

T = TypeVar("T")


class RateLimiter:
    """
    Asynchronous rate limiter managing request intervals, delays, and random jitter.
    """

    def __init__(
        self,
        requests_per_second: float = 5.0,
        delay_seconds: float = 0.0,
        jitter: bool = True,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ):
        self.min_interval = 1.0 / max(requests_per_second, 0.001)
        self.delay_seconds = delay_seconds
        self.jitter = jitter
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._last_request_time: float = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire rate limiting slot with interval throttling and optional jitter."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request_time
            wait_time = self.min_interval - elapsed

            if wait_time > 0:
                await asyncio.sleep(wait_time)

            if self.delay_seconds > 0:
                actual_delay = self.delay_seconds
                if self.jitter:
                    actual_delay += random.uniform(0, self.delay_seconds * 0.5)
                await asyncio.sleep(actual_delay)

            self._last_request_time = time.monotonic()

    async def execute_with_retry(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute async function with rate limiting and exponential backoff retry."""
        attempt = 0
        while True:
            await self.acquire()
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                attempt += 1
                if attempt > self.max_retries:
                    raise exc
                sleep_time = (self.backoff_factor ** attempt)
                if self.jitter:
                    sleep_time += random.uniform(0, 0.5)
                await asyncio.sleep(sleep_time)
