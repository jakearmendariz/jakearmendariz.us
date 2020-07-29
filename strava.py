from stravalib import Client
from config import *
from datetime import datetime
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
    
    def to_miles(self, distance):
        return distance/1609.34
    
        
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
        result['distance'] = round(self.to_miles(activity_dict['distance']), 2)
        result['hours'] = int(activity_dict['moving_time'][0:1])
        result['date'] = activity_dict['start_date'][:10]
        arr = result['date'].split('-')
        result['date_value'] = int(arr[0])*365 + (int(arr[1])-1) * 30.5 + int(arr[2])
        result['moving_time'] = activity_dict['moving_time']
        result['elapsed_time'] = activity_dict['elapsed_time']
        result['total_elevation_gain'] = self.elavation_to_str(round(activity_dict['total_elevation_gain']*3.280839895))
        result['type'] = activity_dict['type']
        return result
    
    def elavation_to_str(self, elevation):
        return "{:,}".format(elevation)
            
        
    def add_pace(self, activity_list):
        for activity in activity_list:
            if(activity['type'] == 'Run'):
                activity['pace'] = self.get_pace(activity['distance'], activity['moving_time'])
                activity['pace_str'] = self.minutes_to_str(activity['pace']) + ' /mile'
            else:
                activity['pace'] = self.get_mph(activity['distance'], activity['moving_time'])
                activity['pace_str'] = str(activity['pace'])  + ' mph'
            # activity['pace_str'] = self.get_mph(activity['distance'], activity['moving_time']) * activity['distance']
        return activity_list
    
    def get_mph(self, distance, time):
        if not isinstance(time, float) and not isinstance(time, float):
            time = self.to_hours(time)
        if(distance == 0):
            return 0
        return round(float(distance)/time, 2)
    
    def get_pace(self, distance, time):
        if not isinstance(time, int) and not isinstance(time, float):
            time = self.to_minutes(time)
        return float(time)/distance
    
    def minutes_to_str(self, minutes):
        seconds = str(round((minutes%1)*60))
        if(len(seconds) == 1 and minutes%1 < 0.16):
            seconds = '0' + seconds
        elif(len(seconds) == 1):
            seconds = seconds + '0'
        
        return str(int(minutes)) + ':' + seconds
    
    def to_minutes(self, time):
        arr = [int(i) for i in time.split(':') if i.isdigit()]
        return arr[0]*60 + arr[1] + float(arr[2])/60
    
    def to_hours(self, time):
        arr = [float(i) for i in time.split(':') if i.isdigit()]
        return arr[0] + arr[1]/60 + arr[2]/3600
        