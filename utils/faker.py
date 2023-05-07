import random
import string


def random_str(length=7):
    return "".join([random.choice(string.ascii_letters) for _ in range(length)])
