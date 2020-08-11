from app import mongo
from hashlib import sha224
from src.util import *
from flask_pymongo import pymongo
from src.tweet import *
from datetime import datetime
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib.pyplot import figure

fig, ax = plt.subplots()

class User():
    data = {}

    def __init__(self, name, email, password, profile_img):
        self.data['name'] = name
        self.data['email'] = email
        self.data['password'] = password
        self.data['id'] = sha224(email.encode('utf-8')).hexdigest()
        self.data['profile_img'] = profile_img
        print('new user:', self.data['name'],
              self.data['email'], self.data['password'])

    @staticmethod
    def signup(data):
        return User(data['name'], data['email'], data['password'], data['profile_img'])

    @staticmethod
    def login(dict):
        user = User("",
                    dict.get('email'),
                    dict.get('password'))
        userDict = user.dbRead()
        if not verify_password(userDict['password'], dict.get('password')):
            raise Exception("Invalid password")
        return userDict

    # simply return the response of the created login

    def dbInsert(self):
        print('dbinsert:', self.data['name'],
              self.data['email'], self.data['password'])
        return mongo.db.users.insert_one({
            '_id': self.data['id'],
            'name': self.data['name'],
            'email': self.data['email'],
            'password': self.data['password'],
            'profile_img': self.data['profile_img']
        })

     # read in the response
    def dbRead(self):
        document = mongo.db.users.find_one_or_404({"_id": self.id})
        print("Found the user")
        return document

# Class for storing data for my lightspeed game
# Only two variables, the email and the highscore


class Score():
    data = {}

    def __init__(self, email, score):
        self.data['email'] = email
        self.data['score'] = score
        print('New Score:',
              self.data['email'], self.data['score'])

    @staticmethod
    def update(email, new_score):
        score = Score(
            email,
            new_score)
        exists = score.dbRead()
        if exists == None:
            print("No score for", email, "existed")
            score.dbInsert()
            print("Inserted score of", score)
        else:
            print('exisiting score:', exists.get('score'))
            print('updated score:', new_score)
            if int(exists['score']) <= int(new_score):
                update = {}
                update['email'] = email
                update['score'] = new_score
                mongo.db.scores.update_one(
                    {'email': email}, {"$set": update})
                print("Updated ", email, " top score to ", new_score)
            else:
                print('Not a highscore, not updating database')
        return

    # simply return the response of the created login

    def dbInsert(self):
        print('dbinsert:', self.data['email'], self.data['score'])
        return mongo.db.scores.insert_one({
            'email': self.data['email'],
            'score': self.data['score'],
        })

     # read in the response
    def dbRead(self):
        document = mongo.db.scores.find_one(
            {"email": self.data['email']})
        print("Found the score")
        print(document)
        return document

    @staticmethod
    def worldRecord():
        record = mongo.db.scores.find_one(sort=[("score", pymongo.ASCENDING)])
        return record['score']

    @staticmethod
    def userScore(email):
        record = mongo.db.scores.find_one({"email": email})
        if record == None:
            return 0
        return record['score']


class Politician():
    people = ['Donald Trump', 'Hillary Clinton', 'Joe Biden',
              'Bernie Sanders', 'Nancy Pelosi', 'Mitch McConnell']

    def __init__(self, name):
        index = name.index(' ')
        self.name = name
        self.first = name[:index]
        self.last = name[index+1:]
        #print('politician:', self.first, self.last)
        pass

    def addPoll(self, twitter):
        politician = mongo.db.politics.find_one({"lastName": self.last})
        if politician == None:
            print("Could not find politician")
            return None
        rating = twitter.searchSediment(self.last)
        at = datetime.now().strftime("%B %d, %Y")
        politician['rating'].append((rating, at))
        mongo.db.politics.update_one(
            {'lastName': self.last}, {"$set": politician})
        print("Added rating to politician")

    def deleteAll(self):
        politician = mongo.db.politics.find_one({"lastName": self.last})
        if politician == None:
            print("Could not find politician")
            return None
        politician['rating'] = []
        mongo.db.politics.update_one(
            {'lastName': self.last}, {"$set": politician})
        print("Added rating to politician")

    @staticmethod
    def updateGraph():
        twitter = TwitterApi(API_KEY, API_SECRET_KEY,
                             ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        people = ['Donald Trump', 'Hillary Clinton', 'Joe Biden',
                  'Bernie Sanders', 'Nancy Pelosi', 'Mitch McConnell']
        for person in people:
            user = Politician(person)
            if user == None:
                return
            user.addPoll(twitter)
        print('all users updated')

    @staticmethod
    def zeroGraph():
        people = Politician.people
        for person in people:
            user = Politician(person)
            if user == None:
                return
            user.deleteAll()
        print('all users updated')

    @staticmethod
    def graph_politicians():
        plt.switch_backend('Agg')
        fig = plt.figure(figsize=(10, 7))
        # figure(figsize=(10,7))
        for person in Politician.people:
            index = person.index(' ')
            last = person[index+1:]
            politician = mongo.db.politics.find_one({"lastName": last})
            polls = []
            dates = []
            for poll in politician['rating']:
                polls.append(poll[0])
                dates.append(poll[1])
            polls = np.asarray(polls)
            dates = np.asarray(dates)
           
            line = pd.Series(data=polls, index=dates)
            line.plot(label=person, legend=True, linewidth=4.0)
            # Politician.smooth_line(person, dates, polls)
        plt.ylabel('polling')
        plt.xlabel('date')
        plt.title("Twitter Approval Rating Over Time")
        return mpld3.fig_to_html(fig)
    
    @staticmethod
    def smooth_line(person, x, y):
        x_range = np.arange(len(x))
        x_new = np.linspace(x_range[0], x_range[-1],2000)
        f = interp1d(x_range, y, kind='quadratic')
        y_smooth=f(x_new)
        ax.plot (x_new,y_smooth, label=person)

# Calls once a day to record politicans ratings. Cannot record with a static graph


def save_politician_ratings():
    Politician.updateGraph()
    pass


def delete_excess_files():
    print("removing excess files")
    for file in os.listdir('templates/strava_user_files/'):
        os.remove(os.path.join('templates/strava_user_files/', file))
    pass


# Politician.updateGraph()
# Politician.zeroGraph()
# Politician.graph_politicians()
