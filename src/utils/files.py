# -*- coding: utf-8 -*-

import json
import os
import pickle


file_folders = {
	'sentiment': ['taggers', 'sentiment'],
}

file_types = {
	'model': ['models'],
	'config': [],
}




def compute_path(file_folder: str, file_type: str, file_name: str) -> str:

	"""
	Builds the absolute path to the desired file

	:param file_folder: folder where the file types are
	:param file_type: type of the file
	:param file_name: name of the file
	"""

	try:
		project_root = str(os.path.dirname(os.getcwd()))

		path = [project_root]
		path = path + file_folders[file_folder]
		path = path + file_types[file_type]
		path = path + [file_name]

		return os.path.join(*path)

	except KeyError:
		exit('The file type "' + file_type + '" is not defined')




def load_object(file_folder: str, file_type: str, file_name: str) -> dict:

	"""
	Loads an object from the specified file

	:param file_folder: folder where the file types are
	:param file_type: type of the file
	:param file_name: name of the file
	"""

	file_path = compute_path(file_folder, file_type, file_name)

	try:
		file = open(file_path, 'rb')
		obj = pickle.load(file)
		file.close()

		return obj

	except IOError:
		exit('The object could not be loaded from ' + file_path)




def read_json(file_folder: str, file_type: str, file_name: str) -> dict:

	"""
	Reads a JSON file and returns it as a dictionary

	:param file_folder: folder where the file types are
	:param file_type: type of the file
	:param file_name: name of the file
	"""

	file_path = compute_path(file_folder, file_type, file_name)

	try:
		file = open(file_path, 'r', encoding='utf-8')
		json_dict = json.load(file)
		file.close()

		return json_dict

	except IOError:
		exit('The file ' + file_name + ' cannot be opened')
