import tweepy
from os import environ
from datetime import date, timedelta

auth = tweepy.OAuthHandler(environ['consumer_key'], environ['consumer_secret'])
auth.set_access_token(environ['access_token'], environ['access_token_secret'])
api = tweepy.API(auth)

yesterday = date.today() - timedelta(1)
print(str(yesterday) + '\n')

tweets = tweepy.Cursor(
    api.search,
    q='#cats #catsoftwitter',
    count='200',
    since=str(yesterday),
    lang='en'
).items()

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
