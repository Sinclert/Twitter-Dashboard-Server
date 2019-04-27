# -*- coding: utf-8 -*-

import numpy




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