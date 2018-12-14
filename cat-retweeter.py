import tweepy
from os import environ
from datetime import datetime, date, timedelta
import pandas as pd

# Setup tweepy authorization
auth = tweepy.OAuthHandler(environ['consumer_key'], environ['consumer_secret'])
auth.set_access_token(environ['access_token'], environ['access_token_secret'])
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Get dates
today = date.today()
yesterday = today - timedelta(1)
print("Yesterday:", str(yesterday))

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

print("Query:", query)

# Get tweets posted since yesterday (i.e. today) for query
# Get 200 just to be safe
tweets = tweepy.Cursor(
    api.search,
    q=query,
    count='200',
    since=str(yesterday),
    lang='en'
).items()

# Retweet first tweet with attached media
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
