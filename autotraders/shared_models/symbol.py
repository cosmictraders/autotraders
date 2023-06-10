class Symbol(str):
    def __init__(self, t, obj):
        super(t, obj).__init__()

    def __eq__(self, other):
        return self.lower() == other.lower()
