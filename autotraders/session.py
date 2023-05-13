import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_session(token):
    """Creates a session with the provided token."""
    s = requests.Session()
    s.auth = BearerAuth(token)
    return s
