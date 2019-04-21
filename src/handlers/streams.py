# -*- coding: utf-8 -*-


# Global list of all Twitter streams
TWITTER_STREAMS = {}




def build_key(account: str) -> str:

	""" Builds a hash key given a Twitter account

	:param account: Twitter account

	"""

	return account




def set_twitter_stream(account: str, stream: object) -> None:

	""" Saves a Twitter stream given a pair account-token

	:param account: Twitter account
	:param stream: Twitter stream object

	"""

	key = build_key(account)
	TWITTER_STREAMS[key] = stream




def get_twitter_stream(account: str) -> object:

	""" Retrieves a Twitter stream given a pair account-token

	:param account: Twitter account

	"""

	key = build_key(account)
	return TWITTER_STREAMS.get(key)
