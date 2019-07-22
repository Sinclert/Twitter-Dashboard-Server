# -*- coding: utf-8 -*-

import numpy
import random
import requests
from config import KEYS
from typing import Union


fuzz_margin = 0.02




def compute_center(points: list) -> list:

	"""
	Computes the center from a list of point coordinates

	:param points: list of points (lon, lat)
	"""

	polygon = numpy.array(points)

	length = polygon.shape[0]
	sum_lon = numpy.sum(polygon[:, 0])
	sum_lat = numpy.sum(polygon[:, 1])

	return [sum_lon / length, sum_lat / length]




def fuzz_point(coords: list) -> list:

	"""
	Fuzzes a place center location in order to avoid overlapping

	:param coords: point (lon, lat)
	"""

	lon_fuzz = random.random() * 2 * fuzz_margin
	lat_fuzz = random.random() * 2 * fuzz_margin

	new_lon = coords[0] + lon_fuzz - fuzz_margin
	new_lat = coords[1] + lat_fuzz - fuzz_margin

	return [new_lon, new_lat]




def region_to_coords(region: str) -> Union[list, None]:

	"""
	Obtains the region coordinates from the geocoding API response

	:param region: natural language region description
	"""


	# Obtaining basic data to perform the request
	geocoding_key = KEYS['geocoding_key']
	geocoding_url = KEYS['geocoding_url']
	geocoding_params = {"address": region, "key": geocoding_key}

	# Performing the request to Google geocoding API
	response = requests.get(url = geocoding_url, params = geocoding_params)
	response = response.json()

	# In case of being valid: get the coordinates
	if response['status'] == 'OK':

		# Get the coordinates of the specified region
		geometry = response['results'][0]['geometry']['viewport']
		return [
			geometry['southwest']['lng'],
		    geometry['southwest']['lat'],
		    geometry['northeast']['lng'],
		    geometry['northeast']['lat']
		]

	# In case of not being valid
	else:
		return None
