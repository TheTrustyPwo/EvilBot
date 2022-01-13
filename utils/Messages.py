import random

from utils import Configuration


def getMessage(name: str, data: list = None) -> str:
    data = [] if data is None else data
    value = Configuration.getConfig()["Messages"][name]
    if isinstance(value, list):
        value = random.choice(value)
    for i in data:
        value = value.replace(str(i[0]), str(i[1]))
    return value.replace(r"\n", "\n")
