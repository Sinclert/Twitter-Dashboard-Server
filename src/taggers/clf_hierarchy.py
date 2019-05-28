# -*- coding: utf-8 -*-

from taggers.clf_node import NodeClassif
from typing import Union
from utils.files import read_json




class HierarchicalClassif(object):

	""" Represents a hierarchical classification tree """


	# Required JSON node keys (class attribute)
	keys = ['clf_file', 'clf_object', 'clf_children']




	def __init__(self, cls_folder: str):

		"""
		Loads the JSON profiles models into the tree attribute

		:param cls_folder: folder with all the classifier files
		"""

		self.folder = cls_folder

		profile = read_json(
			f_folder=cls_folder,
			f_type='config',
			f_name='config.json',
		)

		# Checking that the JSON structure is a dict
		assert isinstance(profile, dict)

		try:
			self.tree = profile['tree']
			self.labels = profile['labels']
			self.__load_clf(self.tree)

		except KeyError:
			exit('Invalid JSON keys')




	def __load_clf(self, node: dict):

		"""
		Recursively check and load classifier objects into 'clf_object'

		:param node: current tree node to load its file
		"""

		# Check JSON keys coherence
		assert all(k in node for k in self.keys)

		node['clf_object'] = NodeClassif(self.folder, node['clf_file'])

		try:
			clf_labels = node['clf_object'].get_labels()
			clf_child_names = node['clf_children'].keys()
			clf_child_nodes = node['clf_children'].values()

			# Check that all clf children names are also labels
			assert all(k in clf_labels for k in clf_child_names)

			for child_node in clf_child_nodes:
				self.__load_clf(child_node)

		except AttributeError:
			exit('Invalid JSON values')




	def get_labels(self) -> list:

		""" Gets the label names """

		try:
			return list(self.labels)

		except AttributeError:
			exit('Invalid JSON labels structure')




	def predict(self, sentence: str) -> Union[str, None]:

		"""
		Predicts the label of a sentence using the loaded classifiers

		:param sentence: text to classify
		"""

		node = self.tree
		label = node['clf_object'].predict(sentence)

		while label in node['clf_children'].keys():
			node  = node['clf_children'][label]
			label = node['clf_object'].predict(sentence)

		if label is None:
			print(sentence, '(Unknown label)')

		return label
