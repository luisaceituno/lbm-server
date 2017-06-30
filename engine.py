
class Engine():

    def __init__(self):
        pass

    def get_top_songlist(self, lon, lat):

        

        return "test"

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
        return[aggregatedVoteList]
