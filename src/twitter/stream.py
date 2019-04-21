# -*- coding: utf-8 -*-

from tweepy import API
from tweepy import StreamListener
from tweepy import Stream

from twitter.auth import get_oauth_handler




class TwitterStream(StreamListener):

	""" Represents a Twitter Streaming object """




	def __init__(self, token_key: str, token_secret: str) -> None:

		""" Creates a Twitter listener object

		:param token_key: Twitter token
		:param token_secret: Twitter token secret

		"""

		super().__init__()

		oauth_handler = get_oauth_handler()
		oauth_handler.set_access_token(token_key, token_secret)

		self.api = API(oauth_handler)
		self.stream = None

		# Timeout before closing (secs)
		self.timeout = 15




	@staticmethod
	def get_text(tweet: object) -> str:

		""" Extracts the lowercase text from a Status object (tweet)

		:param tweet: Tweet object

		"""

		if hasattr(tweet, 'retweeted_status'):
			tweet = tweet.retweeted_status

		if hasattr(tweet, 'extended_tweet'):
			tweet = tweet.extended_tweet
			return tweet['full_text'].lower()

		else:
			return tweet.text.lower()




	def start_stream(self, queries: list, langs: list, coords: list) -> None:

		""" Starts the Twitter stream

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
			timeout = self.timeout
		)

		self.stream.filter(
			track = queries,
			languages = langs,
			locations = coords,
			is_async = True
		)




	def finish_stream(self) -> None:

		""" Closes the Twitter stream """

		self.stream.disconnect()
		print('Disconnected from the Twitter stream')




	def on_status(self, tweet: object) -> None:

		""" Process received tweet

		:param tweet: Tweet object

		"""

		tweet_text = self.get_text(tweet)
		print(tweet_text)




	def on_exception(self, exception: Exception) -> None:

		""" Finish stream due to the timeout exception """

		print('Timeout exception due to lack of data')
		self.finish_stream()




	def on_error(self, code: int) -> None:

		""" Error listener which prints error code

		:param code: Stream error code

		"""

		exit('Twitter stream error: ' + str(code))
