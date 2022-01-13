import sqlite3
import time
from utils import Logger

DATABASE_FILE = "database.sqlite"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.connection.cursor()
        self.createTables()
        Logger.info("asdf")

    def createTables(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Money(UID varchar(18) NOT NULL UNIQUE, Balance integer, Bank integer, PRIMARY KEY (UID))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Cooldown(ID integer AUTO_INCREMENT, UID varchar(18), Command varchar(36), Cooldown integer, PRIMARY KEY (ID))")

    def getUserMoney(self, userId: int) -> (int, int):
        self.cursor.execute("SELECT Balance, Bank FROM Money WHERE UID=?", (userId,))
        result = self.cursor.fetchall()
        if not result:
            return 0, 0
        else:
            return result[0][0], result[0][1]

    def updateUserMoney(self, userId: int, balance: int, bank: int) -> None:
        self.cursor.execute("INSERT OR REPLACE INTO Money(UID, Balance, Bank) VALUES (?,?,?)", (userId, balance, bank))
        self.connection.commit()

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


database = Database()


def getDatabase():
    return database
