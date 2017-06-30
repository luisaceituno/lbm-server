from pymongo import MongoClient
from datetime import datetime

class MongoDB():
    client = MongoClient("mongodb://localhost:27017")
    db = client.admin

    def __init__(self):
        pass

    def insert_vote(self):

        vote = {"song_id": "214123",
                "url": "test",
                "location": {"lon": 24.22, "lat": 33.3}}
        
        created_time = datetime.now()
        vote['created_time'] = created_time
            
        self.db.vote.insert_one(vote)



db = MongoDB()
db.insert_vote()