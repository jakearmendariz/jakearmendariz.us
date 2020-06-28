from stravalib import Client
from config import *

class Strava():
    def __init__(self, access_token):
       self.client = Client (access_token = access_token)
       self.athlete = self.client.get_athlete()
       
    # def __init__(self, access_token):
    #     self.client = Client(access_token=access_token)
    #     self.athlete = self.client.get_athlete()
        
    def getActivites(self, count = 10):
        print(self.client.get_activites(limit=count))
        
    def getFullName(self):
        return self.athlete.firstname + " " + self.athlete.lastname

#auth = Client.authorization_url(client_id = STRAVA_CLIENT_ID, redirect_uri = 'localhost:5000', approval_prompt=u'auto')
# strava = Strava()
# print(strava.getFullName())

# client = Client (access_token = '63a4ca6ee769c485b550437d2a3d7a25802fd592')
# print(client.())


# strava = Strava('4ff2e7879b14c4b0607595809cac9dd505c17d9c')
# print(strava.getFullName())

