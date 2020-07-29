# Main file

from flask_wtf import Form
import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from werkzeug import serving
import ssl

# flask run --cert=cert.pem --key=key.pem
app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)

from models import *
from strava_views import *
from basic_views import *
from blog_views import *
from tweet_views import *


if __name__ == '__main__':
    app.run(use_reloader=False, sl_context=('cert.pem', 'key.pem'))
