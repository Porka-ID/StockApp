import mdp
import pymongo as pm
class Database:
    def __init__(self) -> None:
        self.client = pm.MongoClient(mdp.mdp)
        self.db = self.client["DBStock"]
        self.col = self.db["Stock"]

    def getAll(self):
        return self.col.find() or False