from typing import Any, Optional

from autotraders import AutoTradersSession
from autotraders.error import SpaceTradersException


class SpaceTradersEntity:
    def __init__(
        self, session: AutoTradersSession, action_url, data: Optional[dict] = None
    ):
        self.session: AutoTradersSession = session
        self.action_url = action_url
        if self.action_url[-1] != "/":
            self.action_url += "/"
        self.json: dict[str, Any] = {}
        self.update(data)

    def get(self, action: Optional[str] = None) -> dict:
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
            raise SpaceTradersException(
                j["error"], r.url, r.status_code, r.request.headers, r.headers
            )
        return j

    def post(self, action: str, data=None) -> dict:
        if data is not None:
            r = self.session.post(
                self.action_url + action,
                json=data,
            )
        else:
            r = self.session.post(self.action_url + action)
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(
                j["error"], r.url, r.status_code, r.request.headers, r.headers
            )
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
            raise SpaceTradersException(
                j["error"], r.url, r.status_code, r.request.headers, r.headers
            )
        return j

    def _update(
        self,
        data: Optional[dict[str, Any]] = None,
        special_endpoint: Optional[str] = None,
    ) -> dict[str, Any]:
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

    def update(self, data: Optional[dict] = None):
        pass

    def update_attr(self, mappings: dict[str, Any], data: dict[str, Any]):
        for mapping in mappings:
            mapping_info = mappings.get(mapping, {})
            t = mapping_info.get("type", None)
            optional = mapping_info.get("optional", True)
            data_name = mapping_info.get("alias", mapping)
            if data_name in data:
                if t == "object":
                    setattr(
                        self,
                        mapping,
                        mapping_info["class"](**data[data_name]),
                    )
                elif t == "dynamic":
                    setattr(
                        self,
                        mapping,
                        mapping_info["class"](
                            getattr(self, mapping_info.get("first_arg", "symbol")),
                            self.session,
                            data[data_name],
                        ),
                    )
                elif t is None or t == "primitive":
                    setattr(self, mapping, data[data_name])
            elif not optional:
                raise ValueError("Missing required attribute " + mapping)
