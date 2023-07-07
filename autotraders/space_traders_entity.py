import json

from autotraders import AutoTradersSession
from autotraders.error import SpaceTradersException


class SpaceTradersEntity:
    def __init__(self, session: AutoTradersSession, action_url, data=None):
        self.session: AutoTradersSession = session
        self.action_url = session.base_url + action_url
        if self.action_url[-1] != "/":
            self.action_url += "/"
        self.update(data)

    def get(self, action: str = None) -> dict:
        if action is None:
            r = self.session.get(
                self.action_url[0 : len(self.action_url) - 1]  # noqa E203
            )
        else:
            r = self.session.get(
                self.action_url + action,
            )
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(j["error"], r.status_code)
        return j

    def post(self, action: str, data=None) -> dict:
        self.session.headers["Content-Type"] = "application/json"
        if data is not None:
            r = self.session.post(
                self.action_url + action,
                data=json.dumps(data),
            )
        else:
            r = self.session.post(self.action_url + action)
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(j["error"], r.status_code)
        return j

    def update(self, data: dict = None):
        """
        :param data: If you have data from an api requests, you can provide it here. If not provided, an API request
        will be sent.
        :raise IOException: If the server fails
        """
        pass
