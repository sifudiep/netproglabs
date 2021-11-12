import random

def getLotto():
    result = set()
    while(len(result) < 7):
        result.add(random.randint(1,35))

    return result


