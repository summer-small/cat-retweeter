import tweepy
from os import environ
from datetime import datetime, date, timedelta

# Setup tweepy authorization
auth = tweepy.OAuthHandler(environ['consumer_key'], environ['consumer_secret'])
auth.set_access_token(environ['access_token'], environ['access_token_secret'])
api = tweepy.API(auth)

# Tweepy authorization for local testing
# Add keys and tokens to credentials.py (already in gitignore)
# Uncomment lines below and comment out standard auth lines to use
# Alternatively, set keys and tokens as environment variables
#from credentials import *
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

# Get date
today = date.today()
print("Today:", str(today))

# Default query
query = "#cats #catsoftwitter"

# Get holiday data
holidays = []
with open('data/holidays.csv', 'r') as file:
    line = file.readline()
    line = file.readline()
    while (line):
        holidays.append(line.rstrip().split(','))
        line = file.readline()

# Get todays date as a string of the same format as the holidays csv
today_str = datetime.strftime(today, '%d/%m')
print(today_str)

# Check if any holidays are today
holiday = None
for day in holidays:
    if day[2] == today_str:
        holiday = day
        break

# If today is a holiday add that hashatag to the query
if (holiday):
    query += ' {}'.format(holiday[1])
    print("Holiday: {}".format(holiday[0]))

# Add filters:
# - Must have media
# - Not a retweet
query += " filter:media -filter:retweets"

print("Query:", query)
print("-"*48)

# Loop until appropriate tweet found
# This loop is unlikely to go more than once, but just in case
cat_found = False
while not cat_found:

    # Get tweets posted today for query
    # Get 200 just to be safe
    tweets = tweepy.Cursor(
        api.search,
        q=query,
        count='100',
        since=str(today),
        lang='en'
    ).items()

    # Retweet first tweet that has not already been retweeted
    for tweet in tweets:
        print("@{}".format(tweet.user.screen_name))
        print(tweet.created_at)
        print(tweet.text)
        print("-"*48)
        try:
            # Retweet
            api.retweet(tweet.id)
            cat_found = True
            break
        except tweepy.TweepError as e:
            print(e.reason, "\n")
    
    # If there are no holiday cat media tweets, change to default query
    if not cat_found:
        query = "#cats #catsoftwitter filter:media -filter:retweets"
        print("New query:", query)
