from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt, saveLListAsCSV, ifExist
import numpy as np
import copy
from operator import itemgetter

def getDataFromTracks(filepath):
	"""
	Parameters
	----------
	filepath: string
		The directory to the file relative to the parentPath
		# [raceID, driverID, constructorID, rank, points, grid, postion, positionOrder]
	Returns
	-------
	tuple
		(headings, data)

	"""
	TrackData = getDataset(filepath)
	# TrackData.next()
	dataObtained = TrackData.next()
	Data = list(TrackData)
	print "Data from file: " + str(dataObtained)
	# print "Data Extracted: " + 'Year ' + " raceID"
	# yearDict_raceList = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	# dataObtained.append("firstLapChange")
	# for d in Data:
	# 	d.append(int(d[5]) - int(d[7]))
	return (dataObtained, Data)

def getRecentTracks():
	"""
	Returns:
	--------
	list:
		[CircuitIDs]
	"""
	TrackHeadings, TrackData = getDataFromTracks("track_data_final.csv")
	_ret_list = []
	for data in TrackData:
		if ifExist(data[1], _ret_list):
			i = 1 # dummy variable
		else:
			_ret_list.append(data[1])
	return _ret_list

def getRecentTracksName():
	"""
	Returns:
	--------
	dictionary:
		{CircuitID: CircuitName}
	"""
	_ret_dict = defaultdict(lambda:"")
	TrackHeadings, TrackData = getDataFromTracks("track_data_final.csv")
	for data in TrackData:
		_ret_dict[data[1]] = data[0]
	return _ret_dict


if __name__ == '__main__':
	TrackHeadings, TrackData = getDataFromTracks("track_data_final.csv")
	# print TrackData
	# [9:36]

