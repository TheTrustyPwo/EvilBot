import time
from colorama import Fore


def info(message):
    print(f"{Fore.WHITE}[{time.strftime('%H:%M:%S', time.gmtime())} INFO]: {message}{Fore.WHITE}")


def warn(message):
    print(f"{Fore.YELLOW}[{time.strftime('%H:%M:%S', time.gmtime())} INFO]: {message}{Fore.WHITE}")


def error(message):
    print(f"{Fore.RED}[{time.strftime('%H:%M:%S', time.gmtime())} INFO]: {message}{Fore.WHITE}")


def gap():
    info(50 * "=")
