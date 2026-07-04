from creatures import FindBinIndex
from fileProcessor import ReadTable
from dice import dice
from lootTypes import CoinsObject, GemsObject, ArtsObject

#TREASURE TYPE A - COINS
def A(budget):
    #Grabs lookup table and designates working bin
    coins_table = ReadTable("coins-table.csv", "c")
    roll_index = FindBinIndex(budget, coins_table[0])
    print(
        f"Generating Coins with approx budget of {coins_table[0][roll_index]} gp..."
    )

    #creates empty objects
    coins = []

    #Generates coin loot
    for i in range(1, 5):
        roll = coins_table[i][roll_index]
        if roll == "":
            coins.append(0)
        else:
            coin_dice = [int(x) for x in roll.split(";")]
            coins.append(dice(coin_dice[1], coin_dice[0]) * coin_dice[2])
    return CoinsObject(coins)

#TREASURE TYPE B - GEMS AND COINS
def B(budget):
    #Grabs lookup table and designates working bin
    gems_table = ReadTable("gems-table.csv", "c")
    roll_index = FindBinIndex(budget, gems_table[0])

    #creates empty objects
    columns = len(gems_table)
    coins = []
    gems = GemsObject([])
    print(
        f"Generating Gems and Coins with approx budget of {gems_table[0][roll_index]} gp..."
    )

    #Generates coin loot
    for i in range(1, 5):
        roll = gems_table[i][roll_index]
        if roll == "":
            coins.append(0)
        else:
            coin_dice = [int(x) for x in roll.split(";")]
            coins.append(dice(coin_dice[1], coin_dice[0]) * coin_dice[2])

    #Generates gem loot
    for i in range(5, columns):
        if gems_table[i][roll_index] != "":
            quantity = int(gems_table[i][roll_index])
            grade = i - 4
            gems.GenerateGems(grade, quantity)

    return CoinsObject(coins), gems

#TREASURE TYPE C - ART OBJECTS
def C(budget):
    arts_table = ReadTable("art-table.csv", "c")
    roll_index = FindBinIndex(budget, arts_table[0])
    arts = ArtsObject([])
    print(
        f"Generating Artworks with approx budget of {arts_table[0][roll_index]} gp..."
    )

    for i in range(1, 7):
        ref = arts_table[i][roll_index]
        if ref != "":
            quantity = int(ref)
            grade = i
            arts.GenerateArts(grade, quantity)

    return arts

def D():
    return

def E():
    return

def F():
    return

def G():
    return

def H():
    return

def I():
    return