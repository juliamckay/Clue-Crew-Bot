import codecs
import tweepy
import time
import random
import json
from os import environ
#import config

import config


def create_api(consumer_key, consumer_secret_key, access_token, access_token_secret):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def get_random_tweet(tweets):
    random_tweet = random.choice(tweets)
    return random_tweet

def create_tweet(tweets, api):
    #choose random tweet
    tweet = get_random_tweet(tweets)

    #post tweet
    message = ''
    if "status" in tweet:
        message = tweet["status"]
    api.update_status(status=message)


if __name__ == "__main__":
    consumer_key = environ['CONSUMER_KEY']
    consumer_secret_key = environ['CONSUMER_SECRET']
    access_token = environ['ACCESS_KEY']
    access_token_secret = environ['ACCESS_SECRET']

    #consumer_key = config.api_key
    #consumer_secret_key = config.api_secret
    #access_token = config.access_token
    #access_token_secret = config.access_secret

    api = create_api(consumer_key, consumer_secret_key, access_token, access_token_secret)
    tweet_file = 'tweets.json'

    with open(tweet_file, 'r') as f:
        tweets = json.load(f)

    # Tweet quote
    tweet_created = False
    while not tweet_created:
        #try to create tweet, expect duplicate tweet error and pass if raised
        try:
            create_tweet(tweets, api)
            tweet_created = True
        except tweepy.TweepError as error:
            if error.api_code == 187:
                print("duplicate message error")
            else:
                raise error

