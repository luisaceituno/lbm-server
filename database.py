from pymongo import MongoClient
from bson import json_util
from datetime import datetime
from bson.son import SON
import json
import time


class MongoDB():
    client = MongoClient("mongodb://localhost:27017")
    db = client.admin

    def __init__(self):
        pass

    def insert_vote(self):

        vote = {"song_id": "214123",
                "url": "test",
                "rating": 1,
                "location": {"lon": 11.53144, "lat": 48.1567}}
        
        created_time = datetime.now()
        vote['created_time'] = created_time
            
        self.db.vote.insert_one(vote)

    def get_votes_by_loc(self, lon, lat):
        votes = self.db.vote.find( {"location": SON([("$near", [lon, lat]), ("$maxDistance", 1)])})
        return list(votes)



db = MongoDB()
votes = db.get_votes_by_loc(11, 48)
print(json.dumps(votes, default=json_util.default))
