from stravalib import Client

class Strava():
    
    def __init__(self, access_token):
        self.client = Client(access_token=access_token)
        self.athlete = client.get_athlete()
        
    def getActivites(self, count = 10):
        print(self.client.get_activites(limit=count))
        
    def getFullName(self):
        return self.athlete['firstname'] + " " + self.athlete['lastname']

        