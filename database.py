from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client.admin

def insert_vote():

    vote = {"song_id": "214123",
            "url": "test",
            "location": {"lon": 24.22, "lat": 33.3}}
    
    created_time = datetime.now()
    vote['created_time'] = created_time
           
    db.vote.insert_one(vote)


insert_vote()