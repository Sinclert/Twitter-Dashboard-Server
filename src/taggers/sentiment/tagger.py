# -*- coding: utf-8 -*-

from taggers.clf_hierarchy import HierarchicalClassif
from utils.singleton import Singleton




class SentimentTagger(metaclass=Singleton):

	""" Represents a sentiment classifier object """


	def __init__(self):

		""" Loads the necessary classifiers to assign the label """

		self.classifier = HierarchicalClassif('sentiment')




	def predict(self, text) -> str:

		"""
		Predicts a sentiment label given a text

		:param text: comment to predict
		"""

		return self.classifier.predict(text)
