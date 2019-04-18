# -*- coding: utf-8 -*-

from tweepy import OAuthHandler
from twitter.secrets import app_keys




def get_oauth_handler():
	return OAuthHandler(
		consumer_key=app_keys['consumer_key'],
		consumer_secret=app_keys['consumer_secret']
	)
