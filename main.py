import sys
from encounter import Encounter
from console import EncounterArgs
from LootObject import LootObject

#Main working loop. 
def main():
    #Handles cases for each type of input arguments and stores preferred output type
    print("Processing arguments...")
    creatures, output = EncounterArgs(sys.argv)

    #Generates the encounter object containing budget, xp award, and treasure types
    print("Analysing encounter...")
    encounter = Encounter(creatures)

    #Create the proxy LootObject
    loot = LootObject(encounter)

    #Main Generation Process
    print("Generating loot...")
    loot.PopulateLoot()
    
    print("\n------Loot Gen Procedure Complete------")
    if output[0]:
        print("\nPrinting Output to console...")
        print(loot)
    else:
        output_dest = "output/" + output[1]
        print(f"Writing output to {output_dest}...")
        with open(output_dest, "w") as f:
            f.write(repr(loot))

main()
