from strava import *

"""
Ideas
    cmp -> compares two activites, given their activity ID's
    

"""
class Chatbot():
    def __init__(self, strava):
        self.strava = strava
        self.activity = None
        self.in_activity = False
        
    def get_response(self, user_input):
        if self.in_activity:
            return self.get_activity_response(user_input)
        words = user_input.split(' ')
        if user_input == "cmd list":
            return self.command_list()
        if words[0] == 'checkout':
            self.activity = self.get_activity(int(words[1]))
            self.in_activity = True
            return "In activity:" + self.activity['name']
        return "Fuck you poser"
    
    def get_activity_response(self, user_input):
        words = str(user_input).split(' ')
        # self.diff("exit", words[0])
        print(words[0])
        if(words[0] == "exit"):
            self.in_activity = False
            return "exiting activity"
        if words[0] == "summary":
            return str(self.activity['name']) + ' is a ' + str(self.activity['type']) + ' it was ' + str(round(self.strava.to_miles(self.activity), 2)) + 'miles'
        if user_input == "moving time":
            return str(self.activity['type']) + " was " + str(self.activity['moving_time'])
        elif user_input == "total time":
            return str(self.activity['type']) + " was " + str(self.activity['elapsed_time'])
        elif "time" == user_input:
            return str(self.activity['type']) + " was " + str(self.activity['moving_time']) + " of active time and " + str(self.activity['elapsed_time']) + "total time"
        return words[0] + " is not a valid activity command<br>To leave activity type \'exit\'"
    
    def command_list(self):
        return "Command List:<br>get --object-- ex:get follower list<br>average pace --activity--average pace run<br>get summary --activity-id--get pace --activity-id--<br>get total time --activity_id--<br>get active time --activity_id--"
    
    def get_activity(self, id):
        return self.strava.get_activity_dict(id)
    
    
#2eafa54f4d16dd65805e3884d2c312db699d0f1b

    