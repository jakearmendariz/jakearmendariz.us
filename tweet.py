import tweepy
from config import *
import re
from textblob import TextBlob
import numpy as np
import time
#from flask import make_responses


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
        try:
            public_tweets = self.api.search(q=word, lang="en", count=100)
        except:
            print("Rate limit exceeded")
            return
        print('total tweets:', len(public_tweets))
        average = 0
        for tweet in public_tweets:
            text = ' '.join(re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
            average += self.binaryClassifier(TextBlob(text).sentiment.polarity)
            # print(text, TextBlob(text).sentiment.polarity)

        average = average/len(public_tweets)
        average *= 100
        # print('\n', average, '% approval rating')
        return average

    # Hand in a username, and a word if you want to search for tweets with said word
    def getTweets(self, username, word='', count=20):
        try:
            user = self.api.get_user(username)
        except:
            print("User does not exist")
            return None
        try:
            tweets = self.api.user_timeline(
                screen_name=username, count=count, include_rts=True)
        except:
            print("Rate limit exceeded")
            return []
        # THERES A PROBLEM WHERE IF USER DOES NOT EXIST IT BREAKS
        # I THINK THE BEST SOLUTION IS JUST TO DO A TRY/CATCH STATEMENT, IF IT BREAKS, USER IS PRIVATE OR DNE
        if len(tweets) == 0:
            return []
        # else:
            # print(tweets)
        total = 0
        feed = []
        for tweet in tweets:
            if 'https://t.co' in tweet.text:
                index = tweet.text.index('https://t.co')
                if "media" in tweet.entities:
                    feed.append(
                        (tweet.text[0:index], tweet.entities['media'][0]['media_url']))
                    # print('\n\nmedia:', tweet.entities['media'])
                else:
                    feed.append(
                        (tweet.text[0:index], ''))
            else:
                feed.append(
                    (tweet.text[0:index], ''))
            total += 1
            # print(tweet)
        # print('post count:', user.statuses_count)
        print('count', total)
        return feed

    def getWrapped(self, username):
        try:
            user = self.api.get_user(username)
        except:
            print("User does not exist")
            return None
        average = ""
        try:
            tweets = self.api.user_timeline(
                screen_name=username, count=200, include_rts=False, exclude_replies=True)
        except:
            print("rate limit exceeded")
            return None
        # THERES A PROBLEM WHERE IF USER DOES NOT EXIST IT BREAKS
        # I THINK THE BEST SOLUTION IS JUST TO DO A TRY/CATCH STATEMENT, IF IT BREAKS, USER IS PRIVATE OR DNE
        if len(tweets) == 0:
            return []
        # else:
            # print(tweets)
        count = 0
        feed = []
        maxLikes = 0
        maxText = ''
        mostliked = 'fuck you'
        average = 0
        for tweet in tweets:
            if tweet.favorite_count > maxLikes:
                maxLikes = tweet.favorite_count
                mostliked = tweet
            count += 1
            # print(tweet)
            average += TextBlob(tweet.text).sentiment.polarity
            # print(TextBlob(tweet.text).sentiment.polarity)
        average /= count
        print("most liked tweet = ", mostliked.text, mostliked.created_at,
              maxLikes, "likes\nsentiment:", average)
        pass

    # Returns the best friend of the user
    # Ways to find this, search these tweets, every time a user likes a tweet or retweets add a weight, if users are two high for someone like trump
    # Lets just return the person who you retweet the most

    def bestFriend(self, username):
        try:
            user = self.api.get_user(username)
        except:
            print("User does not exist")
            return None

        friends = {}
        try:
            tweets = self.api.user_timeline(
                screen_name=username, count=30, include_rts=False, exclude_replies=True)
        except:
            print("rate limit exceeded")
            return None
        for tweet in tweets:
            retweets = self.api.retweets(tweet.id, count=5)
            # print(tweet.text)
            for retweet in retweets:
                # print("retweets:", retweet.user.screen_name)
                name = retweet.user.screen_name
                if name in friends:
                    friends[name] += 2
                else:
                    friends[name] = 2

        # analyzes the users who's posts the user liked
        for favorite in tweepy.Cursor(self.api.favorites, id=username).items(200):
            # To get diffrent data from the tweet do "favourite" followed by the information you want the response is the same as the api you refrenced too
            # Basic information about the user who created the tweet that was favorited
            # print('\n\n\nTweet Author:')
            # Print the screen name of the tweets auther
            # print('Screen Name: '+str(favorite.user.screen_name))
            # print('Name: '+str(favorite.user.name))
            if str(favorite.user.screen_name) in friends:
                friends[str(favorite.user.screen_name)] += 1
            else:
                friends[str(favorite.user.screen_name)] = 1

            # Basic information about the tweet that was favorited
            # print('\nTweet:')
            # Print the id of the tweet the user favorited
            # print('Tweet Id: '+str(favorite.id))
            # Print the text of the tweet the user favorited
            # print('Tweet Text: '+str(favorite.text.encode("utf-8")))
            # print('Posted on:', favorite.created_at)
            # Encoding in utf-8 is a good practice when using data from twitter that users can submit (it avoids the program crashing because it can not encode characters like emojis)
        # print(friends)
        max = 0
        bestfriend = ''
        for key in friends:
            value = friends[key]
            if value > max:
                bestfriend = key
                max = value
        print('best friend is', bestfriend, 'value', max)
        pass


API_KEY = 'v9gW9WQIOg50ItkObmNT6fLxK'
API_SECRET_KEY = 'kUd69URMSmqJhdC2JiDpLKQYvesT0XYEzpYj8LwWaaePz5gCET'

ACCESS_TOKEN = '1088520435656847360-Xah4d3GEOCSjbHvVItuKJRqsy0yzNN'
ACCESS_TOKEN_SECRET = 'pglDWUnuQbizA888laZh4kZTPVDDwSFpa1RTs28ISBjmN'

#hello = TwitterApi(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# ello.bestFriend('realdonaldtrump')
