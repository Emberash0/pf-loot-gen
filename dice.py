from random import randint

#Takes a number of sides, m and number of dice, n
#Returns NdM
def dice(m: int, n: int = 1):
    total = 0
    for _ in range(n):#Roll n dice...
        total += randint(1, m)#... of m sides
    return total
