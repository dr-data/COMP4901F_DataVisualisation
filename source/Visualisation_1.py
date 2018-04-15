from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt, saveLListAsCSV
import numpy as np
import copy

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

def convertRaceToYear(targetDict, yearDict_raceList, freqOut = False):
	"""
	Note
	----
	When freqOut is False, targetDict must be {circuitID: [raceID]}
			  else  True, targetDict must be {consID: [raceID]}
	Parameters
	----------
	targetDict : dict
		targeDict can be {consID: [raceID]} or {circuitID: [raceID]} or
	yearDict_raceList: dict
		{year: dict}
	freqOut: dict of dict of list
		False: {circuitID:[year]}
		True: {consID: {year: frequency}}
	Returns
	-------
	freqOut == False 
		{circuitID: [year]} or {consID: [year]} or {driverID:[year]}
	freqOut == True 
		{consID: {year:frequency}}

	"""
	keys_t = sorted(targetDict.keys(), key=lambda _key: int(_key))
	keys_y = sorted(yearDict_raceList.keys(), key=lambda _key: int(_key))

	if(freqOut):
		ret_dict = defaultdict(lambda:defaultdict(lambda:0))
		for key_t in keys_t:
			for raceID_t in targetDict[key_t]:
				for key_y in keys_y:
					if raceID_t in yearDict_raceList[key_y]:
						ret_dict[key_t][key_y] += 1

		return ret_dict
	else:
		ret_dict = defaultdict(lambda:[])
		for key_t in keys_t:
			for raceID_t in targetDict[key_t]:
					for key_y in keys_y:
						if raceID_t in yearDict_raceList[key_y]:
							if(key_y not in ret_dict[key_t]):
								ret_dict[key_t].append(key_y)
								continue
		return ret_dict

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

def getDriverIDPointsConstructor(dataset):
	ret = {"dataset": defaultdict(lambda: {driverID: "", points: 0, constructorID: ""})}
	_listOfList = [["DriverID", "Points","ConstructorID","TotalPoints", "NumberOfDrivers", "AveragePoints", "NumberOfCollaborations"]]
	# {driverID: {constructorID: points}}
	_temp = defaultdict(lambda:defaultdict(lambda:float(0)))
	# {driverID: totalpoints}
	_totalpoints = defaultdict(lambda:float(0))
	# {constructorID: [driverID]}
	_consDriver = defaultdict(lambda:[])
	# get number of collaborations in terms of years
	# {constructor: {driverID: [raceID]}}
	# Step 1: get {constructor: {driverID: [year]}}
	_consDriverYear = defaultdict(lambda:defaultdict())
	_consDriverRaceID = defaultdict(lambda:defaultdict(lambda:[]))
	# Step 1: get {driverID: [raceID]}
	# Step 2: convert to {driverID:[year]}

	# Step 1 #
	_driverRace = defaultdict(lambda:[])
	for data in dataset:
		_temp[data[1]][data[2]] += float(data[4])
		_totalpoints[data[1]] += float(data[4])
		_consDriver[data[2]].append(data[1])
		_consDriverRaceID[data[2]][data[1]].append(data[0])
		_driverRace[data[1]].append(data[0])

	yearDict_raceList = getYearRaceID("races.csv")
	# Step 2 #
	_driverYear = convertRaceToYear(_driverRace, yearDict_raceList)
	keys_CDR = sorted(_consDriverRaceID.keys(), key = lambda _key: int(_key))
	
	# Step 2 #
	for key_CDR in keys_CDR:
		_temp_DriverYear = convertRaceToYear(_consDriverRaceID[key_CDR], yearDict_raceList)
		keys_temp_DY = sorted(_temp_DriverYear.keys(), key= lambda _key: int(_key))
		for key_temp_DY in keys_temp_DY:
			_consDriverYear[key_CDR][key_temp_DY] = _temp_DriverYear[key_temp_DY]

	keys_temp = sorted(_temp.keys(), key = lambda _key: int(_key))
	for key_temp in keys_temp:
		keys_temp_inner = sorted(_temp[key_temp].keys(), key = lambda _key: int(_key))
		for key_temp_inner in keys_temp_inner:
			_listOfList.append([key_temp, \
				_temp[key_temp][key_temp_inner],\
				 key_temp_inner, _totalpoints[key_temp], \
				 len(_consDriver[key_temp_inner]),\
			 	_totalpoints[key_temp]/len(_driverYear[key_temp]), \
			 	len(_consDriverYear[key_temp_inner][key_temp])])
	return {"listofList": _listOfList}

if __name__ == '__main__':
	dataset = getRaceDriverConstRankPts("results.csv")
	DPS = getDriverIDPointsConstructor(dataset)
	# print DPS["listofList"]
	saveLListAsCSV("DriverID_Points_ConstructorID_TotalPoints_NumDrivers", DPS["listofList"])


