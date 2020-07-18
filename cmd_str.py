import random
import string
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

cmd_list = "Command List:<br>get --object-- ex:get follower list<br>average pace --activity--average pace run<br>get summary --activity-id--get pace --activity-id--<br>get total time --activity_id--<br>get active time --activity_id--"

"""
Ideas
    get activites < 10                      -> gets list of activiites less than 10 miles
    get activites < 10 and less 2 hours     -> gets list of activities less than 10 miles and less than 2 hours active time
    get activites < 2 hours and > 10        -> gets list of activities less than 2 hours active time and more than 10 miles
    Rides:
        faster than 20 mph
        slower than 20 mph
    Runs:
        faster than 8 min/mile
        faster than 8 pace
        faster
"""

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
class commandStr():
    def __init__(self, user_input):
        self.user_input = user_input
        self.words = user_input.split()
        self.words = self.words[1:]
        self.length = len(self.words)
        self.clean()
        
    def clean(self):
        for i in range(self.length):
            if self.get(i) == 'less':
                self.words[i] = '<'
            if self.get(i) == 'greater':
                self.words[i] = '>'
            if self.get(i) in ['fastest', 'longest']:#moves the end of array
                word = self.get(i)
                del self.words[i]
                i -= 1
                self.words.append(word)
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