# -*- coding: utf-8 -*-

import json
import os
import pickle


file_folders = {
	'sentiment': ['src', 'taggers', 'sentiment'],
}

file_types = {
	'model': ['models'],
	'config': [],
}




def compute_path(f_folder: str, f_type: str, f_name: str) -> str:

	"""
	Builds the absolute path to the desired file

	:param f_folder: folder where the file types are
	:param f_type: type of the file
	:param f_name: name of the file
	"""

	try:
		project_root = str(os.path.dirname(os.getcwd()))

		path = [project_root]
		path = path + file_folders[f_folder]
		path = path + file_types[f_type]
		path = path + [f_name]

		return os.path.join(*path)

	except KeyError:
		exit('The file type "' + f_type + '" is not defined')




def load_object(f_folder: str, f_type: str, f_name: str) -> dict:

	"""
	Loads a serialized object from the specified file

	:param f_folder: folder where the file types are
	:param f_type: type of the file
	:param f_name: name of the file
	"""

	path = compute_path(f_folder, f_type, f_name)

	try:
		file = open(path, 'rb')
		obj = pickle.load(file)
		file.close()

		return obj

	except IOError:
		exit('The object could not be loaded from ' + path)




def read_json(f_folder: str, f_type: str, f_name: str) -> dict:

	"""
	Reads a JSON file and returns it as a dictionary

	:param f_folder: folder where the file types are
	:param f_type: type of the file
	:param f_name: name of the file
	"""

	path = compute_path(f_folder, f_type, f_name)

	try:
		file = open(path, 'r', encoding='utf-8')
		json_dict = json.load(file)
		file.close()

		return json_dict

	except IOError:
		exit('The file ' + f_name + ' cannot be opened')
