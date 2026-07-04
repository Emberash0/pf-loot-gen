from creatures import Creature

def EncounterBuilder(pace: str = "medium", lookup = None) -> list[Creature]:
    encounter = []
    #Until no creatures remain
    while True:
        print("Please enter the next creature in the encounter. If no more, enter 'n'\n")
        creature = input().lower()
        if creature == "n":
            break
        print("How many of this creature were in the encounter?")

        #Creates creature object for the encounter list with name of creature and quantity
        creature_amt = int(input())
        new_creature = Creature(creature, creature_amt, lookup, pace)
        encounter.append(new_creature)
    return encounter