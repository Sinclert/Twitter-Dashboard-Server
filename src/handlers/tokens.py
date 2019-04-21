# -*- coding: utf-8 -*-


# Global list of all token secrets
TOKEN_SECRETS = {}




def build_key(account: str, token: str) -> str:

	""" Builds a hash key given a Twitter account and token

	:param account: Twitter account
	:param token: Twitter token

	"""

	return account + "_" + token




def set_token_secret(account: str, token: str, secret: str) -> None:

	""" Saves a token secret given a pair account-token

	:param account: Twitter account
	:param token: Twitter token
	:param secret: Twitter token secret

	"""

	key = build_key(account, token)
	TOKEN_SECRETS[key] = secret




def get_token_secret(account: str, token: str) -> str:

	""" Retrieves a token secret given a pair account-token

	:param account: Twitter account
	:param token: Twitter token

	"""

	key = build_key(account, token)
	return TOKEN_SECRETS.get(key)
