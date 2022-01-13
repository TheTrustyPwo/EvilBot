import os
import platform
import sys
import nextcord
from nextcord.ext import commands
import requests
from utils import Database
from utils import Logger

Logger.info("Checking for rate limits")
response = requests.head(url="https://discord.com/api/v1")
try:
    retry = int(response.headers['Retry-After']) / 60
    Logger.error(f"Rate limit detected! {retry} minutes left")
except:
    Logger.info("No rate limit detected")

Database.getDatabase().removeExpiredCooldown()

intents = nextcord.Intents().all()
client = commands.Bot(command_prefix=".", intents=intents)


@client.event
async def on_ready():
    # change_status.start()
    await client.deploy_application_commands()
    Logger.gap()
    Logger.info(f"Logged in as {client.user.name}")
    Logger.info(f"Nextcord API version: {nextcord.__version__}")
    Logger.info(f"Python version: {platform.python_version()}")
    Logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    Logger.gap()

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        entry = os.path.join(dirName, entry)
        if os.path.isdir(entry):
            allFiles = allFiles + getListOfFiles(entry)
        else:
            allFiles.append(entry)
    return allFiles


if __name__ == "__main__":
    Logger.info("Loading cogs")
    n = 0
    for file in getListOfFiles("./cogs"):
        if file.endswith(".py"):
            extension = file[2:-3].replace('\\', '.')
            try:
                client.load_extension(extension)
                n += 1
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                Logger.warn(f"Failed to load cog: {extension} \n {exception}")
    Logger.info(f"Loaded {n} cogs!")
    # client.load_extension("cogs.AI")

client.run("ODQ2NzM3NzQwOTI5NTY0Njcy.YKz3-Q.w-pf29MtNdXDjb0GwKtPHGk4hnM")
