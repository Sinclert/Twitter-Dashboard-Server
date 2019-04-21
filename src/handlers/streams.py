# -*- coding: utf-8 -*-

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




	def set(self, account: str, stream: object) -> None:

		"""
		Saves a Twitter stream given a pair account-token

		:param account: Twitter account
		:param stream: Twitter stream object
		"""

		key = self.build_key(account)

		# Stopping previous stream in case it existed
		if key in self.streams:
			self.streams[key].stop_stream()

		self.streams[key] = stream




	def get(self, account: str) -> object:

		"""
		Retrieves a Twitter stream given a pair account-token

		:param account: Twitter account
		"""

		key = self.build_key(account)
		return self.streams.get(key)
