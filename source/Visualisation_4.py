from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt, saveLListAsCSV
from ActiveDrivers import getRecentDrivers
from Visualisation_2 import getRaceID_Grid_FirstLapPosition_FinalPosition
import numpy as np
import copy
from ActiveCircuit import getCircuitRaceList
from operator import itemgetter

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

def getConstructorIDName(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	dict{key:string}
		{ConstructorID: ConstructorName}

	"""
	cons_Data = getDataset(filepath)
	# print list(cons_Data)
	dataObtained = cons_Data.next()
	print "Data Extracted: " + str(dataObtained)
	ret_dict = {}
	for _cons in cons_Data:
		ret_dict[_cons[0]] = _cons[1]
	return ret_dict

def getDriverIDName(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	dict{key:string}
		{ConstructorID: ConstructorName}

	"""
	driver_Data = getDataset(filepath)
	# print list(cons_Data)
	dataObtained = driver_Data.next()
	print "Data Extracted: " + str(dataObtained)
	ret_dict = {}
	for _driver in driver_Data:
		ret_dict[_driver[0]] = _driver[1] + " " + _driver[2]
	return ret_dict

def getDriverIDPointsConstructor(dataset):
	ret = {"dataset": defaultdict(lambda: {driverID: "", points: 0, constructorID: ""})}
	_listOfList = [["DriverID", "DriverName" ,"Points","ConstructorID", "ConstructorName","TotalPoints", "NumberOfDrivers", "AveragePoints", "NumberOfCollaborations", "Years", "ConstructorAveragePoints", "StartingPosition", "PositionAfterFirstLap", "FinalPosition"]]
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
	ConstructorIDName = getConstructorIDName("constructors.csv")
	DriverName = getDriverIDName("drivers.csv")
	# Step 2 #
	_driverYear = convertRaceToYear(_driverRace, yearDict_raceList)
	keys_CDR = sorted(_consDriverRaceID.keys(), key = lambda _key: int(_key))
	
	# Step 2 #
	for key_CDR in keys_CDR:
		_temp_DriverYear = convertRaceToYear(_consDriverRaceID[key_CDR], yearDict_raceList)
		keys_temp_DY = sorted(_temp_DriverYear.keys(), key= lambda _key: int(_key))
		for key_temp_DY in keys_temp_DY:
			_consDriverYear[key_CDR][key_temp_DY] = _temp_DriverYear[key_temp_DY]

	# dict_of_list {driverID: [starting position, position after first lap, ending position]}
	_dict_grid_firstLapPosition_finalPosition = getRaceID_Grid_FirstLapPosition_FinalPosition()

	keys_temp = sorted(_temp.keys(), key = lambda _key: int(_key)) # driverID
	for key_temp in keys_temp:
		keys_temp_inner = sorted(_temp[key_temp].keys(), key = lambda _key: int(_key))
		# temp string for years
		_temp_year_string = ""

		for str_year in _driverYear[key_temp]:
			# print _driverYear[key_temp]
			_temp_year_string = _temp_year_string + "," + str(str_year)

		for key_temp_inner in keys_temp_inner:
			for _data in _dict_grid_firstLapPosition_finalPosition[key_temp]:	
				_listOfList.append([key_temp, \
					DriverName[key_temp], \
					_temp[key_temp][key_temp_inner],\
					 key_temp_inner, ConstructorIDName[key_temp_inner],\
					 _totalpoints[key_temp], \
					 len(_consDriver[key_temp_inner]),\
				 	_totalpoints[key_temp]/len(_driverYear[key_temp]), \
				 	len(_consDriverYear[key_temp_inner][key_temp]), \
				 	_temp_year_string, \
				 	_temp[key_temp][key_temp_inner]/len(_consDriverYear[key_temp_inner][key_temp]),\
				 	_data[1], _data[2], _data[3]])

	return {"listofList": _listOfList}

def filterDataAccordingToRecentDrivers(dataset):
	_ret_dataset = []
	RecentDriverList = getRecentDrivers(1990)
	_temp_headings = dataset[0]
	_ret_dataset.append(_temp_headings)
	for data in dataset:
		if(data[0] in RecentDriverList):
			_ret_dataset.append(data)
	return _ret_dataset

def getDriverTopPerformingCircuits():
	def returnCategory(rank):
		if(int(rank) == 1):
			# print "1"
			return "1"
		if((int(rank) > 1) & (int(rank) < 4)):
			# print "2-3"
			return "2_3"
		if((int(rank) > 3) & (int(rank) < 11)):
			# print "4-10"
			return "4_10"
		return "others"

	# step one temp data structure {driverID: {rank: {circuitId: count}}}
	_tempCountDict = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
	# step two temp data structure {driverID: {rank: [circuitId, count]}}
	_tempCountList = defaultdict(lambda:defaultdict(lambda:[]))
	# return list [driverID, _ranking, circuit_id]
	_ret_list = []

	circuitRaceList = getCircuitRaceList("races.csv") # {circuitID: raceList}
	RGFF_dict = getRaceID_Grid_FirstLapPosition_FinalPosition() # {driverID: [ raceID, starting position, position after first lap, final position]}
	# print circuitRaceList
	# print RGFF_dict

	_RGFF_dict_keys = sorted(RGFF_dict.keys(), key = lambda _key: int(_key))
	_circuitRace_keys = sorted(circuitRaceList.keys(), key = lambda _key: int(_key))
	# print _RGFF_dict_keys
	# print _circuitRace_keys
	for _rkey in _RGFF_dict_keys:
		for _ckey in _circuitRace_keys:
			# print (RGFF_dict[_rkey])
			# print circuitRaceList[_ckey]
			for _driverInfo in RGFF_dict[_rkey]:
				if(_driverInfo[0] in circuitRaceList[_ckey]):
					# print RGFF_dict[_rkey][3]
					_tempCountDict[_rkey][returnCategory(_driverInfo[3])][_ckey] += 1

	# print _tempCountDict
	driverIDKeys = sorted(_tempCountDict.keys(), key = lambda _key: int(_key))
	for _dikey in driverIDKeys:
		rankingKeys = _tempCountDict[_dikey].keys()
		for _rkey in rankingKeys:
			circuitKeys = _tempCountDict[_dikey][_rkey].keys()
			for _ckey in circuitKeys:
				_temp_2Dlist = [_ckey,_tempCountDict[_dikey][_rkey][_ckey]]
				# _tempCountList[_dikey][_rkey][0] = _ckey
				# _tempCountList[_dikey][_rkey][1] = _tempCountDict[_dikey][_rkey][_ckey]
				_tempCountList[_dikey][_rkey].append(_temp_2Dlist)
			_tempCountList[_dikey][_rkey].sort(key=itemgetter(1), reverse = True)

	driverIDKeys = sorted(_tempCountList.keys(), key = lambda _key: int(_key))
	for _dikey in driverIDKeys:
		rankingKeys = _tempCountList[_dikey].keys()
		for _rkey in rankingKeys:
			breakCount = 0
			# print _tempCountList[_dikey][_rkey]
			_temp_top3Circuits = ""
			for listData in (_tempCountList[_dikey][_rkey]):
				_temp_top3Circuits += ( "_" + str(listData[0]))
				breakCount += 1
				if(breakCount > 2):
					break
			_ret_list.append([_dikey, _rkey, _temp_top3Circuits])
	return _ret_list

def createDataFrame(headings, data):
	headings = ["driverId", "ranking", "circuits"]
	data.insert(0,headings)
	saveLListAsCSV("DriversTopPerformingCircuits", data)

if __name__ == '__main__':
	dataset = getRaceDriverConstRankPts("results.csv")
	DPS = getDriverIDPointsConstructor(dataset)
	# print DPS["listofList"]
	# newArray = np.array(DPS["listofList"])[]
	FilteredDataset = filterDataAccordingToRecentDrivers(DPS["listofList"])
	saveLListAsCSV("PreprocessedDataset4", FilteredDataset)
	headings = []
	createDataFrame(headings, getDriverTopPerformingCircuits())




