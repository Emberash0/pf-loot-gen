from creatures import FindBinIndex
from fileProcessor import ReadTable
from dice import dice
from lootTypes import CoinsObject

def A(budget):
    coins_table = ReadTable("coins-table.csv", "c")
    roll_index = FindBinIndex(budget, coins_table[0])
    print(f"\nGenerating coins with approx budget of {coins_table[0][roll_index]} gp...")
    coins = []
    for i in range(1, 5):
        roll = coins_table[i][roll_index]
        if roll == "":
            coins.append(0)
        else:
            coin_dice = [int(x) for x in roll.split(";")]
            coins.append(dice(coin_dice[1], coin_dice[0]) * coin_dice[2])
    loot = CoinsObject(coins)
    return loot

def B():
    return

def C():
    return

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