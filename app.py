# Main file

from binomial import Binomial
from flask_wtf import Form
import os
from flask import Flask, render_template, request
#from flask_mail import Message, Mail
from flask_pymongo import PyMongo

app = Flask(__name__)
#mail = Mail(app)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)
#user: dbuser - mypassword

from models import *
from views import *

if __name__ == '__main__':
    app.run()
