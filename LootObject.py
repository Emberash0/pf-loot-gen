from random import randint
import Generate as Generate
from lootTypes import CoinsObject, GemsObject, ArtsObject

#A loot object contains properties for each type of loot available (coins, gems etc.)
#It accumulates all the different treasure generated and has a neat and tidy representation
#To make a readable output. Think of it like the list of contents of the treasure chest
class LootObject:
    def __init__(self, encounter):
        #for the output, its convenient for LootObject to store the encounter object it was given
        #LootObjects have access to the total xp and treasure values, as well as information
        #about all creatures in the encounter
        self.encounter = encounter

        #takes the set of treasure types and makes a more easily manipulated list
        self.options = list(encounter.types)

        #budget will be referenced and changed throughout the methods
        self.budget = encounter.value

        #as we don't know which treasure types and order will be performed, we need to initialise
        #the various treasure objects with empty values, and have the generation methods add to them rather than overwrite them
        self.coins = CoinsObject([0, 0, 0, 0])
        self.gems = GemsObject([])
        self.art = ArtsObject([])

    #Long and complex, but this builds the main body of text that will be the output
    def __repr__(self): 
        result = f"Total reward for Encounter:\n"
        result += f"The party fought:\n"
        for creature in self.encounter.creatures:
            result += f"- {creature.quantity} {creature.name}(s)\n"
        self.value = self.coins.value + self.gems.value + self.art.value
        result += f"\nThis awards {self.encounter.xp}XP and treasure equivalent to {self.value} gp from a budget of {self.encounter.value} gp\n"
        result += f"The party receives as loot:\n"
        result += repr(self.coins)
        result += repr(self.gems)
        result += repr(self.art)
        return result

    #Method called by the populate loot method, it determines, from the list of options, 
    #which treasure type to generate next. This generation will remove the type from the list
    def ChooseTreasureType(self):

        #Hoards and lairs feel appropriate to ask, as they are context specific
        if "H" in self.options or "I" in self.options:
            print("Were the creature(s) guarding a lair or hoard? (lair/hoard/n)")
            match input().lower():
                case "lair":
                    self.treasure_type = "H"
                    self.options.remove("H")
                case "hoard":
                    self.treasure_type = "I"
                    self.options.remove("I")
                
                #if its neither, we don't want to have to ask again next time round, so just remove them
                case default:
                    self.options.remove("I")
                    self.options.remove("H")
                    num_options = len(self.options) - 1
                    self.treasure_type = self.options[randint(0, num_options)]
            print("")
        else:
            num_options = len(self.options) - 1
            self.treasure_type = self.options[randint(0, num_options)]
    
    def PopulateLoot(self):
            
            #chooses the treasure type to generate next
            self.ChooseTreasureType()

            #matches to the correct case to run the correct Generate function
            match self.treasure_type:
                case "A":
                    self.options.remove("A")
                    coins = Generate.A(self.budget)
                    self.budget -= coins.value
                    self.coins += coins
                case "B":
                    self.options.remove("B")
                    coins, gems = Generate.B(self.budget)
                    self.budget -= coins.value + gems.value
                    self.coins += coins
                    self.gems += gems
                    
                case "C":
                    self.options.remove("C")
                    arts = Generate.C(self.budget)
                    self.budget -= arts.value
                    self.art += arts

                case "D":
                    self.coins, self.potions, self.scrolls, self.wands = Generate.D()
                case "E":
                    self.armour, self.weapons = Generate.E()
                case "F":
                    (
                        self.coins, 
                        self.potions, 
                        self.armour, 
                        self.shields, 
                        self.weapons, 
                        self.wondrous, 
                        self.rings
                    ) = Generate.F()
                case "G":
                    (
                        self.coins,
                        self.potions,
                        self.scrolls,
                        self.wands,
                        self.wondrous, 
                        self.rings, 
                        self.rods,
                        self.staves, 
                        self.weapons
                    ) = Generate.G()
                case "H":
                    (
                        self.coins,
                        self.weapons,
                        self.potions, 
                        self.scrolls,
                        self.gems,
                        self.wands,
                        self.armour,
                        self.weapons,
                        self.rings,
                        self.wondrous, 
                        self.rods,
                        self.staves
                    ) = Generate.H()
                case "I":
                    (
                        self.coins,
                        self.armour, 
                        self.wands,
                        self.art,
                        self.gems,
                        self.weapons, 
                        self.wondrous,
                        self.scrolls,
                        self.rings,
                        self.potions,
                        self.rods,
                        self.staves,
                    ) = Generate.I()
            if self.budget > 0 and len(self.options) > 0:
                self.PopulateLoot()
