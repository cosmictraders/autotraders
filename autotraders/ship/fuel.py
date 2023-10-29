from pydantic import BaseModel, NonNegativeInt


class Fuel(BaseModel):
    current: NonNegativeInt
    capacity: NonNegativeInt

    def cheap_refuel(self) -> int:
        """
        :return: The number of units to fill up in the nearest 100.
        """
        return ((self.capacity - self.current) // 100) * 100

    def __str__(self):
        return str(self.current) + "/" + str(self.total)

    def __float__(self):
        return float(self.current) / float(self.capacity)

    def __hash__(self):
        return hash((self.current, self.capacity))
