class SpaceTradersException(Exception):
    def __init__(self, error, url, status_code, request_headers, response_headers):
        super().__init__(error["message"])
        self.code = error["code"]
        self.url = url
        self.status_code = status_code
        self.request_headers = request_headers
        self.response_headers = response_headers
