from autotraders.time import parse_time


class Survey:
    def __init__(self, data):
        self.signature = data["signature"]
        self.symbol = data["symbol"]
        self.deposits = data["deposits"]
        self.expiration = parse_time(data["expiration"])
        self.size = data["size"]

    def __dict__(self):
        return {
            "signature": self.signature,
            "symbol": self.symbol,
            "deposits": self.deposits,
            "expiration": self.expiration.isoformat(),
            "size": self.size,
        }
