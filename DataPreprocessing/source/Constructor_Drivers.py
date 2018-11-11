from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt
import numpy as np
import copy

def getRaceDriverConstRankPts(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	dict{key:[list]}
		[raceID, driverID, constructorID, rank, points]

	"""
	cons_Data = getDataset(filepath)
	dataObtained = cons_Data.next()
	print "Data Extracted: " + str(dataObtained)
	return cons_Data

def getYearRaceID(filepath):
	"""
	Parameters
	----------
	filepath: string
		The directory to the file relative to the parentPath

	Returns
	-------
	dictionary of list
		{year: [raceID]}

	"""
	YearRace_Data = getDataset(filepath)
	dataObtained = YearRace_Data.next()
	print "Data from file: " + str(dataObtained)
	print "Data Extracted: " + 'Year ' + " raceID"
	yearDict_raceList = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	for race_year in YearRace_Data:
		# print race_circuit
		yearDict_raceList[race_year[1]].append(race_year[0]) # {circuitID: [raceID]}
	return yearDict_raceList

def _getYearFromRaceID(raceID, yearDict_raceList, keys_yr):
	# print "keys_yr"
	# print keys_yr
	# print "search for raceID: " + raceID

	for key_yr in keys_yr:
		if(raceID in yearDict_raceList[key_yr]):
			# print "year"
			# print key_yr
			# print yearDict_raceList[key_yr]
			return key_yr

def getConsDrivers(dataset):
	yearDict_raceList = getYearRaceID("races.csv")
	keys_yr = yearDict_raceList.keys()
	ret_dict = defaultdict(lambda:[])
	for data in dataset:
		# if( int(_getYearFromRaceID(data[0], yearDict_raceList, keys_yr)) < 1980):
		ret_dict[data[2]].append(data[1])
	keys_cd = sorted(ret_dict.keys(), key=lambda d: len(ret_dict[d]))
	print "length(keys_cd)"
	print len(keys_cd)
	print "number of drivers"
	for key_cd in keys_cd:
		print len(ret_dict[key_cd])
	return ret_dict

if __name__ == '__main__':
	dataset = getRaceDriverConstRankPts("results.csv")
	dict_ = getConsDrivers(dataset)
