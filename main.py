import sys
from encounter import Encounter
from console import EncounterArgs
from LootObject import LootObject

from Generate import A

#Main working loop. 
def main():
    #Handles cases for each type of input arguments and stores preferred output type
    print("Processing arguments...")
    creatures, output = EncounterArgs(sys.argv)
    print("Processing input...\n")

    #Generates the encounter object containing budget, xp award, and treasure types
    encounter = Encounter(creatures)
    print(encounter)

    loot = LootObject(encounter.types, encounter.value)

    

main()
