# - * - coding: UTF-8 - * -

import tweepy
# Consumer keys and access tokens, used for OAuth
consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXX'
access_token_secret = 'XXXX'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

def numFollowers(usertwitter):
    user = api.get_user(usertwitter)
    return (user.followers_count)

def numFriends(usertwitter):
    user = api.get_user(usertwitter)
    return (user.friends_count)

def location(usertwitter):
    user = api.get_user(usertwitter)
    return (user.location)
