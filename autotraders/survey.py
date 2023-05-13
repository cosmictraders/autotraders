from autotraders.util import parse_time


class Survey:
    def __init__(self, data):
        self.signature = data["signature"]
        self.symbol = data["symbol"]
        self.deposits = data["deposits"]
        self.expiration = parse_time(data["expiration"])
        self.size = data["size"]
