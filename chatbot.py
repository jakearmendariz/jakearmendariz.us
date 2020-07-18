from strava import *
import webbrowser
import os
from cmd_str import *
from activity_list import *

class Chatbot():
    def __init__(self, strava):
        self.strava = strava
        self.activity = None
        self.in_activity = False
        self.activity_list = None
        
    def get_response(self, user_input):
        user_input = user_input.lower()
        words = user_input.split(' ')
        print(words)
        if words[0] == 'info':
            print("info command")
            return self.info_cmd(words[1])
        if self.in_activity:
            return self.get_activity_response(user_input)
        if user_input == "cmd list":
            return self.command_list()
        if words[0] == 'checkout':
            self.activity = self.get_activity(int(words[1]))
            self.in_activity = True
            return "In activity:" + self.activity['name']
        if 'get' in user_input:
            print("getting activites")
            return "<a href= \"" + self.create_and_get_file(user_input)+ "\" target = \"blank\"> activity list </a>"
        if 'length' in user_input or 'size' in user_input:
            if(self.activity_list == None):
                return "No activity list"
            else:
                return str(len(self.activity_list))
        if('average' in user_input):
            print("AVERAGE IN USER INPUT")
            return str(self.average(user_input))
        return self.valid_commands()
    
    def command_list(self):
        return cmd_list
    
    def get_activity(self, id):
        return self.strava.get_activity_dict(id)
    
    def valid_commands(self):
        cmds = "List of valid commands:<br>"
        arr = activity_commands if self.in_activity else commands
        for cmd in arr:
           cmds  += cmd + "<br>"
        return cmds
    
    def info_cmd(self, cmd):
        if self.in_activity:
            try :
                index = activity_cmds.index(cmd)
            except ValueError:
                return self.valid_commands()
            return activity_commands_info[index]
        try :
            index = cmds.index(cmd)
        except ValueError:
            return self.valid_commands()
        return commands_info[index]
    
    def create_and_get_file(self, user_input):
        activity_list = ActivityList(self.activity_list)
        return activity_list.create_list(chatbot=self, user_input=user_input)
    
    def average(self, user_input):
        print("Finding the average")
        words = user_input.split()
        act_list = ActivityList(self.activity_list)
        return act_list.average(chatbot=self, stat=words[1])
    
    def get_activity_response(self, user_input):
        words = str(user_input).split(' ')
        if(words[0] == "exit"):
            self.in_activity = False
            return "exiting activity"
        if words[0] == "summary":
            return str(self.activity['name']) + ' is a ' + str(self.activity['type']) + ' it was ' + str(self.strava.to_miles(self.activity['distance'])) + 'miles'
        if user_input == "moving time":
            return str(self.activity['type']) + " was " + str(self.activity['moving_time'])
        elif user_input == "total time":
            return str(self.activity['type']) + " was " + str(self.activity['elapsed_time'])
        elif "time" in user_input:
            return str(self.activity['type']) + " was " + str(self.activity['moving_time']) + " of active time and " + str(self.activity['elapsed_time']) + "total time"
        return self.valid_commands()
            
                
        
