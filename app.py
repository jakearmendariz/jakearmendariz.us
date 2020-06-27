# Main file

from flask_wtf import Form
import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from werkzeug import serving
import ssl


# app = Flask(__name__)
# app.config.from_pyfile('config.py')
# mongo = PyMongo(app)

# from models import *
# from views import *

# HTTPS - PYTHON2 ( i think)
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt') # inside of app.run (, ssl_context=context)

# HTTPS_ENABLED = True
# VERIFY_USER = False
# API_HOST = "0.0.0.0"
# API_PORT = 5000
# API_CRT = "server.crt"
# API_KEY = "server.key"
# API_CA_T = "ca.crt"
# context = None

# if HTTPS_ENABLED:
#     context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#     if VERIFY_USER:
#         context.verify_mode = ssl.CERT_OPTIONAL
#         #context.load_verify_locations(API_CA_T)
#     try:
#         context.load_cert_chain(API_CRT, API_KEY)
#     except Exception as e:
#         sys.exit("Error starting flask server. " +
#             "Missing cert or key. Details: {}"
#             .format(e))
# serving.run_simple(
#     API_HOST, API_PORT, app, ssl_context=context)


# flask run --cert=cert.pem --key=key.pem
app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)

from models import *
from views import *
from basic_views import *


if __name__ == '__main__':
    app.run(use_reloader=False, sl_context=('cert.pem', 'key.pem'))
