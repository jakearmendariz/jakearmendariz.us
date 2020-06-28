from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash
from app import app, mongo
from models import *
from strava import *
from config import *
from werkzeug.utils import secure_filename
from flask_mail import Message, Mail
import os
import urllib.request
import sys
from pymongo import MongoClient
import gridfs
from util import *
import time
from http import cookies
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import mpld3
import atexit
import requests
import werkzeug
import urllib3
from urllib.parse import urlencode #Allows me to encode url for strava oatuh
from stravalib import Client

#For sessions
app.secret_key = APP_SECRET_KEY

def get_auth_url():
    client = Client()
    url = client.authorization_url(client_id=STRAVA_CLIENT_ID, scope = ['profile:read_all' , 'activity:read_all', 'read_all'],
    redirect_uri='https://localhost:5000/strava/')
    return url


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
        return render_template('strava.html', full_name = name)
    return redirect(get_auth_url())

def strava_authorization(code):
    client = Client()
    access_dict = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                            client_secret=STRAVA_CLIENT_SECRET,
                                            code=code)
    print("acces_token", access_dict['access_token'])
    client = Client(access_token = access_dict['access_token'])
    session['access_token'] = access_dict['access_token']
    return display_strava()


@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def render_static(page_name):
    if("strava" in request.full_path ):
        print("static strava")
        #If code is in the url then it was a authorization attempt. Else, user should have loggedin already
        code = request.args.get('code')
        if(code == None and 'access_token' in session):
            return display_strava()
        return strava_authorization(code)
    return render_template('%s.html' % page_name)
