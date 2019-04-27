# -*- coding: utf-8 -*-

import numpy
import random


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