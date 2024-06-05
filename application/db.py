import mdp
import pymongo as pm
from bson.objectid import ObjectId
class Database:
    def __init__(self) -> None:
        self.client = pm.MongoClient(mdp.mdp)
        self.db = self.client["DBStock"]
        self.col = self.db["Stock"]

    def getAll(self):
        return self.col.find() or False
    
    def insertStock(self, name, type, nbrStock, infos):
        self.col.insert_one({"name": name, "type": type, "qty": nbrStock, "infos": infos})
        return name, type, nbrStock, infos
    
    def deleteStock(self, id):
        self.col.delete_one({"_id": ObjectId(id)})
        return id
    
    def deleteAllStock(self):
        self.col.delete_many({})
        return {}
    
    def modifyNbrStock(self, name, nbr):
        self.col.update_one({"name": name}, {"$set": {"qty": nbr}})
        return {"qty": nbr}
    
    def modifyStock(self, name, type, nbrStock, infos, oldName):
        print(oldName)
        self.col.update_one({"name": oldName}, {"$set": {"name": name, "type": type, "qty": nbrStock, "infos": infos}})
        return [name, type, nbrStock, infos]