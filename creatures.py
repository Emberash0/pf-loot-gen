from getSpecialTypes import GetDragon, GetElemental
from fileProcessor import ReadTable, ReadFile

def FindBinIndex(value, list):
    bin_found = False
    index = 0
    while not bin_found:
        check_val = int(list[index])
        if value == check_val:
            return index
        if value < check_val:
            return index - 1
        if value > check_val and index == len(list) - 1:
            return index
        index += 1

def CalcValue(xp, pace = "medium"):
    treasure_lookup = ReadTable("Treasure_by_XPTotal.csv", "c")
    xp_list = treasure_lookup[0]
    slow_list = treasure_lookup[1]
    medium_list = treasure_lookup[2]
    fast_list = treasure_lookup[3]
    bin_index = FindBinIndex(xp, xp_list)
    match pace:
        case "slow":
            value = int(slow_list[bin_index])
        case "medium":
            value = int(medium_list[bin_index])
        case "fast":
            value = int(fast_list[bin_index])
        case default:
            print("Unexpected pace entry, assuming medium...")
            value = int(medium_list[bin_index])
    return value

def NPCValue(CR, NPC_type = "basic"):
    treasure_lookup = ReadTable("NPC_Treasure.csv", "c")
    if CR < 0:
        match NPC_type:
            case "heroic":
                return 260
            case default:
                return 130
    cr_list = treasure_lookup[0]
    hero_list = treasure_lookup[1]
    gp_list = treasure_lookup[2]
    match NPC_type:
        case "basic":
            bin_index = FindBinIndex(CR, cr_list)
            value = int(gp_list[bin_index])
        case "heroic":
            bin_index = FindBinIndex(CR, hero_list)
            value = int(gp_list[bin_index])
        case default:
            print("Unexpected NPC type, assuming basic...\n")
            bin_index = FindBinIndex(CR, cr_list)
            value = int(gp_list[bin_index])
    return value

def CheckType(name):
    types = ReadFile("creature_types.txt")
    valid_type = False
    while not valid_type:
        if name in types:
            return name
        else:
            print("Not a valid type, please enter a valid type\n")
            name = input().lower()

class Creature:
    def __init__(self, name: str, quantity: int = 1, lookup: list = None, pace: str = "Medium") -> None:
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
                while not creature_found and i < len(lookup):
                    creature = lookup[i]
                    if self.name == creature.name:
                        self.type = creature.type
                        self.cr = creature.cr
                        self.treasure = creature.treasure
                        self.xp = int(creature.xp)
                        self.treasure_default = creature.treasure_default
                        creature_found = True
                    i += 1
                if not creature_found:
                    print(f"Could not find {self.name} in bestiary\nAre they an NPC? (Y/N)\n")
                    if input().lower() == "N":
                        raise ValueError("Creature Name not valid and not an NPC")
                    else:
                        print("What type of creature is the NPC?\n")
                        self.type = CheckType(input().lower())
                        print("What level is the NPC?\n")
                        cr = input()
                        while not cr.isdigit():
                            print("That was not a number, please enter a valid cr\n")
                            cr = input()
                        self.cr = int(cr)
                        self.treasure = "NPC"
                        xp_lookup = ReadTable("XP_by_CR.csv", "c")
                        self.xp = int(xp_lookup[1][xp_lookup[0].index(f"{self.cr}")])
                        self.treasure_default = "other"
            match self.treasure:
                case "none":
                    self.value = 0
                case "incidental":
                    self.value = CalcValue(self.xp, pace) / 2
                case "standard":
                    self.value = CalcValue(self.xp, pace)
                case "double":
                    self.value = CalcValue(self.xp, pace) * 2
                case "triple":
                    self.value = CalcValue(self.xp, pace) * 3
                case "NPC":
                    print(f"{self.name} is an NPC, are they basic or heroic?\n")
                    NPC_type = input().lower()
                    self.value = NPCValue(self.cr, NPC_type)

    def __repr__(self) -> str:
        return f"Creature({self.name}, {self.quantity}, CR{self.cr}, {self.xp}XP, dropping treasure equivalent to {self.value} gp, {self.type})"

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
                

