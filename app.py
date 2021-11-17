'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
app.py

Runs the rest of the application, imports all of the files
HTTPS: ! flask run --cert=cert.pem --key=key.pem
HTTP:  ! flask run

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('src/config.py')
mongo = PyMongo(app)

from src.models import *
from src.strava.strava_views import *
from src.basic_views import *
from src.blog_views import *
from src.tweet_views import *

if __name__ == '__main__':
    app.run(host='127.0.0.1', use_reloader=False, ssl_context=('cert.pem', 'key.pem'))
    # app.run(use_reloader=False, sl_context=('cert.pem', 'key.pem'))
    #   app.run(host='0.0.0.0', port = '5000', debug=True, use_reloader=True)

#>>>>>>> 34bb6ef4e1a0798553906b88dccd541239031030
