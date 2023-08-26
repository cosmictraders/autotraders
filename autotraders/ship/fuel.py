from pydantic import BaseModel


class Fuel(BaseModel):
    current: int
    capacity: int

    def __str__(self):
        return str(self.current) + "/" + str(self.total)
