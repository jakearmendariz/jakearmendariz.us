import tweepy
from config import *
import re
from textblob import TextBlob
import time
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
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
        #print('total tweets:', len(public_tweets))
        average = 0
        for tweet in public_tweets:
            text = ' '.join(re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
            average += self.binaryClassifier(TextBlob(text).sentiment.polarity)
            # average += (TextBlob(text).sentiment.polarity)
            #print(text, TextBlob(text).sentiment.polarity)

        average = average/len(public_tweets)
        average *= 100
        # print('\n', average, '% approval rating')
        return round(average)

    # Hand in a username, and a word if you want to search for tweets with said word
    def getTweets(self, username, word='', count=20):
        try:
            user = self.api.get_user(username)
        except:
            print("User does not exist")
            return None
        try:
            tweets = self.api.user_timeline(
                screen_name=username, count=count, include_rts=True, tweet_mode='extended')
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
            # print(tweet)
            try:
                # print(tweet.extended_tweet)
                text = tweet.extended_tweet["full_text"]
                print('Full Tweet')
            except AttributeError:
                text = tweet.full_text
            print(text)
            if 'https://t.co' in text:
                index = text.index('https://t.co')
                if "media" in tweet.entities:
                    feed.append(
                        (text[0:index], tweet.entities['media'][0]['media_url']))
                    # print('\n\nmedia:', tweet.entities['media'])
                else:
                    feed.append(
                        (text[0:index], ''))
            else:
                feed.append(
                    (text, ''))
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
        url = user.profile_image_url_https
        url = url.replace('_normal', '')
        userdict['profile_img'] = url
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
        for favorite in tweepy.Cursor(self.api.favorites, id=username).items(1):
            if str(favorite.user.screen_name) in friends:
                friends[str(favorite.user.screen_name)] += 1
            else:
                friends[str(favorite.user.screen_name)] = 1
            count += 1
            likedSentiment += TextBlob(favorite.text).sentiment.polarity

        if(count > 0):
            likedSentiment /= count
        else:
            likedSentiment = 0
        liked = count
        count = 0
        # PULLS REGULAR TWEETS
        popular_tweet = [None, -1]
        try:
            tweets = self.api.user_timeline(
                screen_name=username, count=1, include_rts=True)
        except:
            print("did not pull tweets")
            return
        # CHECK REPLIES-- SEE WHO LIKED IT
        size = len(tweets)
        print('number of tweets:', size)
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
                compare = int(tweet.favorite_count) + \
                    int(tweet.retweet_count)*2
                # print('compare', compare, ',', popular_tweet[1])
                if compare > int(popular_tweet[1]):
                    popular_tweet[0] = tweet
                    popular_tweet[1] = compare
        like_arr = []
        date_arr = []
        count = 0
        for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=username, tweet_mode="extended", include_rts=False).items(500):
            count += 1
            # print(tweet.full_text)
            date_arr.append(tweet.created_at.strftime("%B %d, %Y"))
            like_arr.append(tweet.favorite_count)
            tweetSentiment += TextBlob(tweet.full_text).sentiment.polarity
            compare = int(tweet.favorite_count) + \
                int(tweet.retweet_count)*2
            # print('compare', compare, ',', popular_tweet[1])
            if compare > int(popular_tweet[1]):
                popular_tweet[0] = tweet
                popular_tweet[1] = compare

            #print(tweet.created_at.strftime("%B %d, %Y"), tweet.text)
        print('\n\nNumber of Tweets', count)

        if(count > 0):
            tweetSentiment /= count
        else:
            tweetSentiment = 0
        # Gets the maximum key value
        friends[username] = 0
        bestfriend = max(friends, key=friends.get)
        # print(friends)
        print('\n\nbest friend is', bestfriend, 'value', max)
        user = {}
        user['bestfriend'] = bestfriend
        user['tweet_sentiment'] = round(((tweetSentiment+1)/2)*100)
        user['liked_sentiment'] = round(((likedSentiment+1)/2)*100)
        
        user['sentiment'] = TwitterApi.sentiment_to_string(user['tweet_sentiment'])
        
        user['amount_analyzed'] = liked+count
        user['liked'] = liked
        user['posts'] = count
        if popular_tweet[0] != None:
            user['pop_likes'] = popular_tweet[0].favorite_count
            user['pop_retweets'] = popular_tweet[0].retweet_count
        else:
            user['pop_likes'] = 0
            user['pop_retweets'] = 0
        # This is for creating the graph
        size = len(date_arr)
        dates = np.array([date_arr[size-index-1] for index in range(size)])
        likes = np.array([like_arr[size-index-1] for index in range(size)])

        line = pd.Series(data=likes, index=dates)
        user['graph'] = self.graph_like_distribution(line)
        #user['graph'] = self.scatter_plot(dates, likes)

        # This divides most populat tweet into useable components
        if popular_tweet[0] != None:
            try:
                text = popular_tweet[0].full_text
            except:
                text = popular_tweet[0].text
            if 'https://t.co' in text:
                index = text.index('https://t.co')
                if "media" in popular_tweet[0].entities:
                    popular_tweet = [text[0:index],
                                     popular_tweet[0].entities['media'][0]['media_url']]
                    # print('\n\nmedia:', tweet.entities['media'])
                else:
                    popular_tweet = [text[0:index], '']
            else:
                popular_tweet = [text[0:index], '']

            user['popular_tweet'] = popular_tweet
        else:
            user['popular_tweet'] = [None, '']
        print("\n\nretuning user with ", user)
        return user

    def a(self):
        user = self.api.get_user('realDonaldTrump')
        print(
            user.created_at.strftime("%B %d, %Y"))
        return

    def graph_like_distribution(self, line):
        plt.switch_backend('Agg')
        fig = plt.figure(figsize=(8, 4))
        line.plot(linewidth=2.5)
        plt.ylabel('likes')
        plt.xlabel('dates')
        plt.title('Like Distribution over time')
        return mpld3.fig_to_html(fig)

    def scatter_plot(self, xaxis, yaxis):
        plt.switch_backend('Agg')
        fig = plt.figure(figsize=(8, 4))
        df = pd.DataFrame({'dates': xaxis, 'likes': yaxis})
        df.plot('dates', 'likes',
                kind='scatter', title='Like Distribution over time')
        return mpld3.fig_to_html(fig)
    
    @staticmethod
    def sentiment_to_string(rating):
        if rating > 80:
            return 'very positive'
        elif rating > 60:
            return 'positive '
        elif rating > 40:
            return 'neutral'
        elif rating > 20:
            return 'negative'
        else:
            return 'very negative'

API_KEY = 'v9gW9WQIOg50ItkObmNT6fLxK'
API_SECRET_KEY = 'kUd69URMSmqJhdC2JiDpLKQYvesT0XYEzpYj8LwWaaePz5gCET'

ACCESS_TOKEN = '1088520435656847360-Xah4d3GEOCSjbHvVItuKJRqsy0yzNN'
ACCESS_TOKEN_SECRET = 'pglDWUnuQbizA888laZh4kZTPVDDwSFpa1RTs28ISBjmN'


# hello = TwitterApi(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# user = hello.a()
# hello.wrapped('sleeping_drums')
