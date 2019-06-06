# -*- coding: utf-8 -*-

import re
from tweepy import API
from tweepy import StreamListener
from tweepy import Stream
from twitter.auth import get_oauth_handler
from twitter.tweet import SimpleTweet




class TwitterStream(StreamListener):

	""" Represents a Twitter Streaming object """


	def __init__(self, token: str, token_secret: str, callback: callable):

		"""
		Creates a Twitter listener object

		:param token: Twitter token
		:param token_secret: Twitter token secret
		:param callback: callback when a tweet is received
		"""

		super().__init__()

		oauth_handler = get_oauth_handler()
		oauth_handler.set_access_token(token, token_secret)

		self.api = API(oauth_handler)

		# Stream properties
		self.stream = None
		self.stream_filter = None
		self.stream_timeout = 30

		# On status (tweet) listener functions
		self.tweet_builder = SimpleTweet
		self.tweet_callback = callback




	def __filter(self, tweet: SimpleTweet):

		"""
		Filters the tweet if it does not contain the filter term

		:param tweet: Tweet object
		"""

		if re.search(self.stream_filter, tweet.text) is not None:
			return tweet
		else:
			return None




	def start(self, filter_term: str, filter_langs: tuple, filter_coords: tuple):

		"""
		Starts the Twitter stream

		:param filter_term: filter word
		:param filter_langs: filter languages
		:param filter_coords: filter coordinates in groups of 4
			1. South-West longitude
			2. South-West latitude
			3. North-East longitude
			4. North-East latitude
		"""

		# The stream filter term must be set first
		self.stream_filter = '(^|\s)' + filter_term + '(\s|$)'

		self.stream = Stream(
			auth = self.api.auth,
			listener = self,
			timeout = self.stream_timeout
		)

		self.stream.filter(
			languages = filter_langs,
			locations = filter_coords,
			is_async = True
		)




	def stop(self):

		""" Closes the Twitter stream """

		self.stream.disconnect()
		print('Disconnected from the Twitter stream')




	def on_status(self, tweet: object):

		"""
		Processes received tweet and executes callback

		:param tweet: Tweet object
		"""

		tweet = self.tweet_builder(tweet)
		tweet = self.__filter(tweet)

		if type(tweet) == SimpleTweet:
			tweet = tweet.serialize()
			self.tweet_callback(tweet)




	def on_exception(self, exception: Exception):

		""" Finish stream due to the timeout exception """

		print('Timeout exception due to lack of data')
		self.stop()




	def on_error(self, code: int):

		"""
		Error listener which prints error code

		:param code: Stream error code
		"""

		exit('Twitter stream error: ' + str(code))
