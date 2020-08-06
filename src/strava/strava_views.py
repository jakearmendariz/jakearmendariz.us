from app import app, mongo
from src.models import *
from src.strava.strava import *
from src.config import *
from src.strava.chatbot import *
from src.util import *
from stravalib import Client


#For sessions
app.secret_key = APP_SECRET_KEY

chatbot = None

activities = None

# dictionary contains key:value between the [       strava_id     :       activity_dict     ]
#                                               (stored in session)
user_activities = {}

my_activities = None

def get_auth_url():
    client = Client()
    url = client.authorization_url(client_id=STRAVA_CLIENT_ID, scope = ['profile:read_all' , 'activity:read_all', 'read_all'],
    redirect_uri='https://localhost:5000/strava/')
    return url

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')    
    print('user:', userText)
    global chatbot
    return chatbot.get_response(userText)


@app.route('/strava', methods = ['GET, POST'])
def display_strava():
    print("display_strava")
    if('access_token' in session):
        try:
            strava = Strava(session['access_token'])
        except: #access_token was expired or broken. Restart initialization
            del session['access_token']
            return redirect(get_auth_url())
        print("athlete", strava.get_name())
        name = strava.get_name()
        session['strava_name'] = name
        global chatbot
        chatbot = Chatbot(strava)
        # graph = strava.graph_activity_distribution
        if(request.method == 'POST'):
            _graph = strava.graph_activity_distribution(line="smooth")
            return render_template('strava.html', full_name = name, graph=_graph, graphing=True, selectValue=2)
        return render_template('strava.html', full_name = name,selectValue=0)
    return redirect(get_auth_url())

def strava_authorization(code):
    client = Client()
    access_dict = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                            client_secret=STRAVA_CLIENT_SECRET,
                                            code=code)
    print("acces_token", access_dict['access_token'])
    client = Client(access_token = access_dict['access_token'])
    session['access_token'] = access_dict['access_token']
    session['strava_id'] = client.get_athlete().id
    return get_activities()

@app.route('/strava_user_files/<string:hash>/', methods=['GET', 'POST'])
def render_data(hash):
    print("rendering strava_user_file")
    return render_template('/strava_user_files/%s.html' % hash)

@app.route('/strava-activities', methods = ['GET, POST'])
@app.route('/strava_activities', methods = ['GET, POST'])
def get_activities():
    if('access_token' in session):
        try:
            client = Client(access_token =session['access_token'])
            client.get_athlete()
        except: #access_token was expired or broken. Restart initialization
            del session['access_token']
            return redirect(url_for(get_auth_url(), next= request.url))
    else:
        return redirect(url_for(get_auth_url(), next= request.url))
    global user_activities
    if session['strava_id'] not in user_activities:
        activities = ActivityList()
        activities.load_list()
        user_activities[session['strava_id']] = activities
        if 'admin' in session:
            print("SAVING ADMIN LIST FOR GUEST VIEWER!!!!")
            global my_activities
            my_activities = activities
    activities =  user_activities[session['strava_id']]
    form = request.form.to_dict()
    print(form)
    if(len(form) > 1):
        static_list = activities.create_filtered_list(form['query'], form['DistanceFrom'], form['DistanceTo'], form['PaceFrom'], form['PaceTo'],form['TimeFrom'], form['TimeTo'])
    elif(len(form) == 1):
        print("refresh list")
        activities.load_list()
        user_activities[session['strava_id']] = activities
        static_list = activities.get_full_list()
    else:
        static_list = activities.get_full_list()
    print("Got activities, rendering in html")
    
    if 'strava_name' not in session:
        strava = Strava(session['access_token'])
        session['strava_name'] = strava.get_name()
    if 'query' not  in form:
        form['query'] = 'All'
    return render_template('strava_activites.html', activities = static_list, form=form, name = session['strava_name'])

@app.route('/jakes-activities', methods = ['GET, POST'])
def get_my_activities():
    print("GET JAKES_ACTIVITIES!!!!")
    form = request.form.to_dict()
    db_strava = mongo.db.strava.find_one({'user':'jakearmendariz99@gmail.com'})
    db_activities = db_strava['activity']
    print("Got jakes activities from database")
    
    print(form)
    if(len(form) > 1):
        if 'query' not in form:
            form['query'] = 'All'
        static_list = ActivityList.static_filter(db_activities, form['query'], form['DistanceFrom'], form['DistanceTo'], form['PaceFrom'], form['PaceTo'],form['TimeFrom'], form['TimeTo'])
    else:
        # Refresh
        if(session['strava_id'] == 41359451): #If Jake is the one hitting refresh
            print("Jake is updating activities")
            activities = ActivityList()
            activities.load_list()
            db_strava['activity'] = activities.get_full_list()
            mongo.db.strava.update_one(
            {'email': 'jakearmendariz99@gmail.com'}, {"$set": db_strava})
        static_list = db_strava['activity']
    return render_template('strava_activites.html', activities = static_list, form=form, name = "Jake Armendariz")

@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def render_static(page_name):
    if("strava" in request.full_path):
        print("static strava")
        #If code is in the url then it was a authorization attempt. Else, user should have loggedin already
        code = request.args.get('code')
        if 'access_token' in session:
            if('strava-activities' in request.full_path):
                return get_activities()
            return get_activities()
        elif(code == None):
            return redirect(get_auth_url())
        return strava_authorization(code)
    if("jakes-activities" in request.full_path):
        return get_my_activities()
    return render_template('%s.html' % page_name)

