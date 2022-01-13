import random
import hashlib
import hmac
import time
import string


def generateServerSeed() -> (str, str):
    serverSeed = ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(64))
    return serverSeed, hashlib.sha256(serverSeed.encode("utf-8")).hexdigest()


def generateNumber(serverSeed: str, clientSeed: str, modifier: str, maxValue: int = 100) -> int:
    serverSeed.encode("utf-8")
    key = "%s:%s:%s" % (modifier, serverSeed, modifier)  # HMAC Secret Key
    client = "%s:%s:%s" % (modifier, clientSeed, modifier)  # HMAC Client Key
    signature = hmac.new(
        key.encode("utf-8"),
        client.encode("utf-8"),
        hashlib.sha512).hexdigest()  # HMAC-SHA512 Hash
    decimal = int(signature[:8], 16)  # Convert first 8 characters to base 16 decimal
    return min(round(decimal / 4294967295 * maxValue), maxValue)  # To whole number and ensure number <= 10000


def getTimestampHash() -> str:
    return hashlib.sha1(str(time.time()).encode("utf-8")).hexdigest()
