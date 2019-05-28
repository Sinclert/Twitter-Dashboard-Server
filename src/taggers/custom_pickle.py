# -*- coding: utf-8 -*-

import pickle
from taggers.sentiment.custom import TextTokenizer




class CustomUnpickler(pickle.Unpickler):

	""" Represents a custom class unpickler """


	def find_class(self, module, name):

		if name == 'TextTokenizer':
			return TextTokenizer

		return super().find_class(module, name)
