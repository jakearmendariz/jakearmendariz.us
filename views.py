from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash
from app import app, mongo
from models import *
from flask_mail import Message, Mail
from tweet import *
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


app.secret_key = APP_SECRET_KEY
cookie = cookies.SimpleCookie()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)


@app.route('/tweet/', methods=['POST', 'GET'])
def search():
    print('tweeeet')
    if request.method == 'POST':
        print('finding tweets')
        tweepy = TwitterApi(API_KEY, API_SECRET_KEY,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        approval = tweepy.searchSediment(request.form.get('search'))
        if 'email' in session:
            return render_template('tweet.html', loggedin=True, answer=approval)
        return render_template('tweet.html', loggedin=False, answer=approval)
        # return render_template('tweet.html', answer=approval)
    if 'email' in session:
        return render_template('tweet.html', loggedin=True)
    return render_template('tweet.html', loggedin=False)


@app.route('/mytweets/', methods=['POST', 'GET'])
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
            result = str(approval) + '% approval rating'
            return render_template('tweet.html', loggedin=isloggedin, answer=result)
        if(query == 'All'):
            count = request.form.get('count')
            tweets = tweepy.getTweets(request.form.get('input'), count)
            return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'),  tweets=tweets)
        if(query == 'Wrapped'):
            userdict = tweepy.wrapped(request.form.get('input'))
            # return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'),  wrapped=True, profile_img='https://jakearmendariz.com/public/images/smile.jpg',
            #                       description='I like to eat cake', followers='followers', friends='friends',
            #                       date='October 11, 1999', popular_text='Corona virus is a fucking bummer',
            #                       popular_img='https://jakearmendariz.com/public/images/smile.jpg', tweet_sentiment=7, liked_sentiment=2)
            return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'), name=userdict['name'],  wrapped=True, profile_img=userdict['profile_img'],
                                   description=userdict['description'], followers=userdict['followers'], friends=userdict['friends'],
                                   date=datetime.strptime(userdict['created_at'], "%M %d, %Y"), popular_text=userdict['popular_tweet'][0],
                                   popular_img=userdict['popular_img'][1], tweet_sentiment=userdict['tweet_sentiment'], liked_sentiment=userdict['liked_sentiment'])
        # return render_template('tweet.html', answer=approval)
    return render_template('mytweets.html', loggedin=isloggedin)


def is_spam(name, msg):
    banned = ['sex', 'drugs', 'money', 'USD', '$',
              'singles', 'passive', 'adult', 'dating', '18']
    name = name.lower()
    msg = str(msg).lower()

    for word in banned:
        if word in name:
            return True
        if word in msg:
            return True
    return False

# Fill in the best score, and the world record score
@app.route('/games/lightspeed/', methods=['GET'])
def play():
    if 'email' in session:
        return render_template('/games/light.html', record=Score.worldRecord(), highscore=Score.userScore(session.get('email')), loggedin=True)
    return render_template('/games/light.html', record=Score.worldRecord(), highscore=Score.userScore(session.get('email')), loggedin=False)


@app.route('/games/lightspeed/', methods=['POST'])
def submitScore():
    print("Updating light speed scores")
    prev_best = request.form['highscore']
    print('request form[highscore]', prev_best)
    if 'email' in session:
        print('previous best:', prev_best)
        Score.update(session['email'], prev_best)
    else:
        print("USER NOT LOGGED IN, CANNOT SUBMIT HIGH SCORE!!!!")
    if 'email' in session:
        return render_template('/games/light.html', record=Score.worldRecord(), highscore=Score.userScore(session.get('email')), loggedin=True)
    return render_template('/games/light.html', record=Score.worldRecord(), highscore=Score.userScore(session.get('email')), loggedin=False)


@app.route('/games/', methods=['GET', 'POST'])
def showGames():
    print("Display playable games")
    return render_template('/games.html')


@app.route('/games/<string:page_name>/', methods=['GET'])
def render_games(page_name):
    if page_name == 'lightspeed':
        return render_template('/games/light.html')
    if page_name == 'snakers':
        return render_template('/games/snakers.html')
    if page_name == 'basic':
        return render_template('/games/basic.html')
    if page_name == 'flappy':
        return render_template('/games/flappy.html')
    return render_template('/games/index.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if session.get('email') != None:
            print("user already logged in, redirect")
            return redirect(url_for('viewTweets'))
        else:
            return render_template('login.html')
    if request.method == 'POST':
        if(session.get('delay') != None):
            diff = time.time()-session['delay']
            if diff < 30:
                print(diff, '/30 waited')
                return render_template('login.html', exception='You must wait 30 seconds before trying again')
        print("post request, logging user in signup page")
        result = request.form
        print('email is:', result['email'])
        user = mongo.db.users.find_one({'email': result['email']})
        if user == None:
            print('Did not find email')
            return render_template('login.html', exception='Email does not exist, please sign up')
        # IF USER PASSWORD IS ACCEPTED, CREATE SESSION
        if verify_password(user['password'], result['password']):
            print('Password match!')
            session['email'] = result['email']
            resp = make_response(render_template(
                "mytweets.html", loggedin=True))
            resp.set_cookie('email', result['email'], secure=True)
            return resp
            # return redirect(url_for('viewTweets'))
        else:
            print('Invalid password')
            if session.get('attempts') == None:
                print('first wrong attempt')
                session['attempts'] = 0
            else:
                session['attempts'] += 1
                print(session['attempts'], ' wrong attempt')
            if(session.get('attempts') > 5):
                session['attempts'] = 0
                session['delay'] = time.time()
                print('time delay start')
                return render_template('login.html', exception='You must wait 30 seconds before trying again')
            return render_template('login.html', exception='Invalid password')


def nameImage(filename, email):
    index = email.find('@')
    newname = email[:index] + filename
    print('naming image', )
    return newname


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        if 'email' in session:
            return redirect(url_for('viewTweets'))
        else:
            return render_template('signup.html')
    if request.method == 'POST':
        print('request.form', request.form)
        print('request.files', request.files)
        print("post request, creating user in signup page")
        result = request.form
        name = result.get('name')
        email = result.get('email')
        password = result.get('password')
        exists = mongo.db.users.find_one({'email': result['email']})
        if(exists != None):
            print('email already exists, cannot create')
            return render_template('signup.html', exception='email is already in use, please login')
        file = ''
        image = ''
        filename = ''
        if 'file' not in request.files:
            print("FILE WAS NOT FOUND")
            flash('No file part')
            return redirect(request.url)
        try:
            file = request.files["file"]
            print('Found the file!!!')
            filename = nameImage(file.filename, email)
            mongo.save_file(filename, file)
            print('Saved the file!!!')
        except:
            print('could not find the file name', sys.exc_info()[0])
            # return redirect(url_for('/signup/'), exception='did not find file')
            return render_template('signup.html', exception='did not find file')
        image = ''
        if file.filename == '':
            print('No selected file')
        user = User(name, email, hash_password(password), filename)
        user.dbInsert()
        print("User insert successful!")
        session['email'] = result['email']
        return redirect(url_for('viewTweets'))
    pass


@app.route('/file/<filename>/')
def file(filename):
    print('Display file')
    return mongo.send_file(filename)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/manageprofile/', methods=['GET', 'PUT', 'POST'])
def manageprofile():
    if request.method == 'GET':
        print('GET: manage profile')
        user = mongo.db.users.find_one({'email': session['email']})
        if user == None:
            print('Cannot find current user')
            return render_template('manageprofile.html')
        else:
            try:
                _src = url_for('file', filename=user['profile_img'])
                return render_template('manageprofile.html', name=user['name'], email=user['email'], src=_src)
            except:
                print('Error:', sys.exc_info()[0])
                return render_template('manageprofile.html', name=user['name'], email=user['email'])
    elif request.method == 'POST':
        print('POST: manage profile')
        filename = ''
        update = request.form
        print('new user:', update)
        print('new file:', request.files)
        if 'profile_img' in request.files:
            file = request.files['profile_img']
            if allowed_file(file.filename):
                print("updating profile image")
                filename = file.filename
                filename = nameImage(filename, session['email'])
                mongo.save_file(filename, file)
                update = update.copy()
                update['profile_img'] = filename
                print("updated profile image:", filename)
            else:
                print('no file submitted or unacceptable file')
        else:
            update = update.copy()
            del update['profile_img']
            print('no file submitted')
        print('Post request, going to update user')
        mongo.db.users.update_one(
            {'email': session['email']}, {"$set": update})
        print('User updated')
        user = mongo.db.users.find_one({'email': update['email']})
        if user == None:
            print("Error could not find new user")
            return render_template('manageprofile.html')
        else:
            print('manage profile, wth info')
            _src = url_for('file', filename=user['profile_img'])
            print(_src)
            return render_template('manageprofile.html', name=user['name'], email=user['email'], src=_src)
    else:
        print("Error:", request.method)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    # print(session)
    if 'email' in session:
        return render_template('index.html', loggedin=True)
    return render_template('index.html', loggedin=False)


@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def render_static(page_name):
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
