# -*- coding: utf-8 -*-


from collections import Counter

from tweepy import API
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
from tweepy import TweepError

from twitter.credentials import *

from utils import clean_text




class TwitterListener(StreamListener):

	""" Represents a Twitter Streaming listener

	Attributes:
	----------
		API:
			type: tweepy.API
			info: object used to make connection with Twitter

		stream:
			type: tweepy.Stream
			info: Twitter stream end point

		buffer:
			type: list
			info: circular buffer containing the latest predictions

		index:
			type: int
			info: buffer index to the next position to be replaced

		clf:
			type: HierarchicalClassif
			info: hierarchical classifier to predict labels

		counters
			type: dict
			info: label counters
	"""




	def __init__(self, token_key: str, token_secret: str, buffer_size: int, clf):

		""" Creates a Twitter listener object

		Arguments:
		----------
			token_key: identifies the user
			token_secret: accompanies the token key
			buffer_size: size of the label circular buffer
			clf: HierarchicalClassif object used to predict labels

		"""

		super().__init__()

		try:
			consumer_key = APP_KEYS['consumer_key']
			consumer_secret = APP_KEYS['consumer_secret']

			auth = OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(token_key, token_secret)

			self.API = API(auth)

		except TweepError:
			exit('Unable to create the tweepy API object')

		self.stream = None
		self.buffer = [None] * buffer_size
		self.index = 0
		self.clf = clf
		self.counters = Counter()




	def __update_buffer(self, label: str):

		""" Replace the self.index position by the specified label

		Arguments:
		----------
			label: replaces the one in self.index position

		"""

		try:
			self.counters[self.buffer[self.index]] -= 1
		except KeyError:
			pass

		self.buffer[self.index] = label
		self.index = (self.index + 1) % len(self.buffer)
		self.counters[label] += 1




	@staticmethod
	def get_text(tweet) -> str:

		""" Extracts the text from a Status object (tweet)

		Arguments:
		----------
			tweet: Status object containing all the attributes of a tweet

		Returns:
		----------
			text: lowercase tweet text

		"""

		if hasattr(tweet, 'retweeted_status'):
			tweet = tweet.retweeted_status

		if hasattr(tweet, 'extended_tweet'):
			tweet = tweet.extended_tweet
			return tweet['full_text'].lower()

		else:
			return tweet.text.lower()




	def start_stream(self, queries: list, langs: list, coords: list, timeout: int = 15):

		""" Starts the Twitter stream

		Arguments:
		----------
			queries: words to filter
			langs: language codes to filter

			coords: groups of 4 coordinates to filter, where:
				1. South-West longitude
				2. South-West latitude
				3. North-East longitude
				4. North-East latitude

			timeout: seconds to launch an exception (optional)

		"""

		self.stream = Stream(
			auth = self.API.auth,
			listener = self,
			timeout = timeout
		)

		self.stream.filter(
			track = queries,
			languages = langs,
			locations = coords,
			is_async = True
		)




	def finish_stream(self):

		""" Closes the Twitter stream """

		self.stream.disconnect()
		print('Disconnected from the Twitter stream')




	def on_status(self, tweet):

		""" Process received tweet

		Arguments:
		----------
			tweet: Status object containing all the fields of a tweet

		"""

		tweet_text = self.get_text(tweet)
		tweet_text = clean_text(tweet_text)

		label = self.clf.predict(tweet_text)

		if label is not None:
			self.__update_buffer(label)




	def on_exception(self, exception: Exception):

		""" Finish stream due to the timeout exception """

		print('Timeout exception due to lack of data')
		self.finish_stream()




	def on_error(self, code: int):

		""" Prints error code

		Arguments:
		----------
			code: stream error code

		"""

		exit('Twitter stream error: ' + str(code))
