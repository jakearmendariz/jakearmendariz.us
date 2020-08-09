'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
activity_list.py

Activity list, for sorting and displaying user data

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from src.strava.cmd_str import *
from src.strava.strava import *
from src.strava.convert import *
from flask import  session

MAX = 1000000
MIN = 0
class ActivityList():
    def __init__(self, activity_list=None):
        self.activity_list = activity_list
    
    # Loads list to the class
    def load_list(self):
        strava = Strava(session['access_token'])
        self.activity_list = strava.get_activities()
        self.activity_list = strava.add_pace(self.activity_list)
        
    # Returns full activity list
    def get_full_list(self):
        return self.activity_list
    
    # Returns a filtered list
    def create_filtered_list(self,activity_type='All', distanceFrom = 0, distanceTo = 10000, paceFrom = 0, paceTo = 1000, timeFrom = 0, timeTo=100000):
        parameters = ActivityList.clean_form_input(distanceFrom, distanceTo, paceFrom, paceTo, timeFrom, timeTo)
        return ActivityList.activity_filter(self.activity_list, activity_type, parameters)
    
    # Returns a static filter of the list
    @staticmethod
    def static_filter(activity_list, activity_type='All', distanceFrom = 0, distanceTo = 10000, paceFrom = 0, paceTo = 1000, timeFrom = 0, timeTo=100000):
        parameters = ActivityList.clean_form_input(distanceFrom, distanceTo, paceFrom, paceTo, timeFrom, timeTo)
        return ActivityList.activity_filter(activity_list, activity_type, parameters)
    
    # Cleans the data. Factors in dates, time, pace, distance and activity type
    @staticmethod
    def activity_filter(activity_list, activity_type, parameters):
        filtered_list = []
        for activity in activity_list:
            if(activity_type != 'All'):
                if(activity_type != activity['type']):
                    continue
            if activity['distance'] > parameters['distanceFrom'] and  activity['distance'] < parameters['distanceTo']:
                if activity['pace'] > parameters['paceFrom'] and  activity['pace'] < parameters['paceTo']:
                    if activity['date_value'] > parameters['timeFrom'] and activity['date_value'] < parameters['timeTo']:
                        filtered_list.append(activity)
        return filtered_list
    
        
    @staticmethod
    def clean_form_input(distanceFrom, distanceTo, paceFrom, paceTo, timeFrom, timeTo):
        distanceFrom = ActivityList.sanitize_input(distanceFrom, MIN)
        distanceTo = ActivityList.sanitize_input(distanceTo, MAX)
        
        paceFrom = ActivityList.sanitize_input(paceFrom, MIN)
        paceTo = ActivityList.sanitize_input(paceTo,MAX)
        
        timeFrom = ActivityList.sanitize_time(timeFrom, MIN)
        timeTo = ActivityList.sanitize_time(timeTo, MAX)
        
        return {"distanceFrom": distanceFrom, "distanceTo": distanceTo, "paceFrom": paceFrom, "paceTo": paceTo, "timeFrom": timeFrom,"timeTo":timeTo}
            
    @staticmethod
    def sanitize_input(input, default_value):
        if (input != ''):
            input = int(input)
        else:
            input = default_value
        return input
    
    @staticmethod
    def sanitize_time(time, default_value):
        if (time ==''):
            time = default_value
        elif(not isinstance(time, int)):
            arr = time.split('-')
            time = int(arr[0])*365          # years
            if(len(arr) > 1):
                time += int(arr[1]-1) * 30  # Months (subtract 1 bc january is month 0)
            elif(len(arr) > 2):
                time += int(arr[2])         # Days
        return time