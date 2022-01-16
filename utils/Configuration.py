import yaml

FILE = "config.yml"

config = yaml.load(open(FILE, encoding="utf-8"), Loader=yaml.FullLoader)


def get() -> dict:
    return config


def get_guild_ids() -> list:
    return config["Guild-IDs"]


def get_global() -> bool:
    return config["Global-Slash-Commands"]
