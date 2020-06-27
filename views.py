from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash
from app import app, mongo
from models import *
from flask_mail import Message, Mail
from tweet import *
from strava import *
from config import *
from werkzeug.utils import secure_filename
import os
import urllib.request
import sys
from pymongo import MongoClient
import gridfs
from util import *
import time
from http import cookies
from datetime import timedelta, datetime
from test import *
import matplotlib.pyplot as plt
import mpld3
import atexit
import requests
import werkzeug
import urllib3
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import urlencode #Allows me to encode url for strava oatuh
from stravalib import Client

app.secret_key = APP_SECRET_KEY
cookie = cookies.SimpleCookie()

strava_payload = {
    'client_id': STRAVA_CLIENT_ID,
    'client_secret':STRAVA_CLIENT_SECRET,
    #'refresh_token':STRAVA_REFRESH_TOKEN,
    #'grant_type':'refresh_token',
    'grant_type': 'authorization_code',
    'f':'json',
}

strava_oauth_payload = {
    'client_id': STRAVA_CLIENT_ID,
    'redirect_uri':'https://localhost:5000/strava/',
    'response_type':'code',
    'grant_type': 'authorization_code',
    'scope':'profile:read_all,read',
    'approval_prompt':'force'
}
strava_base_url = "https://www.strava.com/oauth/authorize"

strava_post_url = "https://www.strava.com/api/v3/oauth/token"

def get_strava_post_url():
    strava_post_url =  strava_post_url + '?' + urlencode(strava_payload)
    print("strava_post_url:", strava_post_url)
    return strava_post_url

def get_strava_oauth_url():
    strava_oath_url =  strava_base_url + '?' + urlencode(strava_oauth_payload)
    print("strava_uoath_url:", strava_oath_url)
    return strava_oath_url

stravaObj = ""


# Check models, this will save the politicians score twice a day at 12pm and 5pm. Then it will store in database
scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
# 12pm
scheduler.add_job(func=save_politician_ratings,
                  trigger="cron", hour=19, minute=0, second=0)
# 5p,
scheduler.add_job(func=save_politician_ratings,
                  trigger="cron", hour=0, minute=0, second=0)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

def getCode(url):
    end_of_url = url[url.index("code=")+5:]
    return end_of_url[:end_of_url.index("&")]

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)
    
@app.route('/strava-connect/', methods = ['GET', 'POST'])
def strava_connect():
    if(request.method == 'GET'):
        return render_template('/strava_connect.html', strava_auth_link = get_strava_oauth_url())
    print(request)
    print("post request to strava_connect")
    return render_template('/strava_connect.html');

@app.route('/strava/<string:url>/', methods = ['GET'])
def loginStrava(url):
    strava_payload['code'] = getCode(url)
    response = requests.post(strava_post_url, data = strava_payload)
    print("logged into strava\n\naccess_token = ", session['strava_access_token'])
    stravaObj = Strava(session['strava_access_token'])
    return render_template('/strava.html', full_name = "got access token, created object!")
    
    #return render_template('/strava.html', full_name = stravaObj.getFullName())
    #return redirect(url_for(displayStrava)


@app.route('/strava/', methods = ['GET, POST'])
def displayStrava():
    # stravaObj = Strava()
    # print("display strava")
    # print("rendering strava from display Strava()", stravaObj.getFullName())
    # return render_template('strava.html', full_name = stravaObj.getFullName())
    return render_template('strava.html')


@app.route('/twitteranalysis/', methods=['POST', 'GET'])
def viewTweets():
    isloggedin = 'email' in session
    if request.method == 'POST':
        # True if logged in, false if not
        print('finding tweets')
        tweepy = TwitterApi(API_KEY, API_SECRET_KEY,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        query = request.form.get("query")
        print('query:', query)
        if(query == "Sentiment"):
            approval = tweepy.searchSediment(request.form.get('input'))
            result = ' has a '+str(approval) + '% twitter approval rating'
            return render_template('mytweets.html', topic=request.form.get('input'), loggedin=isloggedin, answer=result, selectValue=3)
        elif(query == 'All'):
            count = request.form.get('count')
            tweets = tweepy.getTweets(request.form.get('input'), count=count)
            return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'),  tweets=tweets, count=count, all=True, selectValue=1)
        elif(query == 'Wrapped'):
            userdict = tweepy.wrapped(request.form.get('input'))
            if userdict == None:
                return render_template('mytweets.html', loggedin=isloggedin, answer='Does not Exists', selectValue=2)
            renderImage = True
            if userdict['popular_tweet'][1] == '':
                renderImage = False
            return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'), name=userdict['name'],  wrapped=True, profile_img=userdict['profile_img'],
                                   description=userdict['description'], followers=userdict['followers'], friends=userdict['friends'],
                                   date=userdict['created_at'].strftime("%B %d, %Y"), popular_text=userdict['popular_tweet'][0],
                                   popular_img=userdict['popular_tweet'][1], tweet_sentiment=userdict[
                                       'tweet_sentiment'], liked_sentiment=userdict['liked_sentiment'],
                                   bestfriend=userdict['bestfriend'], pop_likes=userdict['pop_likes'], pop_retweets=userdict[
                                       'pop_retweets'], renderImage=renderImage, selectValue=2,
                                   graph=userdict['graph'], sentiment=userdict['sentiment'])
        elif(query == 'Politics'):
            # Politician.updateGraph()
            return render_template('mytweets.html', loggedin=isloggedin, graph=Politician.graph_politicians(), politics=True, selectValue=4)
        # return render_template('tweet.html', answer=approval)   datetime.strptime(userdict['created_at'], "%M %d, %Y")
    return render_template('mytweets.html', loggedin=isloggedin, selectValue=0)


@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def render_static(page_name):
    # print("render_static",request.full_path, " page_name" + page_name)
    if("strava" in request.full_path ):
        print("strava in render_static")
        code = request.args.get('code')
        client = Client()
        access_token = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                              client_secret=STRAVA_CLIENT_SECRET,
                                              code=code)
        print("got the real access_token!!!")
        client = Client(access_token = access_token)
        render_template("/strava.html", full_name = client.get_athlete())
        
    if page_name == 'contact':
        if request.method == 'POST':
            mail = Mail(app)
            name = request.values.get('name')  # Your form's
            email = request.values.get('email')  # input names
            message = request.values.get('message')  # input names
            print('sending email')
            msg = Message(message,
                          sender="jakearmendariz99@gmail.com",
                          recipients=["jakearmendariz99@gmail.com"])
            msg.subject = name
            msg.body = email + "\n" + message
            if not is_spam(name, msg):
                mail.send(msg)
        elif request.method == 'GET':
            if(session.get('email') != None):
                user = mongo.db.users.find_one({'email': session['email']})
                return render_template('contact.html', name=user['name'], email=user['email'])
    if(page_name == 'games'):
        print("Games page!!!")
        return render_template('/games/games.html')
    return render_template('%s.html' % page_name)