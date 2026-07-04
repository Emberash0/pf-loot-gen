class TreasureObject:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"A {self.name} worth {self.value}"
    
class CoinsObject(TreasureObject):
    def __init__(self, coins: list[int]):
        value = 0
        self.copper = coins[0]
        value += self.copper / 100.0
        self.silver = coins[1]
        value += self.silver / 10.0
        self.gold = coins[2]
        value += self.gold
        self.platinum = coins[3]
        value += self.platinum * 10
        self.value = value

    def __repr__(self):
        return f"{self.platinum} pp, {self.gold} gp, {self.silver} sp and {self.copper} cp worth a total of {self.value} gp"