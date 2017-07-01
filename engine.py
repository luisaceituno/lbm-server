from database import MongoDb
import json
from flask import jsonify
from bson import json_util
import pandas as pd
import datetime

TIME_BASE_FACTOR = 21600

class Engine():

    db = None

    def __init__(self):
        self.db = MongoDb()

    def post_vote(self, data):
        vote = json.loads(data)
        self.db.insert_vote(vote)

    def get_top_songlist(self, lon, lat, radius):  
        votes= self.db.get_votes_by_loc(lon,lat, radius)
        votes = self.calculate_rating(votes)

        aggrVotes = self.aggregate_votes(votes)
        top_dict = self.get_top_ratings(aggrVotes)

        location_songs = { "location": { "lon": lon, "lat": lat } }
        location_songs['songs'] = top_dict

        return location_songs

    def aggregate_votes(self, voteList):
        aggregated_votelist = [voteList[0]]
        for vote in voteList:
            insert = True
            while insert == True:
                for aggregated_vote in aggregated_votelist:
                    if vote['song_id'] == aggregated_vote['song_id']:
                        aggregated_vote['rating'] += vote['rating'] #interpreted as string??
                        timedelta = aggregated_vote['created_time'].timestamp() - vote['created_time'].timestamp()
                        avg_time = aggregated_vote['created_time'].timestamp() - timedelta
                        aggregated_vote['created_time'] = datetime.datetime.fromtimestamp(avg_time)
                        insert = False
                if insert == True:
                    aggregated_votelist.append(vote)
                    insert = False
        return aggregated_votelist

    def get_top_ratings(self, aggregated_votelist):
        variables = aggregated_votelist[0].keys()
        df_votes = pd.DataFrame(aggregated_votelist)
        df_votes_sorted = df_votes.sort_values('rating', ascending = False)

        df_votes_sorted.drop_duplicates('song_id', keep='first', inplace = True)
        df_votes_sorted.drop(df_votes_sorted.columns[[0, 1, 2]], axis=1, inplace=True)

        return df_votes_sorted.to_dict(orient='records')
                   
    def calculate_rating(self, aggregated_votelist):
        for vote in aggregated_votelist:
            time_delta = (datetime.datetime.now().timestamp() - vote['created_time'].timestamp() ) 
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
        return aggregated_votelist