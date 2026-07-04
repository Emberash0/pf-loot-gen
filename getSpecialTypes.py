from fileProcessor import ReadFile, ReadTable

#From a name srting, determines the information provided, gets any missing information
#Then returns valid dragon name and age
def GetDragon(name: str) -> tuple[str, int]:
    name_words = name.split(" ")
    num_words = len(name_words)

    #The ONLY non-dragon creature whose name ends in dragon, got to account for it
    if name == "rope dragon":
        return "rope dragon", 0
    match num_words:
        #We are only here because the last word in name was dragon.
        #This one word was dragon, so we still need age and type.
        case 1:
            print("What type of dragon?\n")
            dragon_name = ValidName(input().lower())
            print("What age was the dragon?\n")
            dragon_age = int(ValidAge(input().lower()))
        
        #The last word is dragon. The first word could be type (red, brass etc) or single-word age
        #Type is more likely, so to keep it clean, we will risk asking for age when it has been given 
        #and check type first.
        case 2:
            dragon_name = ValidName(name_words[0])
            print("What age was the dragon?\n")
            dragon_age = int(ValidAge(input().lower()))

        #Most likely this is single-word age, type then dragon. So process middle word as type
        #Then first word as age. If we are wrong the worst that could happen is we will ask for information
        #already given. There is no way we would get either wrong with this logic (other than user error)
        case 3:
            dragon_name = ValidName(name_words[1])
            dragon_age = int(ValidAge(name_words[0]))

        #Assuming no user error, this is a two-word age, single-word type then dragon.
        case 4:
            dragon_name = ValidName(name_words[2])
            age = f"{name_words[0]} {name_words[1]}"
            dragon_age = int(ValidAge(age))
    return dragon_name, dragon_age

#Was the given age valid?
def ValidAge(age: str) -> int:
    ages = ReadTable("dragon_ages.csv", "c")
    valid_age = False
    while not valid_age:
        #YAY it was!
        if age in ages[0]:
            valid_age = True
            #Return the modifier to CR from corresponding age
            age = ages[1][ages[0].index(age)]
            return age
        #Oh dear, not valid, try again until it is
        else:
            print(f"{age} is not a valid dragon age. Please enter valid age\n")
            age = input().lower()

#Same for Dragon type
def ValidName(name: str) -> str:
    names = ReadFile("dragon_types.txt")
    valid_name = False
    while not valid_name:
        if name in names:
            valid_name = True
            return f"{name} dragon"
        else:
            print(f"{name} is not a valid dragon type. Please enter valid type\n")
            name = input().lower()

#Very similar process for elementals, though some easier cases due to both variables only having
#single-word options
def GetElemental(name: str) -> tuple[str, int]:
    name_words = name.split(" ")
    num_words = len(name_words)
    match num_words:
        #Word must be elemental, so we are missing size and element
        case 1:
            print("Please enter the elemental type\n")
            elemental_name = f"{input().lower()} elemental"
            print("What size was the elemental?\n")
            elemental_size = ValidSize(input().lower())

        #Word is either size or element. More likely size 
        # (I would put fire elemental over large elemental) 
        case 2:
            elemental_name = ValidElement(name_words[0])
            print("What size was the elemental?\n")
            elemental_size = ValidSize(input().lower())

        #Yay, size and element, almost certainly in that order
        #Who says Fire Large Elemental?
        case 3:
            size = name_words[0]
            element = name_words[1]
            elemental_name = ValidElement(element)
            elemental_size = ValidSize(size)
        case default:
            raise ValueError("Unexpected number of words in elemental name\n")
    return elemental_name, elemental_size

#Same logic as the dragon variants
def ValidSize(size: str) -> int:
    sizes = ReadTable("elemental_sizes.csv", "c")
    valid_size = False
    while not valid_size:
        if size in sizes[0]:
            valid_size = True
            size = sizes[1][sizes[0].index(size)]
            return size
        else:
            print(f"{size} is not a valid elemental size. Please enter valid size\n")
            size = input().lower()

#Once more!
def ValidElement(name: str) -> str:
    names = ReadFile("elemental_types.txt")
    valid_name = False
    while not valid_name:
        if name in names:
            valid_name = True
            return f"{name} elemental"
        else:
            print(f"{name} is not a valid element. Please enter valid element\n")
            name = input().lower()

