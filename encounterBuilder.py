from creatures import Creature
from fileProcessor import ProcessCreatures, ReadTable

def EncounterBuilder(quantity: int = 1000) -> list[Creature]:
    encounter = []
    lookup = ProcessCreatures(ReadTable("creatures.csv"))

    #Until no creatures remain
    while quantity > 0:
        print("Please enter the next creature in the encounter. If no more, enter 'n'\n")
        creature = input().lower()
        if creature == "n":
            break
        print("How many of this creature were in the encounter?")

        #Creates creature object for the encounter list with name of creature and quantity
        creature_amt = int(input())

        #Handles issue where creature quantity is greater than remaining number of creatures declared
        if creature_amt > quantity:
            print("This is more than remaining creatures declared. Continue? Y/N\n")
            choice = input().lower()
            match choice:
                case "n":
                    raise ValueError("Value mis-match between declared encounter quantity and creature quantity\n")
                case "y":
                    print("After these creatures, how many remain?\n")
                    quantity = int(input())
        else:
            quantity -= creature_amt
        new_creature = Creature(creature, creature_amt, lookup)
        encounter.append(new_creature)

    return encounter