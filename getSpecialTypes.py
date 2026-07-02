from fileProcessor import ReadFile, ReadTable

def GetDragon(name: str) -> tuple[str, int]:
    name_words = name.split(" ")
    num_words = len(name_words)
    if name == "rope dragon":
        return "rope dragon", 0
    match num_words:
        case 1:
            print("What type of dragon?\n")
            dragon_name = ValidName(input().lower())
            print("What age was the dragon?\n")
            dragon_age = int(ValidAge(input().lower()))
        case 2:
            dragon_name = ValidName(name_words[0])
            print("What age was the dragon?\n")
            dragon_age = int(ValidAge(input().lower()))
        case 3:
            dragon_name = ValidName(name_words[1])
            dragon_age = int(ValidAge(name_words[0]))
        case 4:
            dragon_name = ValidName(name_words[2])
            age = f"{name_words[0]} {name_words[1]}"
            dragon_age = int(ValidAge(age))
    return dragon_name, dragon_age

def ValidAge(age: str) -> int:
    ages = ReadTable("dragon_ages.csv", "c")
    valid_age = False
    while not valid_age:
        if age in ages[0]:
            valid_age = True
            age = ages[1][ages[0].index(age)]
            return age
        else:
            print(f"{age} is not a valid dragon age. Please enter valid age\n")
            age = input().lower()

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

def GetElemental(name: str) -> tuple[str, int]:
    name_words = name.split(" ")
    num_words = len(name_words)
    match num_words:
        case 1:
            print("Please enter the elemental type\n")
            elemental_name = f"{input().lower()} elemental"
            print("What size was the elemental?\n")
            elemental_size = ValidSize(input().lower())
        case 2:
            elemental_name = ValidElement(name_words[0])
            print("What size was the elemental?\n")
            elemental_size = ValidSize(input().lower())
        case 3:
            size = name_words[0]
            element = name_words[1]
            elemental_name = ValidElement(element)
            elemental_size = ValidSize(size)
        case default:
            raise ValueError("Unexpected number of words in elemental name\n")
    return elemental_name, elemental_size

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

