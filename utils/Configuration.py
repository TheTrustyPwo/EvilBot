import yaml

FILE = "config.yml"
config = yaml.load(open(FILE), Loader=yaml.FullLoader)


def getConfig():
    return config
