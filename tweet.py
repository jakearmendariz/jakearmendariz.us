import tweepy
from config import *
import re
from textblob import TextBlob
import numpy as np
import time


class TwitterApi():
    def __init__(self, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        auth = tweepy.OAuthHandler(API_KEY,
                                   API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN,
                              ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def binaryClassifier(self, sediment):
        if sediment > 0:
            return 1
        else:
            return 0

    def searchSediment(self, word):
        public_tweets = self.api.search(q=word, lang="en", count=100)
        print('total tweets:', len(public_tweets))
        average = 0
        for tweet in public_tweets:
            text = ' '.join(re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
            average += self.binaryClassifier(TextBlob(text).sentiment.polarity)
            #print(text, TextBlob(text).sentiment.polarity)

        average = average/len(public_tweets)
        average *= 100
        #print('\n', average, '% approval rating')
        return average

    # Hand in a username, and a word if you want to search for tweets with said word
    def getTweets(self, username, word=''):
        try:
            user = self.api.get_user(username)
        except:
            print("User does not exist")
            return None
        print('post count:', user.statuses_count)
        pass
