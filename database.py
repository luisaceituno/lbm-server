from pymongo import MongoClient
from bson import json_util
from datetime import datetime
from bson.son import SON
import json
import time

class MongoDb():
    client = MongoClient("mongodb://localhost:27017")
    db = client.admin

    def __init__(self):
        pass

    def insert_vote(self, vote):        
        created_time = datetime.now()
        vote['created_time'] = created_time  
        self.db.vote.insert_one(vote)

    def get_votes_by_loc(self, lon, lat, range):
        votes = self.db.vote.find( {"location": SON([("$near", [lon, lat]), ("$maxDistance", range)])}).limit(15)
        return list(votes)

