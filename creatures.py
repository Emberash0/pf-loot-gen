from getSpecialTypes import GetDragon, GetElemental
from fileProcessor import ReadTable, ReadFile
from findBinIndex import FindBinIndex

def CalcValue(xp, pace = "medium"):
    #Based on a given XP value and the pace of the campaign, returns the treasure value
    treasure_lookup = ReadTable("Treasure_by_XPTotal.csv", "c")
    #splits the table into the bin list, and a separate list for each pace option
    xp_list = treasure_lookup[0]
    slow_list = treasure_lookup[1]
    medium_list = treasure_lookup[2]
    fast_list = treasure_lookup[3]
    #Finds the row based on the xp given
    bin_index = FindBinIndex(xp, xp_list)

    #pulls value based on pace
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

#Same as CalcValue, but for NPC creatures. Instead of pace, value changes based on level types
def NPCValue(CR, NPC_type = "basic"): 
    treasure_lookup = ReadTable("NPC_Treasure.csv", "c")
    #Some bestiary creatures are NPCs without levels, so have <1 CR. 
    #Here we simply set anyhting less than 1 CR to the minimum treasure value 
    if CR < 0:
        match NPC_type:
            case "heroic":
                return 260
            case default:
                return 130
    #Splits the lookup table...
    basic_list = treasure_lookup[0]
    hero_list = treasure_lookup[1]
    gp_list = treasure_lookup[2]
    #matches based on user input
    match NPC_type:
        case "basic":
            bin_index = FindBinIndex(CR, basic_list)
            value = int(gp_list[bin_index])
        case "heroic":
            bin_index = FindBinIndex(CR, hero_list)
            value = int(gp_list[bin_index])
        case default: #If we are here, there was a weird user input. 
            #We will just assume they wanted basic
            print("Unexpected NPC type, assuming basic...\n")
            bin_index = FindBinIndex(CR, basic_list)
            value = int(gp_list[bin_index])
    return value

#An idiot checker that ensures a creature has a valid type before continuing.
#If not, it asks for user input until a valid type is given
def CheckType(name):
    types = ReadFile("creature_types.txt")
    valid_type = False
    while not valid_type:
        if name in types:
            return name
        else:
            print("Not a valid type, please enter a valid type\n")
            name = input().lower()

#A Creature Object has a name, quantity, and other properties calculated from a given lookup table and pace
class Creature:
    def __init__(self, name: str, quantity: int = 1, lookup: list = None, pace: str = "Medium") -> None:
        self.name = name
        self.quantity = int(quantity)
        if lookup: #If a lookup table is given, it references it to find the appropriate values
            words = self.name.split(" ")
            if "dragon" == words[-1]: #if the creature given is a type of dragon, it needs to be processed to include its age
                name_age = GetDragon(self.name) #Calls function to automatically determine age and type of dragon. 
                                                #if not clear, the function calls for user help
                d_name = name_age[0] #assigns the values
                age = name_age[1]
                xp_lookup = ReadTable("XP_by_CR.csv", "c") #As dragons cr changes based on age, xp must be found from a lookup table
                dragon_found = False
                i = 0
                while not dragon_found: #tries to find the dragon name (sans age) in bestiary. loop exits when dragon is found
                                        #as we already ran GetDragon, which only returns valid dragon names, we know we WILL find the dragon
                    creature = lookup[i]
                    if d_name == creature.name: #Once found, grab all the relevant values for the Creature Object
                        self.type = creature.type
                        self.cr = creature.cr + age
                        self.treasure = creature.treasure
                        self.xp = int(xp_lookup[1][xp_lookup[0].index(f"{self.cr}")])
                        self.treasure_default = None
                        dragon_found = True
                    i += 1
            elif "elemental" == words[-1]: #Very similar with elementals and sizes, only all elementals have the same CR if they are the same size
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
            else: #If it is not a tricky creature (damn you elementals and dragons!) find the creature in the bestiary
                creature_found = False
                i = 0
                while not creature_found and i < len(lookup): #here we do need to break the loop if we reach the end of the bestiary
                                                              # as some users will input NPCs which wont be found, or may have made spelling mistakes
                    creature = lookup[i]
                    if self.name == creature.name:
                        self.type = creature.type
                        self.cr = creature.cr
                        self.treasure = creature.treasure
                        self.xp = int(creature.xp)
                        self.treasure_default = creature.treasure_default
                        creature_found = True
                    i += 1
                if not creature_found: #if the creature isn't found, is it an npc?
                    print(f"Could not find {self.name} in bestiary\nAre they an NPC? (Y/N)\n")
                    if input().lower() == "N": #whelp, we didn't find the creature, and its not an npc, so something went wrong
                        raise ValueError("Creature Name not valid and not an NPC")
                    else:#It IS an NPC! hoorah. now we need to know its type and level to determine other values
                        print("What type of creature is the NPC?\n")
                        self.type = CheckType(input().lower())
                        print("What level is the NPC?\n")
                        cr = input()
                        while not cr.isdigit():#Umm, I asked you for a number!
                            print("That was not a number, please enter a valid cr\n")
                            cr = input()
                        self.cr = int(cr)#assigns values
                        self.treasure = "NPC"
                        xp_lookup = ReadTable("XP_by_CR.csv", "c")
                        self.xp = int(xp_lookup[1][xp_lookup[0].index(f"{self.cr}")])
                        self.treasure_default = "other"
            match self.treasure:#We now know how much treasure this drops. Let's calculate the exact value!
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

    def __repr__(self) -> str: #If printed or otherwise output to a file, it prints something nice like this
        return f"Creature({self.name}, {self.quantity}, CR{self.cr}, {self.xp}XP, dropping treasure equivalent to {self.value} gp, {self.type})"

class LookupCreature(Creature): #A creature type solely used to create the virtual bestiary for creature creation. 
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
                

