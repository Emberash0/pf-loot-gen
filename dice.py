from random import randint

def dice(m: int, n: int = 1):
    total = 0
    for _ in range(n):
        total += randint(1, m)
    return total
