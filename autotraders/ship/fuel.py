from pydantic import BaseModel, NonNegativeInt


class Fuel(BaseModel):
    current: NonNegativeInt
    capacity: NonNegativeInt

    def __str__(self):
        return str(self.current) + "/" + str(self.total)
