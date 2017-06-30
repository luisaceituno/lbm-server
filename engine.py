from database import MongoDb
import json
from flask import jsonify
from bson import json_util

class Engine():

    db = None

    def __init__(self):
        self.db = MongoDb()

    def get_top_songlist(self, lon, lat):
        votes =  self.db.get_votes_by_loc(lon, lat, 1)
        test = json.dumps(votes, default=json_util.default)


        # locationSongs:{

        #     location:{
        #         "lon": ..,
        #         "lat": ...
        #     }
        #     songs : [
        #         {"id": , "rating": }
        #     ]

        # }
        return test

    def post_vote(self, data):
        vote = json.loads(data)
        self.db.insert_vote(vote[0])

