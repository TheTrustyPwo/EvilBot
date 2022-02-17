import sqlite3
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
import urllib
from utils import Logger

DATABASE_FILE = "database.sqlite"


class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:LjaDjjMvl5e7MacW@evil.cyykl.mongodb.net/test?retryWrites=true&w=majority", server_api=ServerApi('1'))
        self.database = self.client["test"]
        self.money = self.database["money"]
        Logger.info("Connected to MongoDB (Remote)")

    def getUserMoney(self, userId: int) -> (int, int):
        return 999999999, 999999999
        # result = self.money.find_one({"_id": userId})
        # if result is None:
        #     return 0, 0
        # return result["balance"], result["bank"]

    def updateUserMoney(self, userId: int, balance: int, bank: int) -> None:
        self.money.replace_one({"_id": userId}, {"balance": balance, "bank": bank}, upsert=True)

    def addUserMoney(self, userId: int, balance: int, bank: int):
        bal, bankBal = self.getUserMoney(userId)
        self.updateUserMoney(userId, bal + balance, bankBal + bank)

    def isOnCooldown(self, userId: int, command: str) -> (bool, int):
        self.cursor.execute("SELECT Cooldown FROM Cooldown WHERE UID=? AND Command=?", (userId, command))
        result = self.cursor.fetchall()
        print(result)
        if not result:
            return False, 0
        else:
            for i in result[0]:
                if i <= int(time.time()):
                    return False, 0
            return True, result[0][0]

    def createCooldown(self, userId: int, command: str, cooldown: int):
        cooldown += int(time.time())
        self.cursor.execute("INSERT INTO Cooldown(UID, Command, Cooldown) VALUES (?,?,?)", (userId, command, cooldown))

    def removeExpiredCooldown(self):
        self.cursor.execute("DELETE FROM Cooldown WHERE Cooldown <= ?", (int(time.time()),))
        Logger.info("Removed expired cooldowns")

    def isSuperAdmin(self, userId: int) -> bool:
        self.cursor.execute("SELECT * FROM SuperAdmins WHERE UID=?", (userId,))
        result = self.cursor.fetchall()
        if not result:
            return False
        return True

    def giveSuperAdmin(self, userId: int):
        self.cursor.execute("INSERT INTO SuperAdmins(UID) VALUES (?)", (userId,))

    def revokeSuperAdmin(self, userId: int):
        self.cursor.execute("DELETE FROM SuperAdmins WHERE UID=?", (userId,))


database = Database()


def getDatabase():
    return database
