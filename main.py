import sys
from console import EncounterArgs
from encounter import Encounter

#Main working loop. 
def main():
    #Handles cases for each type of input arguments
    encounter = Encounter(EncounterArgs(sys.argv))
    print(encounter)
    
    
    return

main()
