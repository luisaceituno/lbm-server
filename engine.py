import pandas as pd
from database import MongoDB
import json
from flask import jsonify
from bson import json_util

class Engine():

    def __init__(self):
        self.db = MongoDb()

    def get_top_songlist(self, lon, lat):
        
        votes= self.db.get_votes_by_loc(lon,lat,1)
        aggrVotes = aggregateVotes(votes)
        top_dict = get_top_ratings(aggrVotes)
        del top_dict['url', 'location', 'created_time']
        top_list = json.dumps(top_dict)
        locationsongs = { "location": { "lon": lon, "lat": lat }, "songs": top_list}
        

        return locationsongs

    def aggregateVotes(self, voteList):
        aggregatedVoteList = [voteList[0]]
        for vote in voteList:  
            for aggregatedVote in aggregatedVoteList:

                if vote.song_id != aggregatedVote.song_id:
                    aggregatedVoteList.append(vote)
                else:
                    aggregatedVote.rating += vote.rating
                    timedelta = aggregatedVote.created_time.timestamp() - vote.created_time.timestamp()
                    aggregatedVote.created_time = aggregatedVote.created_time + timedelta
        return aggregatedVoteList

    def get_top_ratings(self, aggregatedVoteList):
        variables = aggregatedVoteList[0].keys()
        df = pd.DataFrame([[getattr(i,j) for j in variables] for i in aggregatedVoteList], columns = variables)
        return df.sort_values('rating', ascending=False).head(5).to_dict()

                   