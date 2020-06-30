from strava import *
import webbrowser
import os
"""
Ideas
    get activites < 10                      -> gets list of activiites less than 10 miles
    get activites < 10 and less 2 hours     -> gets list of activities less than 10 miles and less than 2 hours active time
    get activites < 2 hours and > 10        -> gets list of activities less than 2 hours active time and more than 10 miles
"""


greetings = ['hi', 'hello', 'what\'s up', 'whats up']
cmds = ['checkout','cmp', 'total', 'get', 'info']
commands = ['checkout (activity_id)','cmp (activity_id) (activity_id)', 'total (entity)', 'get activity list', 'info (cmd)']
commands_info = ['checkout (activity_id): checkouts a specific activity by its id, once checking out an activity you can request more information such as pace and distance',
                 'cmp (activity_id) (activity_id): compares two activities, and each of their stats', 'total (entity): provides your profile total of either [milage, run milage, bike milage, time, followers, following]', 
                 'get activity list: Provides a list of activitites with their id\'s in a new window, so you can reference ids', 'info (cmd): provides information to each command']
activity_cmds = ['summary', 'moving_time', 'active_time', 'time', 'exit', 'info']
activity_commands = ['summary', 'moving time', 'active time', 'time', 'exit', 'info (cmd)']
activity_commands_info = ['summary: quick summary of activity', 'moving time: time strava detected movement', 'total time: time that strava was recording', 'time: moving and activity time summary', 
                          'exit: exits activity, return to home', 'info (cmd): provides information to each command']
compare = ['<', '>', 'less', 'greater']
import random
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
class commandStr():
    def __init__(self, user_input):
        self.user_input = user_input
        self.words = user_input.split()
        self.words = self.words[2:]
        self.length = len(self.words)
        self.clean()
        
    def clean(self):
        for i in range(self.length):
            if self.get(i) == 'less':
                self.words[i] = '<'
            if self.get(i) == 'greater':
                self.words[i] = '>'
        try:
            self.remove('than')
        except ValueError:
            print("than is not in input")
        
    def get(self, index):
        if index >= self.length:
            return ''
        else:
            return self.words[index]
        
    def get_length(self):
        return self.length
    
    def remove(self, word):
        self.words.remove(word)
        self.length = len(self.words)
        
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
        if 'get activities' in user_input:
            print("getting activites")
            return "<a href= \"" + self.write_activity_file(user_input)+ "\" target = \"blank\"> activity list </a>"
        return self.valid_commands()
    
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
    
    def command_list(self):
        return "Command List:<br>get --object-- ex:get follower list<br>average pace --activity--average pace run<br>get summary --activity-id--get pace --activity-id--<br>get total time --activity_id--<br>get active time --activity_id--"
    
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
    
    def write_activity_file(self, user_input):
        filename =  randomString(4) + str(self.strava.get_id())
        # os.remove("templates/" + filename + ".html")
        data = open("templates/strava_user_files/" + filename + ".html", "w+")
        self.activity_list = self.strava.get_activities()
        print('size of activity list', len(self.activity_list))
        self.clean_activities(user_input)
        data.write("<h1>Strava Activites</h1>")
        for activity in self.activity_list:
            print(activity['name'])
            namelink = "<a href= \"https://www.strava.com/activities/" + str(activity['id'])+ "\" target = \"blank\">"+ str(activity['name'])+ "</a>"
            data.write(str(activity['id']) + " " + namelink + " " + str(activity['distance']) + " miles "+ str(activity['elapsed_time']) + " total time recording<br><br>"  )
        data.close()
        self.activity_list = None
        return "https://localhost:5000/strava_user_files/" + filename
    
    
    def clean_activities(self, user_input):
        cmd = commandStr(user_input) 
        for i in range(0, cmd.get_length()):
            print('current command', cmd.get(i))
            if cmd.get(i) == '<':
                if(cmd.get(i+2) == 'hours' or cmd.get(i+2) == 'hour'):
                    self.less_than(float(cmd.get(i+1)), metric = "hours")
                else:
                    self.less_than(float(cmd.get(i+1)))
            if cmd.get(i) == '>':
                if(cmd.get(i+2) == 'hours' or cmd.get(i+2) == 'hour'):
                    self.greater_than(float(cmd.get(i+1)), metric = "hours")
                else:
                    self.greater_than(float(cmd.get(i+1)))
    
    #distance or moving_time
    def less_than(self, value, metric = "distance"):
        activities = []
        print("Only activities less than ", value, metric)
        for activity in self.activity_list:
            if(activity[metric] < value):
                activities.append(activity)
        self.activity_list = activities
        
    #distance or moving_time
    def greater_than(self, value, metric = "distance"):
        activities = []
        print("Only activities greater than ", value, metric)
        for activity in self.activity_list:
            if(activity[metric] > value):
                activities.append(activity)
        self.activity_list = activities
        
                
                
            
                
        
