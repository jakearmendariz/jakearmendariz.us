from app import mongo
from hashlib import sha224
from util import *


class User():
    data = {}

    def __init__(self, name, email, password):
        self.data['name'] = name
        self.data['email'] = email
        self.data['password'] = password
        self.data['id'] = sha224(email.encode('utf-8')).hexdigest()
        print('new user:', self.data['name'],
              self.data['email'], self.data['password'])

    @staticmethod
    def signup(data):
        return User(data['name'], data['email'], data['password'])

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
            'password': self.data['password']
        })

     # read in the response
    def dbRead(self):
        document = mongo.db.users.find_one_or_404({"_id": self.id})
        print("Found the user")
        return document
