
import random

def rand_text(strings):
    rand = random.randint(0, len(strings) - 1)
    return strings[rand]