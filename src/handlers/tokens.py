# -*- coding: utf-8 -*-


# Global list of all token secrets
TOKEN_SECRETS = {}




def build_key(account, token):

	""" Builds a hash key given a Twitter account and token

	:param account: (str) Twitter account
	:param token: (str) Twitter token

	:return: (str)
	"""

	return account + "_" + token




def set_token_secret(account, token, secret):

	""" Saves a token secret given a pair account-token

	:param account: (str) Twitter account
	:param token: (str) Twitter token
	:param secret: (str) Twitter secret
	"""

	key = build_key(account, token)
	TOKEN_SECRETS[key] = secret




def get_token_secret(account, token):

	""" Retrieves a token secret given a pair account-token

	:param account: (str) Twitter account
	:param token: (str) Twitter token

	:return: (str)
	"""

	key = build_key(account, token)
	return TOKEN_SECRETS.get(key)
