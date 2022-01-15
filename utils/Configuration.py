import yaml

FILE = "config.yml"
config = yaml.load(open(FILE, encoding="utf-8"), Loader=yaml.FullLoader)


def getConfig():
    return config
