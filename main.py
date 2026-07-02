import sys
from console import EncounterArgs

#Main working loop. 
def main():
    #Handles cases for each type of input arguments
    encounter = EncounterArgs(sys.argv)
    totalXP = 0
    for creature in encounter:
        totalXP += creature.xp * creature.quantity
    print(totalXP)
    return

main()
