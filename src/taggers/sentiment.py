# -*- coding: utf-8 -*-

import random
from utils.singleton import Singleton


all_labels = (
	'positive',
	'negative',
	'neutral'
)




class SentimentTagger(metaclass=Singleton):

	""" Represents a sentiment classifier object """


	def __init__(self):

		"""
		Loads the necessary classifiers to assign the label
		"""




	@staticmethod
	def predict(text):

		"""
		Predicts a sentiment label given a text

		:param text: comment to predict
		"""

		return random.choice(all_labels)
