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
       
        
    def get_activites(self, count = 10):
        print(self.client.get_activites(limit=count))
        
    def get_name(self):
        return self.athlete.firstname + " " + self.athlete.lastname
    
    def to_miles(self, activity):
        return activity['distance']/1609.34
    
    def graph_activity_distribution(self, line = None):
        fig, ax = self.init_graph()
        if line != None and line == "smooth":
            self.get_activity_smooth_line(ax=ax)
            return mpld3.fig_to_html(fig)
        else:
            line = self.get_activity_line()
            line.plot(linewidth=2.5)
            return mpld3.fig_to_html(fig)
    
    def init_graph(self):
        plt.switch_backend('Agg')
        plt.ylabel('miles')
        plt.xlabel('time')
        plt.title('Distance over time')
        fig, ax = plt.subplots(figsize=(8, 4))
        return fig, ax
        
    def get_activity_line(self):
        dates, distances = self.get_dates_and_distances()
        return pd.Series(data=np.array(distances), index=np.array(dates))

    
    def get_activity_smooth_line(self, fig = None, ax = ax):
        dates, distances = self.get_dates_and_distances()
        x = self.turn_dates_into_numbers(dates)
        x_new = np.linspace(x[0], x[-1],2000)
        f = interp1d(x, distances, kind='quadratic')
        y_smooth=f(x_new)
        ax.plot (x_new,y_smooth, label="pace")
    
    def get_dates_and_distances(self, before_date = "2020-06-29T00:00:00Z"):
        activities = self.client.get_activities(before = before_date,  limit=750)
        distances, dates = [], []
        for activity in activities:
            activity = activity.to_dict()
            dates.append(activity['start_date_local'])
            distances.append(self.to_miles(activity))
        return np.array(dates), np.array(distances)
        
    def turn_dates_into_numbers(self, dates):
        return np.arange(len(dates))
    
    #Turns dates and activites into miles/week
    def miles_per_week(self):
        pass
