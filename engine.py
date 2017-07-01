from database import MongoDb
import json
from flask import jsonify
from bson import json_util
import pandas as pd
from datetime import datetime

TIME_BASE_FACTOR = 21600

class Engine():

    db = None

    def __init__(self):
        self.db = MongoDb()

    def post_vote(self, data):
        vote = json.loads(data)
        self.db.insert_vote(vote)

    def get_top_songlist(self, lon, lat):  
        votes= self.db.get_votes_by_loc(lon,lat,100)
        votes = self.calculate_rating(votes)

        aggrVotes = self.aggregate_votes(votes)
        top_dict = self.get_top_ratings(aggrVotes)

        location_songs = { "location": { "lon": lon, "lat": lat } }
        location_songs['songs'] = top_dict

        return location_songs

    def aggregate_votes(self, voteList):
        aggregatedVoteList = [voteList[0]]
        for vote in voteList:
            insert = True
            while insert == True:
                for aggregatedVote in aggregatedVoteList:
                    if vote['song_id'] == aggregatedVote['song_id']:
                        aggregatedVote['rating'] += vote['rating']
                        timedelta = aggregatedVote['created_time'].timestamp() - vote['created_time'].timestamp()
                        avg_time = aggregatedVote['created_time'].timestamp() + timedelta
                        aggregatedVote['created_time'] = datetime.fromtimestamp(avg_time)
                        insert = False
                    if insert == True:
                        aggregatedVoteList.append(vote)
        return aggregatedVoteList

    def get_top_ratings(self, aggregatedVoteList):
        variables = aggregatedVoteList[0].keys()
        df_votes = pd.DataFrame(aggregatedVoteList)
        df_votes_sorted = df_votes.sort_values('rating', ascending = False)

        df_votes_sorted.drop_duplicates('song_id', keep='first', inplace = True)
        df_votes_sorted.drop(df_votes_sorted.columns[[0, 1, 2]], axis=1, inplace=True)

        return df_votes_sorted.to_dict(orient='records')
                   
    def calculate_rating(self, aggregatedVoteList):
        for vote in aggregatedVoteList:
            time_delta = (datetime.now().timestamp() - vote['created_time'].timestamp() ) 
            time_factor = 1
            if time_delta > TIME_BASE_FACTOR and time_delta <= TIME_BASE_FACTOR*2:
                time_factor = 0.875
            elif time_delta > TIME_BASE_FACTOR*2 and time_delta <= TIME_BASE_FACTOR*3:
                time_factor = 0.75
            elif time_delta > TIME_BASE_FACTOR*3 and time_delta <= TIME_BASE_FACTOR*4:
                time_factor = 0.625
            elif time_delta > TIME_BASE_FACTOR*5:
                time_factor = 0.5
            vote['rating'] *= time_factor
        return aggregatedVoteList