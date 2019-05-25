# -*- coding: utf-8 -*-

from twitter.stream import TwitterStream
from utils.singleton import Singleton




class StreamsHandler(metaclass=Singleton):

	""" Represents a streams handler object """


	def __init__(self):

		""" Creates a streams handler singleton """

		self.streams = {}




	@staticmethod
	def build_key(account: str) -> str:

		"""
		Builds a hash key given a Twitter account

		:param account: Twitter account
		"""

		return account




	def get(self, account: str) -> TwitterStream:

		"""
		Retrieves a Twitter stream given an account

		:param account: Twitter account
		"""

		key = self.build_key(account)
		return self.streams.get(key)




	def set(self, account: str, stream: object) -> None:

		"""
		Saves a Twitter stream given an account

		:param account: Twitter account
		:param stream: Twitter stream object
		"""

		key = self.build_key(account)
		self.streams[key] = stream




	def start_stream(self, account: str, stream: TwitterStream) -> None:

		"""
		Starts a Twitter stream given an account

		:param account: Twitter account
		:param stream: Twitter stream object
		"""

		# Stopping previous stream in case it existed
		self.stop_stream(account)

		self.set(account, stream)
		stream.start(
			langs=['en'],
			coords=[-122.75, 36.8, -121.75, 37.8]
		)




	def stop_stream(self, account: str) -> None:

		"""
		Stops a Twitter stream given an account

		:param account: Twitter account
		"""

		stream = self.get(account)

		if stream is not None:
			stream.stop()

		self.set(account, None)
