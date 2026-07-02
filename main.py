import sys
from console import EncounterArgs
from encounter import Encounter

#Main working loop. 
def main():
    #Handles cases for each type of input arguments
    creatures = EncounterArgs(sys.argv)
    encounter = Encounter(creatures)
    print(encounter)
    return

main()
