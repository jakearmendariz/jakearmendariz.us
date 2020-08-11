'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
strava.py

Gets information from the stravalib api, builds the table, with only necessary data

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from stravalib import Client
from src.config import *
from src.strava.convert import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import re
from scipy.interpolate import interp1d
fig, ax = plt.subplots()


class Strava():
    def __init__(self, access_token):
       self.client = Client (access_token = access_token)
       self.athlete = self.client.get_athlete()
       
    def get_id(self):
        return self.athlete.id
        
    def get_activity_dict(self, id):
        return self.client.get_activity(id).to_dict()
        
    def get_name(self):
        return self.athlete.firstname + " " + self.athlete.lastname
        
    def get_activities(self, before_date = "2021-06-29T00:00:00Z"):
        activities = self.client.get_activities(before = before_date, after = "2017-01-01T00:00:00Z", limit=1200)
        arr = []
        for activity in activities:
            arr.append(self.activity_to_dict(activity))
        return arr
    
    # Condenses the array, removes the hundreds of unnecessary parameters
    def activity_to_dict(self, activity):
        activity_dict = activity.to_dict()
        result = {}
        result['id'] = activity.id
        result['name'] = activity_dict['name']
        result['distance'] = round(Convert.to_miles(activity_dict['distance']), 2)
        result['hours'] = int(activity_dict['moving_time'][0:1])
        result['date'] = activity_dict['start_date'][:10]
        arr = result['date'].split('-')
        result['date_value'] = int(arr[0])*365 + (int(arr[1])-1) * 30.5 + int(arr[2])
        result['moving_time'] = activity_dict['moving_time']
        result['elapsed_time'] = activity_dict['elapsed_time']
        result['total_elevation_gain'] = Convert.elavation_to_str(round(activity_dict['total_elevation_gain']*3.280839895))
        result['type'] = activity_dict['type']
        return result   
        
    def add_pace(self, activity_list):
        for activity in activity_list:
            if(activity['type'] == 'Run'):
                activity['pace'] = Convert.get_pace(activity['distance'], activity['moving_time'])
                activity['pace_str'] = Convert.minutes_to_str(activity['pace']) + ' /mile'
            else:
                activity['pace'] = Convert.get_mph(activity['distance'], activity['moving_time'])
                activity['pace_str'] = str(activity['pace'])  + ' mph'
        return activity_list
    