from getSpecialTypes import GetDragon, GetElemental
from fileProcessor import ReadTable

class Creature:
    def __init__(self, name: str, quantity: int = 1, lookup: list = None) -> None:
        self.name = name
        self.quantity = int(quantity)
        if lookup: #If a lookup table is given, it references it to find the appropriate values
            words = self.name.split(" ")
            if "dragon" == words[-1]: #if the creature given is a type of dragon, it needs to be processed to include its age
                name_age = GetDragon(self.name)
                d_name = name_age[0]
                age = name_age[1]
                xp_lookup = ReadTable("XP_by_CR.csv", "c")
                dragon_found = False
                i = 0
                while not dragon_found:
                    creature = lookup[i]
                    if d_name == creature.name:
                        self.type = creature.type
                        self.cr = creature.cr + age
                        self.treasure = creature.treasure
                        self.xp = int(xp_lookup[1][xp_lookup[0].index(f"{self.cr}")])
                        self.treasure_default = None
                        dragon_found = True
                    i += 1
            elif "elemental" == words[-1]:
                name_size = GetElemental(self.name)
                e_name = name_size[0]
                size = name_size[1]
                xp_lookup = ReadTable("XP_by_CR.csv", "c")
                elemental_found = False
                i = 0
                while not elemental_found:
                    creature = lookup[i]
                    if e_name == creature.name:
                        self.type = creature.type
                        self.cr = size
                        self.treasure = creature.treasure
                        self.xp = int(xp_lookup[1][xp_lookup[0].index(f"{self.cr}")])
                        self.treasure_default = creature.treasure_default
                        elemental_found = True
                    i += 1
            else:
                creature_found = False
                i = 0
                while not creature_found:
                    creature = lookup[i]
                    if self.name == creature.name:
                        self.type = creature.type
                        self.cr = creature.cr
                        self.treasure = creature.treasure
                        self.xp = int(creature.xp)
                        self.treasure_default = creature.treasure_default
                        creature_found = True
                    i += 1
                    if i > len(lookup):
                        raise LookupError(f"Could not find {self.name} in bestiary")

    def __repr__(self) -> str:
        return f"Creature({self.name}, {self.quantity}, CR{self.cr}, {self.xp}XP)"

class LookupCreature(Creature):
    def __init__(self, name: str, type: str, cr: str, treasure: str, xp: int, treasure_default: list[str]) -> None:
        super().__init__(name)
        self.type = type
        self.crstr = cr
        if cr.isdigit():
            self.cr = int(cr)
        else:
            match cr:
                case "1/8":
                    self.cr = -5
                case "1/6":
                    self.cr = -4
                case "1/4":
                    self.cr = -3
                case "1/3":
                    self.cr = -2
                case "1/2":
                    self.cr = -1
                case default:
                    raise ValueError(f"{cr} is an invalid CR in creatures.csv")
        self.treasure = treasure
        self.xp = xp
        self.treasure_default = treasure_default

    def __repr__(self) -> str:
        return f"LookupCreature({self.name}, {self.type}, CR{self.crstr}, {self.xp}XP, {self.treasure} treasure, {self.treasure_default} by default)"
                

