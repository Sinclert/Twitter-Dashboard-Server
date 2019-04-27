# -*- coding: utf-8 -*-

from tweepy import API
from tweepy import StreamListener
from tweepy import Stream

from twitter.auth import get_oauth_handler
from twitter.tweet import SimpleTweet




class TwitterStream(StreamListener):

	""" Represents a Twitter Streaming object """


	def __init__(self, token: str, token_secret: str, callback: callable) -> None:

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
		self.stream_timeout = 15

		# On status (tweet) listener functions
		self.tweet_builder = SimpleTweet
		self.tweet_callback = callback




	def start_stream(self, queries: list, langs: list, coords: list) -> None:

		"""
		Starts the Twitter stream

		:param queries: filter words
		:param langs: filter languages
		:param coords: filter coordinates in groups of 4
			1. South-West longitude
			2. South-West latitude
			3. North-East longitude
			4. North-East latitude
		"""

		self.stream = Stream(
			auth = self.api.auth,
			listener = self,
			timeout = self.stream_timeout
		)

		self.stream.filter(
			track = queries,
			languages = langs,
			locations = coords,
			is_async = True
		)




	def stop_stream(self) -> None:

		""" Closes the Twitter stream """

		self.stream.disconnect()
		print('Disconnected from the Twitter stream')




	def on_status(self, tweet: object) -> None:

		"""
		Processes received tweet and executes callback

		:param tweet: Tweet object
		"""

		tweet = self.tweet_builder(tweet)
		tweet = tweet.serialize()

		self.tweet_callback(tweet)




	def on_exception(self, exception: Exception) -> None:

		""" Finish stream due to the timeout exception """

		print('Timeout exception due to lack of data')
		self.stop_stream()




	def on_error(self, code: int) -> None:

		"""
		Error listener which prints error code

		:param code: Stream error code
		"""

		exit('Twitter stream error: ' + str(code))
