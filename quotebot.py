import codecs
import tweepy
import config
import time
import random
import json
from os import environ

def create_api():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(environ['CONSUMER_KEY'], environ['CONSUMER_SECRET'])
    auth.set_access_token(environ['ACCESS_KEY'], environ['ACCESS_SECRET'])

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
    api = create_api()
    tweet_file = 'tweets.json'
    prev_tweets_file = 'prev_tweeted.json'

    with open(tweet_file, 'r') as f:
        tweets = json.load(f)

    with open(prev_tweets_file, 'r') as f:
        previously_tweeted = json.load(f)

    # Tweet quote
    interval = 60 * 60 * 12  # twice a day
    while True:
        # if we've tweeted all the quotes in the list reset
        if len(tweets) == len(previously_tweeted):
            previously_tweeted = []
            print("reset list")
        create_tweet(tweets, previously_tweeted, api)
        print(previously_tweeted)
        #update previously tweeted file
        with open(prev_tweets_file, 'w') as f:
            json.dump(previously_tweeted, f)
        time.sleep(interval)
