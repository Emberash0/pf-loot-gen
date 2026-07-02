from encounterBuilder import EncounterBuilder
from creatures import Creature
from fileProcessor import ProcessCreatures, ReadTable

def EncounterArgs(args):
    
    match len(args):
        case 1: #Where no quantity or creature are given
            encounter = EncounterBuilder()

        case 2: #Where a total quantity is given, but there are multiple creature types
            if args[1].isdigit():
                encounter_quantity = int(args[1])
                encounter = EncounterBuilder(encounter_quantity)
            else: #Where the arg given was a creature name
                print(f"How many {args[1]}(s) are there?\n")
                encounter_quantity = int(input())
                lookup = ProcessCreatures(ReadTable("creatures.csv"))
                encounter = [Creature(args[1], encounter_quantity, lookup)]

        case default: #where a creature with multiple words is given along with potentially a quantity
            if args[1].isdigit():
                encounter_quantity = int(args[1])
                encounter_creature = " ".join(args[2:])
            elif args[-1].isdigit():
                encounter_quantity = int(args[-1])
                encounter_creature = " ".join(args[1:-1])
            else:
                encounter_creature = " ".join(args[1:])
                print(f"How many {encounter_creature}(s) were there?\n")
                encounter_quantity = int(input())
            lookup = ProcessCreatures(ReadTable("creatures.csv"))
            encounter = [Creature(encounter_creature, encounter_quantity, lookup)]
    return encounter