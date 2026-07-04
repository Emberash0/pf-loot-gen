import argparse
from encounterBuilder import EncounterBuilder
from creatures import Creature
from fileProcessor import ProcessCreatures, ReadTable

def ParseArgs(arg_string): #Uses a parser to assign arguments to correct values and apply relevant settings

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
    input_method_group = parser.add_mutually_exclusive_group(required=True) #Preventing multiple input methods fro being used
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
#Takes arguments and generates Encounter for use along with an output: (Bool:console output, Str:output file path)
    args = ParseArgs(input)

    #Generates a lookup table of key values for the PF Bestiary, used to automate treasure type and amount
    lookup = ProcessCreatures(ReadTable("creatures.csv"))
    pace = args.pace

    #If an output path is given, output to file in set destination
    if args.output != None:
        output_dest = args.output
        output_console = False
    #Else use console output
    else:
        output_console = True
        output_dest = False

    #If input method is to use encounter builder, run this now
    if args.encounterbuilder:
        encounter = EncounterBuilder(pace = pace, lookup = lookup)

    #Verbose input means a creature and quantity were given in the arguments
    #These are now processed
    elif args.verboseinput != None:
        creature = args.verboseinput

        #a tuple: creature name and quantity, from a comma separated string given
        creature_tuple = [x.strip() for x in creature.split(",")]

        #automatically determines which of the tuple values was the quantity
        #allows for user preference on order in string
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
        #ensures that result is of the correct form and generates the creature object
        encounter = [Creature(creature_name, creature_quantity, lookup, pace)]

    #takes input from a file given and uses the verbose input on each line of the file
    elif args.input != None:
        file_name = args.input
        file = ReadTable(file_name)
        encounter = []
        for row in file:
            row_tuple = row.split(",")
            creature_name, creature_number = row_tuple
            creature_quantity = int(creature_number)
            encounter.append(Creature(creature_name, creature_quantity, lookup, pace))
    #all possible input methods exhausted, so to get here, someting has gone wrong
    else:
        raise ValueError("Unknown input type argument")
    
    #passes the list of creatures and an output tuple to caller
    return encounter, [output_console, output_dest]