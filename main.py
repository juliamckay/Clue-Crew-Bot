import codecs

import tweepy
import config
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.api_key,
    config.api_secret)
auth.set_access_token(config.access_token,
    config.access_secret)

#Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Read quote list
filename = open('clue_crew_quotes.txt', 'r')
quote_list = filename.read().split(';')
filename.close()

try:
    #api.update_status("Yet Another\nTest Tweet")
    for quote in quote_list[0:4]:
        quote.lstrip()
        api.update_status(quote)
        print(quote)
        time.sleep(10)
    print("Tweet Successful")
except:
    print("Error during tweeting process")