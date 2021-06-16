import codecs
import tweepy
import time
import random
import json
from os import environ

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

def create_tweet(tweets, tweeted_quotes, api):
    #choose random tweet, check that it has not been tweeted yet
    while True:
        tweet = get_random_tweet(tweets)
        if not tweet in tweeted_quotes:
            break
    #post tweet
    message = ''
    media_list = []
    if "status" in tweet:
        message = tweet["status"]
    if "image" in tweet:
        filename = "images/" + tweet["image"]
        image = api.media_upload(filename)
        media_list.append(image.media_id)
    api.update_status(status=message, media_ids=media_list)
    #add to already tweeted
    tweeted_quotes.append(tweet)


if __name__ == "__main__":
    consumer_key = environ['CONSUMER_KEY']
    consumer_secret_key = environ['CONSUMER_SECRET']
    access_token = environ['ACCESS_KEY']
    access_token_secret = environ['ACCESS_SECRET']
    api = create_api(consumer_key, consumer_secret_key, access_token, access_token_secret)
    tweet_file = 'tweets.json'
    prev_tweets_file = 'prev_tweeted.json'

    with open(tweet_file, 'r') as f:
        tweets = json.load(f)

    with open(prev_tweets_file, 'r') as f:
        previously_tweeted = json.load(f)

    # Tweet quote
    interval = 60 * 60 * 8  # three times a day
    while True:
        # if we've tweeted all the quotes in the list reset
        if len(tweets) == len(previously_tweeted):
            previously_tweeted = []
            #print("reset list")
            with open(prev_tweets_file, 'w') as f:
                json.dump(previously_tweeted, f)
        create_tweet(tweets, previously_tweeted, api)
        #update previously tweeted file
        with open(prev_tweets_file, 'w') as f:
            json.dump(previously_tweeted, f)
        print(previously_tweeted)
        time.sleep(interval)
