class SpaceTradersException:
    def __init__(self, msg, code, status_code):
        super.__init__(msg)
        self.code = code
        self.status_code = status_code

