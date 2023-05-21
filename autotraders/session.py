import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class AutoTradersSession(requests.Session):
    def __init__(self, base_url="https://api.spacetraders.io/v2/"):
        super().__init__()
        self.base_url = base_url


def get_session(token):
    """Creates a session with the provided token."""
    s = AutoTradersSession()
    s.auth = BearerAuth(token)
    return s
