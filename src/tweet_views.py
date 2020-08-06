from app import app, mongo
from src.tweet import *
from src.config import *
from src.util import *
from src.models import *


@app.route('/twitteranalysis/', methods=['POST', 'GET'])
def viewTweets():
    isloggedin = 'email' in session
    if request.method == 'POST':
        # True if logged in, false if not
        print('finding tweets')
        tweepy = TwitterApi(API_KEY, API_SECRET_KEY,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        query = request.form.get("query")
        print('query:', query)
        if(query == "Sentiment"):
            approval = tweepy.searchSediment(request.form.get('input'))
            result = ' has a '+str(approval) + '% twitter approval rating'
            return render_template('mytweets.html', topic=request.form.get('input'), loggedin=isloggedin, answer=result, selectValue=3)
        elif(query == 'All'):
            count = request.form.get('count')
            tweets = tweepy.getTweets(request.form.get('input'), count=count)
            return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'),  tweets=tweets, count=count, all=True, selectValue=1)
        elif(query == 'Wrapped'):
            userdict = tweepy.wrapped(request.form.get('input'))
            if userdict == None:
                return render_template('mytweets.html', loggedin=isloggedin, answer='Does not Exists', selectValue=2)
            renderImage = True
            if userdict['popular_tweet'][1] == '':
                renderImage = False
            return render_template('mytweets.html', loggedin=isloggedin, username=request.form.get('input'), name=userdict['name'],  wrapped=True, profile_img=userdict['profile_img'],
                                   description=userdict['description'], followers=userdict['followers'], friends=userdict['friends'],
                                   date=userdict['created_at'].strftime("%B %d, %Y"), popular_text=userdict['popular_tweet'][0],
                                   popular_img=userdict['popular_tweet'][1], tweet_sentiment=userdict[
                                       'tweet_sentiment'], liked_sentiment=userdict['liked_sentiment'],
                                   bestfriend=userdict['bestfriend'], pop_likes=userdict['pop_likes'], pop_retweets=userdict[
                                       'pop_retweets'], renderImage=renderImage, selectValue=2,
                                   graph=userdict['graph'], sentiment=userdict['sentiment'])
        elif(query == 'Graph'):
            print("GRAPHING")
            # Politician.updateGraph()
            return render_template('mytweets.html', loggedin=isloggedin, graph=Politician.graph_politicians(), graphing=True, selectValue=4)
        elif(query == 'Politics'):
            print("GRAPHING")
            # Politician.updateGraph()
            return render_template('mytweets.html', loggedin=isloggedin, graph=Politician.graph_politicians(), graphing=True, selectValue=4)
        # return render_template('tweet.html', answer=approval)   datetime.strptime(userdict['created_at'], "%M %d, %Y")
    return render_template('mytweets.html', loggedin=isloggedin, selectValue=0)
