# -*- coding: utf-8 -*-

from utils.geolocation import compute_center
from utils.geolocation import fuzz_point


known_sources = (
	'android',
	'iphone',
	'web'
)




class SimpleTweet(object):

	""" Represents a simplification of a Tweet """


	def __init__(self, tweet: object) -> None:

		"""
		Creates a simple Tweet object

		:param tweet: Tweet object
		"""

		self.coords = self.get_coords(tweet)
		self.source = self.get_source(tweet)
		self.text = self.get_text(tweet)




	@staticmethod
	def get_coords(tweet: object) -> dict:

		"""
		Extracts the coordinates from a Status object (tweet)

		:param tweet: Tweet object
		"""

		coords = {'lon': None, 'lat': None}

		if hasattr(tweet, 'coordinates') and type(tweet.coordinates) == dict:
			point = tweet.coordinates.get('coordinates', [None, None])
			coords['lon'] = point[0]
			coords['lat'] = point[1]

		elif hasattr(tweet, 'place') and tweet.place is not None:
			center = compute_center(tweet.place.bounding_box.coordinates[0])
			center = fuzz_point(center)
			coords['lon'] = center[0]
			coords['lat'] = center[1]

		return coords




	@staticmethod
	def get_source(tweet: object) -> str:

		"""
		Extracts the source from a Status object (tweet)

		:param tweet: Tweet object
		"""

		if hasattr(tweet, 'source'):

			for source in known_sources:
				if source in tweet.source.lower():
					return source
			else:
				return 'other'




	@staticmethod
	def get_text(tweet: object) -> str:

		"""
		Extracts the lowercase text from a Status object (tweet)

		:param tweet: Tweet object
		"""

		if hasattr(tweet, 'retweeted_status'):
			tweet = tweet.retweeted_status

		if hasattr(tweet, 'extended_tweet'):
			tweet = tweet.extended_tweet
			return tweet['full_text'].lower()

		else:
			return tweet.text.lower()




	def serialize(self):

		"""
		Returns a dictionary with all the object properties
		"""

		return self.__dict__
