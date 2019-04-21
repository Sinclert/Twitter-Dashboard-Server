# -*- coding: utf-8 -*-

from utils.singleton import Singleton




class SecretsHandler(metaclass=Singleton):

	""" Represents a token secrets handler object """


	def __init__(self):

		""" Creates a token secrets handler singleton """

		self.token_secrets = {}




	@staticmethod
	def build_key(*unique_keys) -> str:

		""" Builds a hash key given a Twitter account and token

		:param unique_keys: individual keys to build a combined key

		"""

		combined_key = '_'.join(unique_keys)
		return combined_key




	def set(self, account: str, token: str, secret: str) -> None:

		""" Saves a token secret given a pair account-token

		:param account: Twitter account
		:param token: Twitter token
		:param secret: Twitter token secret

		"""

		key = self.build_key(account, token)
		self.token_secrets[key] = secret




	def get(self, account: str, token: str) -> str:

		""" Retrieves a token secret given a pair account-token

		:param account: Twitter account
		:param token: Twitter token

		"""

		key = self.build_key(account, token)
		return self.token_secrets.get(key)
