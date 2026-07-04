from fileProcessor import ReadTable
from findBinIndex import FindBinIndex
from dice import dice

#Generate random gemstone based on grade
def GetGem(grade):
    #Avoids circular declaration
    from lootTypes import UnworkedGem, WorkedGem

    #Generate lookup lists and index
    gem_list = ReadTable("gem-list.csv", "c")
    bins = gem_list[0]
    gems = gem_list[grade]

    #Randomly chooses Gem from the appropriate Grade List
    name = gems[FindBinIndex(dice(100), bins)]

    #Determines the random part of increased value if worked
    improvement = dice(4, 2)

    #Is the gemstone already cut?
    if dice(2) - 1 == 0:
        worked = 0
    else:
        worked = 1
    prefix = ""
    if worked == 1:
        prefix = "Cut "
    name = prefix + name

    #Determine value, improved value and Craft DC to cut dependent on grade
    match grade:
        case 1:
            value = 5 + improvement * worked
            craft_DC = 10
        case 2:
            improvement *= 5
            value = 25 + improvement * worked
            craft_DC = 12
        case 3:
            improvement *= 10
            value = 50 + improvement * worked
            craft_DC = 15
        case 4:
            improvement *= 50
            value = 250 + improvement * worked
            craft_DC = 20
        case 5:
            improvement *= 100
            value = 500 + improvement * worked
            craft_DC = 25
        case 6:
            improvement = max(improvement * 500, 2500)
            value = 2500 + improvement * worked
            craft_DC = 25
    if worked:
        return WorkedGem(name, value)
    else:
        return UnworkedGem(name, value, improvement, craft_DC)
    
def GetArt(grade):
    #Avoids circular declaration
    from lootTypes import Art

    #Generate lookup lists and index
    art_list = ReadTable("art-list.csv", "c")
    bins = art_list[0]
    arts = art_list[2 * grade - 1]
    arts_values = art_list[2 * grade]

    #Randomly chooses Art from the appropriate Grade List
    index = FindBinIndex(dice(100), bins)
    name = arts[index]
    value = int(arts_values[index])
    return Art(name, value)