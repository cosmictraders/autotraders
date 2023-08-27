from autotraders import AutoTradersSession
from autotraders.error import SpaceTradersException


class SpaceTradersEntity:
    def __init__(self, session: AutoTradersSession, action_url, data=None):
        self.session: AutoTradersSession = session
        self.action_url = session.b_url + action_url
        if self.action_url[-1] != "/":
            self.action_url += "/"
        self.json = {}
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
            raise SpaceTradersException(j["error"], r.url, r.status_code, r.request.headers, r.headers)
        return j

    def post(self, action: str, data=None) -> dict:
        self.session.headers["Content-Type"] = "application/json"
        if data is not None:
            r = self.session.post(
                self.action_url + action,
                json=data,
            )
        else:
            r = self.session.post(self.action_url + action)
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(j["error"], r.url, r.status_code, r.request.headers, r.headers)
        return j

    def patch(self, action: str, data=None) -> dict:
        self.session.headers["Content-Type"] = "application/json"
        if data is not None:
            r = self.session.patch(
                self.action_url + action,
                json=data,
            )
        else:
            r = self.session.patch(self.action_url + action)
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(j["error"], r.url, r.status_code, r.request.headers, r.headers)
        return j

    def _update(self, data: dict = None, special_endpoint: str = None):
        """
        :param data: If you have data from an api requests, you can provide it here. If not provided, an API request will be sent.

        :raise IOException: If the server fails
        """
        if data is None:
            if special_endpoint is not None:
                self.json = self.get(special_endpoint)["data"]
            else:
                self.json = self.get()["data"]
            return self.json
        else:
            for key in data:
                self.json[key] = data[key]
            return data

    def update_attr(self, mappings, data):
        for mapping in mappings:
            if mapping in data:
                mapping_info = mappings.get(mapping, {})
                t = mapping_info.get("type", None)
                if t == "object":
                    setattr(
                        self,
                        mapping,
                        mapping_info["class"](
                            **data[mapping_info.get("alias", mapping)]
                        ),
                    )
                elif t == "dynamic":
                    setattr(
                        self,
                        mapping,
                        mapping_info["class"](
                            self.symbol, self.session, data[mapping_info.get("alias", mapping)]
                        ),
                    )
                elif t is None or t == "primitive":
                    setattr(self, mapping, data[mapping_info.get("alias", mapping)])

