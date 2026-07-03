import argparse
from encounterBuilder import EncounterBuilder
from creatures import Creature
from fileProcessor import ProcessCreatures, ReadTable

def ParseArgs(arg_string):
    parser = argparse.ArgumentParser(
        description = "A script to generate random loot using rules found in Ultimate Equipment for Pathfinder First Edition"
        )
    #Define input arguments
    parser.add_argument(
        "file", help="main.py"
    )
    parser.add_argument(
        "pace", help="The pace of the campaign determines treasure awarded."
        )

    #Define optional arguments
    input_method_group = parser.add_mutually_exclusive_group(required=True)
    input_method_group.add_argument(
        "-e", "--encounterbuilder", action="store_true", 
        help="Build the encounter in the console. Use -e , -i or give a single creature and quantity as arguments"
        )
    input_method_group.add_argument(
        "-i", "--input", help="Take encounter from an input file, do not use with -e"
    )
    input_method_group.add_argument(
        "-v", "--verboseinput", help="Input single creature type and quantity (assumed 1 if none)"
        )
    parser.add_argument(
        "-o", "--output", help="Path to output file"
        )
    args = parser.parse_args(arg_string)
    return args

def EncounterArgs(input):
    args = ParseArgs(input)
    lookup = ProcessCreatures(ReadTable("creatures.csv"))
    pace = args.pace
    if args.output != None:
        output_dest = args.output
        output_console = False
    else:
        output_console = True
        output_dest = False
    if args.encounterbuilder:
        encounter = EncounterBuilder(pace = pace, lookup = lookup)
    elif args.verboseinput != None:
        creature = args.verboseinput
        creature_tuple = [x.strip() for x in creature.split(",")]
        print(creature_tuple)
        if len(creature_tuple) == 1:
            creature_quantity = 1
            creature_name = creature_tuple[0]
        else:
            if creature_tuple[0].isdigit():
                creature_name = creature_tuple[1]
                creature_quantity = creature_tuple[0]
            elif creature_tuple[1].isdigit():
                creature_name = creature_tuple[0]
                creature_quantity = creature_tuple[1]
            else:
                raise ValueError("-v args should be of form 'name, quantity'\n")
        encounter = [Creature(creature_name, creature_quantity, lookup, pace)]
    elif args.input != None:
        file_name = args.input
        file = ReadTable(file_name)
        encounter = []
        for row in file:
            row_tuple = row.split(",")
            creature_name, creature_number = row_tuple
            creature_quantity = int(creature_number)
            encounter.append(Creature(creature_name, creature_quantity, lookup, pace))
    else:
        raise ValueError("Unknown input type argument")
    return encounter, [output_console, output_dest]