
class CreateFile():
    def __init__(self, activity_list=None):
        self.activity_list = activity_list
    
    def write_header(self, file):
        file.write("<h1>Strava Activites</h1>")
        file.write("<script src=\"../../static/js/strava_table.js\"></script>")
        file.write("<link rel=\"stylesheet\" href=\"../../static/css/activity_list.css\" /> <table  id = \"table\">")
        file.write("<tr><th onclick=\"sortTable(0)\">Activity-id</th><th onclick=\"sortTable(1)\">Date</th><th onclick=\"sortTable(2)\">Name & Link to acitivty</th><th onclick=\"sortTable(3)\">Pace</th><th onclick=\"sortTable(4)\">Distance</th><th onclick=\"sortTable(5)\">Moving Time</tr>")
        file.write("<link href=\"https://fonts.googleapis.com/css?family=Ubuntu&display=swap\"rel=\"stylesheet\"/>")


    def write_to_activity_file(self, chatbot, user_input):
        filename = str(chatbot.strava.get_id()) + randomString(4)
        data = open("templates/strava_user_files/" + filename + ".html", "w+")
        self.write_header(file=data)
        for activity in self.activity_list:
            namelink = "<a href= \"https://www.strava.com/activities/" + str(activity['id'])+ "\" target = \"blank\">"+ str(activity['name'])+ "</a>"
            data.write("<tr><td>" + str(activity['id']) + "</td><td>" + str(activity['date'][:10]) + "</td><td>" + namelink + "</td><td>"+ activity['pace_str'] +"</td><td>" + str(activity['distance']) + " miles</td><td>"+ str(activity['moving_time']) + "</tr><br><br>")
        data.write("</table>")
        data.close()
        return "https://localhost:5000/strava_user_files/" + filename
    
    
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
        
    def average(self, chatbot, stat):
        if stat == 'pace':
            print("find average pace on these activities")
            total_time = 0 #in minutes
            total_dist = 0 #in miles
            for activity in self.activity_list:
                time_arr = str(activity['moving_time']).split(':')
                total_time += int(time_arr[0])*60 + int(time_arr[1])
                total_dist += activity['distance']
            pace = Convert.get_pace(total_time, total_dist)  
            return str(int(pace)) + ':' + str(round((pace%1)*60))  
        elif stat == 'elevation':
            return sum(activity['total_elevation_gain'] for activity in self.activity_list)/len(self.activity_list)
        elif stat == 'distance':
            return sum(activity['distance'] for activity in self.activity_list)/len(self.activity_list)
        elif stat == 'time':
            total = sum(Convert.to_minutes(activity['moving_time']) for activity in self.activity_list)/len(self.activity_list)
            return str(int(total/60)) + ':' + Convert.minutes_to_str(total%60)
        else:
            return "Could not find metric"
    
    
        def type_of(self, activity_type):
            activities = []
        for activity in self.activity_list:
            if(activity['type'] == activity_type):
                activities.append(activity)
        self.activity_list = activities
        
    def clean_activities(self, user_input):
        cmd = commandStr(user_input) 
        for i in range(0, cmd.get_length()):
            print('current command', cmd.get(i))
            if(cmd.get(i) == 'runs'):
                self.type_of('Run')
            if(cmd.get(i) == 'rides'):
                self.type_of('Ride')
            if(cmd.get(i) == 'swims'):
                self.type_of('Swim')
            if cmd.get(i) == '<':
                if(cmd.get(i+2) == 'hours' or cmd.get(i+2) == 'hour'):
                    self.less_than(float(cmd.get(i+1)), metric = "hours")
                else:
                    self.less_than(float(cmd.get(i+1)))
            if cmd.get(i) == '>':
                print(">")
                if(cmd.get(i+2) == 'hours' or cmd.get(i+2) == 'hour'):
                    self.greater_than(float(cmd.get(i+1))-1, metric = "hours")
                else:
                    self.greater_than(float(cmd.get(i+1)))
                    
        def create_list(self, chatbot, user_input):
            self.activity_list = chatbot.strava.get_activities()
        print('size of activity list', len(self.activity_list))
        self.clean_activities(user_input)
        #Adds pace after taking out the needed tasks
        self.activity_list = chatbot.strava.add_pace(self.activity_list)
        # self.activity_list = self.sort()
        chatbot.activity_list = self.activity_list
        return self.write_to_activity_file(chatbot, user_input)