from __future__ import annotations

import time
from typing import Optional, Any

import requests
from requests import Response
from requests.sessions import RequestsCookieJar
from requests_ratelimiter import LimiterSession


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class AutoTradersSession(LimiterSession):
    def __init__(self, base_url="https://api.spacetraders.io/v2/"):
        super().__init__(per_second=2, burst_rate=10, limit_statuses=[429, 502])
        self.base_url = base_url
        self.retries = 5
        self.retry_time = 2

    def request(
        self,
        method: str | bytes,
        url: str | bytes,
        params: Any | None = None,
        data: Any | None = None,
        headers: Any | None = None,
        cookies: None | RequestsCookieJar | Any = None,
        files: Any | None = None,
        auth: Any | None = None,
        timeout: Any | None = None,
        allow_redirects: bool = None,
        proxies: Any | None = None,
        hooks: Any | None = None,
        stream: bool | None = None,
        verify: Any | None = None,
        cert: Any | None = None,
        json: Any | None = None,
    ) -> Response:
        """Just like the normal method, but retries if the status code is 429."""
        resp = super().request(
            method,
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )
        if resp.status_code == 429:
            i = 1
            while i < self.retries and resp.status_code == 429:
                time.sleep(self.retry_time)
                resp = super().request(
                    method,
                    url,
                    params,
                    data,
                    headers,
                    cookies,
                    files,
                    auth,
                    timeout,
                    allow_redirects,
                    proxies,
                    hooks,
                    stream,
                    verify,
                    cert,
                    json,
                )
        return resp


def get_session(token: Optional[str] = None) -> AutoTradersSession:
    """Creates a session with the provided token."""
    s = AutoTradersSession()
    if token is not None:
        s.auth = BearerAuth(token)
    return s
