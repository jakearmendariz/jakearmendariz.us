from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash
from app import app
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

app.secret_key = APP_SECRET_KEY
db = MongoClient().userdb
fs = gridfs.GridFS(db)


@app.route('/tweet/', methods=['POST'])
def search():
    print('tweeeet')
    if request.method == 'POST':
        print('finding tweets')
        tweepy = TwitterApi(API_KEY, API_SECRET_KEY,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        approval = tweepy.searchSediment(request.form.get('search'))
        return render_template('tweet.html', answer=approval)


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


@app.route('/games/<string:page_name>/', methods=['GET', 'POST'])
def render_games(page_name):
    if page_name == 'lightspeed':
        return render_template('/games/light.html')
    if page_name == 'snake':
        return render_template('/games/snake.html')
    if page_name == 'basic':
        return render_template('/games/basic.html')
    if page_name == 'flappy':
        return render_template('/games/flappy.html')
    return render_template('/games/index.html')


@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        print("post request, logging user in signup page")
        result = request.form
        print('email is:', result['email'])
        user = mongo.db.users.find_one({'email': result['email']})
        if user == None:
            print('Did not find email')
            return render_template('login.html', exception='Email does not exist, please sign up')
        if user['password'] == result['password']:
            print('Password did not match')
            session['email'] = result['email']
            return redirect(url_for('index'))
        else:
            print('Invalid password')
            return render_template('login.html', exception='Invalid password')


@app.route('/file/', methods=['POST'])
def savefile():
    print('save file')
    if request.method == 'POST':
        name = request.form['name']
        print("post request, creating user in signup page")
        print('request.form', request.form)
        print('request.files', request.files)
        if 'file' not in request.files:
            print("FILE WAS NOT FOUND")
            flash('No file part')
            return redirect(request.url)
        try:
            file = request.files.get("file")
            print('Found the file!!!')
        except:
            print('could not find the file name', sys.exc_info()[0])
            # return redirect(url_for('/signup/'), exception='did not find file')
            return render_template('signup.html', exception='did not find file')
        image = ''
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        else:
            print('Creating path to file')
            filename = secure_filename(file.filename)
            path = os.path.join(
                '/Users/jakearmendariz/Desktop/flaskapp/static/profile_images/', name)
            file.save(path)
            print('Saved:', filename)
            image = filename
            session['email'] = 'fuckyes'
            return redirect(url_for('index'))


@app.route('/signup/', methods=['POST'])
def signup():
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
        if 'file' not in request.files:
            print("FILE WAS NOT FOUND")
            flash('No file part')
            return redirect(request.url)
        try:
            file = request.files["file"]
            print('Found the file!!!')
            #mongo.save_file(email, file)
            print('Saved the file!!!')
        except:
            print('could not find the file name', sys.exc_info()[0])
            # return redirect(url_for('/signup/'), exception='did not find file')
            return render_template('signup.html', exception='did not find file')
        image = ''
        if file.filename == '':
            print('No selected file')
        else:  # Saves the file,
            filename = secure_filename(file.filename)
            path = os.path.join(
                '/Users/jakearmendariz/Desktop/flaskapp/static/profile_images', email)
            file.save(path)
        user = User(name, email, password)
        user.dbInsert()
        print("User insert successful!")
        session['email'] = result['email']
        return redirect(url_for('index'))
    pass


def create_user():
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
        if 'file' not in request.files:
            print("FILE WAS NOT FOUND")
            flash('No file part')
            return redirect(request.url)
        try:
            file = request.files.get("file")
            print('Found the file!!!')
        except:
            print('could not find the file name', sys.exc_info()[0])
            # return redirect(url_for('/signup/'), exception='did not find file')
            return render_template('signup.html', exception='did not find file')
        image = ''
        if file.filename == '':
            print('No selected file')
        else:  # Saves the file,
            filename = secure_filename(file.filename)
            path = os.path.join(
                '/Users/jakearmendariz/Desktop/flaskapp/static/profile_images', email)
            file.save(path)
        user = User(name, email, password)
        user.dbInsert()
        print("User insert successful!")
        session['email'] = result['email']
        return redirect(url_for('index'))


@app.route('/file/<filename>/')
def file(filename):
    print('Display file')
    return mongo.send_file(filename)


@app.route('/manageprofile/', methods=['GET', 'POST'])
def manageprofile():
    if request.method == 'GET':
        print('manage profile')
        user = mongo.db.users.find_one({'email': session['email']})
        if user == None:
            return render_template('manageprofile.html')
        else:
            print('manage profile, wth info')
            try:
                return render_template('manageprofile.html', name=user['name'], email=user['email'])
            except:
                print('Error:', sys.exc_info()[0])
                return render_template('manageprofile.html', name=user['name'], email=user['email'])

    else:
        print('Post request, going to update user')
        update = request.form
        mongo.db.users.update_one(
            {'email': session['email']}, {"$set": update})
        print('User updated')
        print('manage profile')
        user = mongo.db.users.find_one({'email': update['email']})
        if user == None:
            return render_template('manageprofile.html')
        else:
            print('manage profile, wth info')
            _src = url_for('file', filename=user['email'])
            print(_src)
            return render_template('manageprofile.html', name=user['name'], email=user['email'], src=_src)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', loggedin=True)
    return render_template('index.html', loggedin=False)


@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def render_static(page_name):
    if page_name == 'probability':
        if request.method == 'POST':
            result = request.form
            a = result.get('probability')
            b = result.get('trials')
            obj = Binomial(float(a))
            _answer = obj.probablityofsuccess(int(b), 1)
            return render_template('probability.html', answer=_answer)
        else:
            _answer = ""
            return render_template('probability.html', answer=_answer)
    if page_name == 'answer':
        result = request.form
        a = 'nick'
        a += ' is gay'
        return render_template('answer.html', answer=a)
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
    if(page_name == 'games'):
        print("Games page!!!")
        return render_template('/games/games.html')
    return render_template('%s.html' % page_name)
