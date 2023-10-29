from __future__ import annotations

import time

from httpx import Response, Client
from pyrate_limiter import Limiter, Rate, Duration, BucketFullException


class AutoTradersSession(Client):
    def __init__(
        self, token=None, http2=True, base_url="https://api.spacetraders.io/v2/"
    ):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        super().__init__(headers=headers, http2=http2, base_url=base_url)
        self.limiter = Limiter(Rate(2, Duration.SECOND))
        self.burst_limiter = Limiter(Rate(10, Duration.SECOND * 10))
        self.retries = 5
        self.retry_sleep_time = 2
        self.rate_limiter_sleep_time = 0.1

    def request(
        self,
        method: str,
        url,
        *args,
        **kwargs,
    ) -> Response:
        """Just like the normal method, but retries if the status code is 429."""
        acquired = False
        while not acquired:
            try:
                self.limiter.try_acquire(url)
                acquired = True
            except BucketFullException:
                try:
                    self.limiter.try_acquire(url)
                    acquired = True
                except BucketFullException:
                    time.sleep(self.rate_limiter_sleep_time)
        resp = super().request(
            method,
            url,
            *args,
            **kwargs,
        )
        if resp.status_code == 429:
            i = 0
            while i < self.retries and resp.status_code == 429:
                time.sleep(self.retry_sleep_time)
                resp = super().request(
                    method,
                    url,
                    *args,
                    **kwargs,
                )
                i += 1
        return resp
