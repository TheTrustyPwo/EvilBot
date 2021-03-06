import datetime
import time
import copy
from enum import Enum

import nextcord

from utils import Configuration


class EmbedColors(Enum):
    DEFAULT = Configuration.get()["EmbedColors"]["Default"]
    SUCCESS = Configuration.get()["EmbedColors"]["Success"]
    ERROR = Configuration.get()["EmbedColors"]["Error"]


def getEmbed(name: str, data: list = None) -> nextcord.Embed:
    data = [] if data is None else data
    embed = copy.deepcopy(Configuration.get()["Embeds"][name])
    setPlaceholders(embed, data)
    return nextcord.Embed.from_dict(embed)


def setPlaceholders(embed: dict, data: list):
    for key, value in embed.items():
        if isinstance(value, dict):
            setPlaceholders(value, data)
        elif isinstance(value, list):
            for field in value:
                setPlaceholders(field, data)
        else:
            if key == "color":
                embed["color"] = getColor(value)
                continue
            elif key == "timestamp" and value is True:
                embed["timestamp"] = datetime.datetime.now().isoformat()
                continue
            elif isinstance(value, bool):
                continue
            embed[key] = replace(value, data)


def replace(string: str, data: list) -> str:
    for i in data:
        string = string.replace(str(i[0]), str(i[1]))
    return string


def getColor(color: str) -> int:
    for name, member in EmbedColors.__members__.items():
        if color.upper() == name.upper():
            return int(EmbedColors.__getitem__(name).value)
    return int(color)
