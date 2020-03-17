import tweepy
from config import *
import re
from textblob import TextBlob
import numpy as np
import time
# from flask import make_responses


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
            print(text, TextBlob(text).sentiment.polarity)

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

    def wrapped(self, username):
        try:
            user = self.api.get_user(username)
        except:
            print("User does not exist")
            return None
        userdict = self.bestFriend(username)
        userdict['location'] = user.location
        userdict['name'] = user.name
        userdict['followers'] = user.followers_count
        userdict['friends'] = user.friends_count
        userdict['posts'] = user.statuses_count
        userdict['created_at'] = user.created_at
        userdict['profile_img'] = user.profile_image_url_https
        userdict['description'] = user.description
        print(userdict)
        return userdict

    # Determines best friend on 3 factors
    # Who has retweeted your tweets the most
    # In your last 200 likes, who you have liked the most
    # Who's tweets you reply to the most often
    # And who's tweets you retweet the most often
    def bestFriend(self, username):
        try:
            user = self.api.get_user(username)
            # Checks for correct case with input
            username = user.screen_name
        except:
            print("User does not exist")
            return None

        friends = {}
        friends[username] = 0
        likedSentiment = 0
        tweetSentiment = 0

        # analyzes the users who's posts the user liked
        count = 0
        for favorite in tweepy.Cursor(self.api.favorites, id=username).items(200):
            if str(favorite.user.screen_name) in friends:
                friends[str(favorite.user.screen_name)] += 1
            else:
                friends[str(favorite.user.screen_name)] = 1
            count += 1
            likedSentiment += TextBlob(favorite.text).sentiment.polarity

        likedSentiment /= count
        liked = count
        count = 0
        # PULLS REGULAR TWEETS
        popular_tweet = [None, 0]
        try:
            tweets = self.api.user_timeline(
                screen_name=username, count=200, include_rts=True)
        except:
            print("did not pull tweets")
            return
        # CHECK REPLIES-- SEE WHO LIKED IT
        for tweet in tweets:
            repliedto = tweet.in_reply_to_screen_name
            if repliedto != None:
                if str(repliedto) in friends:
                    friends[str(repliedto)] += 1
                else:
                    friends[str(repliedto)] = 1
            try:
                retweeted = str(tweet.retweeted_status.user.screen_name)
                if retweeted in friends:
                    friends[retweeted] += 1
                else:
                    friends[retweeted] = 1
            except:
                count += 1
                tweetSentiment += TextBlob(tweet.text).sentiment.polarity
                compare = tweet.favorite_count + tweet.retweet_count*2
                if compare > popular_tweet[1]:
                    popular_tweet[0] = tweet
                    popular_tweet[1] = compare

        tweetSentiment /= count
        # Gets the maximum key value
        friends[username] = 0
        bestfriend = max(friends, key=friends.get)
        # print(friends)
        print('\n\nbest friend is', bestfriend, 'value', max)
        user = {}
        user['bestfriend'] = bestfriend
        user['tweet_sentiment'] = tweetSentiment
        user['liked_sentiment'] = likedSentiment
        user['amount_analyzed'] = liked+count
        user['liked'] = liked
        user['posts'] = count

        # This divides most populat tweet into useable components
        if 'https://t.co' in popular_tweet[0].text:
            index = popular_tweet[0].text.index('https://t.co')
            if "media" in popular_tweet[0].entities:
                popular_tweet = [popular_tweet[0].text[0:index],
                                 popular_tweet[0].entities['media'][0]['media_url']]
                # print('\n\nmedia:', tweet.entities['media'])
            else:
                popular_tweet = [popular_tweet[0].text[0:index], '']
        else:
            popular_tweet = [popular_tweet[0].text[0:index], '']

        user['popular_tweet'] = popular_tweet

        return user


API_KEY = 'v9gW9WQIOg50ItkObmNT6fLxK'
API_SECRET_KEY = 'kUd69URMSmqJhdC2JiDpLKQYvesT0XYEzpYj8LwWaaePz5gCET'

ACCESS_TOKEN = '1088520435656847360-Xah4d3GEOCSjbHvVItuKJRqsy0yzNN'
ACCESS_TOKEN_SECRET = 'pglDWUnuQbizA888laZh4kZTPVDDwSFpa1RTs28ISBjmN'

#hello = TwitterApi(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# hello.wrapped('sleeping_drums')
# hello.searchSediment('corona')
