# -*- coding: utf-8 -*-

from typing import Union
from utils.files import load_object




class NodeClassif(object):

	""" Represents a hierarchical node classifier """


	def __init__(self, f_folder: str, f_name: str):

		"""
		Loads a trained model if specified

		:param f_folder: saved model file folder
		:param f_name: saved model file name
		"""

		self.model = None
		self.selector = None
		self.vectorizer = None

		self.__dict__ = load_object(
			f_folder=f_folder,
			f_type='model',
			f_name=f_name
		)




	def get_labels(self) -> list:

		""" Gets the trained label names """

		try:
			return list(self.model.classes_)

		except AttributeError:
			exit('The classifier has not been trained')




	def predict(self, sentence: str) -> Union[str, None]:

		"""
		Predicts the label of the given sentence

		:param sentence: text to classify
		"""

		try:
			feats = self.vectorizer.transform([sentence])
			feats = self.selector.transform(feats)

			# If none of the features give any information
			if feats.getnnz() == 0:
				return None

			return self.model.predict(feats)[0]

		except AttributeError:
			exit('The classifier has not been trained')
