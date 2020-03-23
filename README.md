#Flask App
Jake Armendariz

### Overview
I switched my personal website over to flask. I added the ability to create users, with secure login, signup, password hashing and sessions. I used MongoDB to store users and their information. 

### app.py
Runs the app main file, connects to the mongo database

### config.py
Omitted from git, but signs into email.

### models.py
User class, login, signup
Score class, handles the scores of the light speed game inside the app
Politician class, used for the Twitter API, updated twice a day with sentiment ratings and dates

### util.py
Hash and verify passwords

### views.py
Handles most of the application. Such as mailing through my contact form, or handling the different post requests inside of tweet.html or login/signup. It handles every post and get request on the site

### tweet.py
A Twitter class that does searches twitter assessing sentiment using textBlob. Can print and return up to 200 tweets from any user. A wrapped version of each twitter, with a best friend calculator based on their likes, retweets, etc, and a graph of their like distribution over time. Finally, a daily political check and graphing. So it can record and display twitter sentiment of popular political figures over time. All operations handled in /twitteranalysis

## Run
Create a config.py file, add a an email password, twitterAPI credentials, and a secret key for hashing, then...
! Flask run

I think this could work as a basic backend template for flask if you delete tweet.py, its very basic backend.

