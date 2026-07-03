import sys
from encounter import Encounter
from console import EncounterArgs

#Main working loop. 
def main():
    #Handles cases for each type of input arguments
    creatures, output = EncounterArgs(sys.argv)
    encounter = Encounter(creatures)
    print(output, encounter)

main()
