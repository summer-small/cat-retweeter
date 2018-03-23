import tweepy
from credentials import *
from time import sleep
from datetime import date, timedelta

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

yesterday = date.today() - timedelta(1)
print(str(yesterday))

tweets = tweepy.Cursor(api.search,
                        q='#cats #catsoftwitter',
                        count='200',
                        since=str(yesterday),
                        lang='en').items()
for tweet in tweets:
    print(tweet.user.screen_name)