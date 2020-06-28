from stravalib import Client
from config import *

class Strava():
    def __init__(self, access_token):
       self.client = Client (access_token = access_token)
       self.athlete = self.client.get_athlete()
       
    # def __init__(self, access_token):
    #     self.client = Client(access_token=access_token)
    #     self.athlete = self.client.get_athlete()
        
    def get_activites(self, count = 10):
        print(self.client.get_activites(limit=count))
        
    def get_name(self):
        return self.athlete.firstname + " " + self.athlete.lastname



# strava = Strava('4ff2e7879b14c4b0607595809cac9dd505c17d9c')
# print(strava.get_name())

