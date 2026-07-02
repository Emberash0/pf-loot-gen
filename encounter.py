from fileProcessor import ReadTable

class Encounter:
    def __init__(self, creatures: list):
        
        self.creatures = creatures
        total_xp = 0
        total_val = 0
        types = set()
        for creature in self.creatures:
            total_xp += creature.xp * creature.quantity
            total_val += creature.value * creature.quantity
            types.add(creature.type)
        self.xp = total_xp
        self.value = total_val
        self.types = types
        
    
    def __repr__(self):
        return f"An encounter worth {self.xp}XP rewarding treasure equal to {self.value} gp. Creatures are of the following types: {self.types}\n"

