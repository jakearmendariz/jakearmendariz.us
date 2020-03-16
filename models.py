from app import mongo
from hashlib import sha224
from util import *
from flask_pymongo import pymongo


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
        # record = mongo.db.scores.find().sort(
        #   {"score": -1}, pymongo.DESCENDING)
        record = mongo.db.scores.find_one(sort=[("score", pymongo.ASCENDING)])
        return record['score']

    @staticmethod
    def userScore(email):
        record = mongo.db.scores.find_one({"email": email})
        if record == None:
            return 0
        return record['score']
