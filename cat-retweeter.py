import tweepy
from os import environ
from datetime import datetime, date, timedelta
import pandas as pd

# Tweepy authorization for local testing
#   Add keys and tokens to credentials.py (already in gitignore)
#   Uncomment lines below and comment out standard auth lines to use
#   Alternatively, set keys and tokens as environment variables
#from credentials import *
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

# Setup tweepy authorization
auth = tweepy.OAuthHandler(environ['consumer_key'], environ['consumer_secret'])
auth.set_access_token(environ['access_token'], environ['access_token_secret'])
api = tweepy.API(auth)

# Get date
today = date.today()
print("Today:", str(today))

# Default query
query = '#cats #catsoftwitter'

# Check for holidays
holidays = pd.read_csv('data/holidays.csv', dtype='str')
today_str = datetime.strftime(today, '%d/%m')
holiday = holidays[holidays['date'] == today_str]

# Append holiday hashtag to query if today is a holiday
if not holiday.empty:
    query =  query + ' ' + holiday['hashtag'].values[0]
    print("Holiday:", holiday['event'].values[0])

print("Query:", query, "\n")

# Get tweets posted today for query
# Get 200 just to be safe
tweets = tweepy.Cursor(
    api.search,
    q=query,
    count='200',
    since=str(today),
    lang='en'
).items()

# Retweet first tweet with attached media
# that has not already been retweeted
for tweet in tweets:
    media = tweet.entities.get('media', [])
    if len(media) > 0:
        print("@{}:".format(tweet.user.screen_name))
        try:
            print(tweet.text)
            print()
            api.retweet(tweet.id)
            break
        except tweepy.TweepError as e:
            print(e.reason)
            print()
