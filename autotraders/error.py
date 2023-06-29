class SpaceTradersException(Exception):
    def __init__(self, error, status_code):
        super().__init__(error["message"])
        self.code = error["code"]
        self.status_code = status_code
