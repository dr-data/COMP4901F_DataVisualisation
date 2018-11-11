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
from ActiveDrivers import getRecentDrivers
from ActiveCircuit import getCircuitRaceList
from Visualisation_3 import getRecentTracks, getRecentTracksName

def getDataFromResults(filepath):
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
	RecentDriversList = getRecentDrivers(2000)
	circuitRaceList = getCircuitRaceList("races.csv")
	circuitRaceKeys = circuitRaceList.keys()
	ResultData = getDataset(filepath)
	dataObtained = ResultData.next()
	Data = []
	# Data = list(ResultData)
	for data in ResultData:
		if(ifExist(data[1], RecentDriversList)):
			for key in circuitRaceKeys:
				if(data[0] in circuitRaceList[key]):
					Data.append(data)
	print "Data from file: " + str(dataObtained)
	# print "Data Extracted: " + 'Year ' + " raceID"
	# yearDict_raceList = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	# dataObtained.append("firstLapChange")
	# for d in Data:
	# 	d.append(int(d[5]) - int(d[7]))
	return (dataObtained, Data)

def getPitStops(filepath):
	"""
	Parameters
	----------
	filepath: string
		The directory to the file relative to the parentPath
		# [raceId, driverId, stop, lap, time, duration, milliseconds]
	Returns
	-------
	tuple
		(headings, data, dictionary)

	"""
	RecentDriversList = getRecentDrivers(2000)
	circuitRaceList = getCircuitRaceList("races.csv")
	circuitRaceKeys = circuitRaceList.keys()
	PitStopsData = getDataset(filepath)
	dataObtained = PitStopsData.next()
	Data = []
	for data in PitStopsData:
		if(ifExist(data[1], RecentDriversList)):
			for key in circuitRaceKeys:
				if(data[0] in circuitRaceList[key]):
					Data.append(data)
	# Data = list(PitStopsData)
	print "Data from file: " + str(dataObtained)
	# print "Data Extracted: " + 'Year ' + " raceID"
	_ret_dict = defaultdict(lambda:defaultdict(lambda:0.0))
	for d in Data:
		# {raceId, driverId :{ stop: pit time }}
		_ret_dict[str(d[0]) +"," + str(d[1])][d[2]] = d[6]
	return (dataObtained, Data, _ret_dict)

def getLapTimes(filepath):
	"""
	Parameters
	----------
	filepath: string
		The directory to the file relative to the parentPath
		# [raceId, driverId, lap, position, time, milliseconds]
	Returns
	-------
	tuple
		(headings, data, dictionary, dictionary of dictionary)
	"""
	RecentDriversList = getRecentDrivers(2000)
	circuitRaceList = getCircuitRaceList("races.csv")
	circuitRaceKeys = circuitRaceList.keys()
	LapTimesData = getDataset(filepath)
	dataObtained = LapTimesData.next()
	# Data = list(LapTimesData)
	Data = []
	for data in LapTimesData:
		if(ifExist(data[1], RecentDriversList)):
			for key in circuitRaceKeys:
				if(data[0] in circuitRaceList[key]):
					Data.append(data)
	print "Data from file: " + str(dataObtained)
	# {raceID: [[driverID, lap#, laptime]]}
	_ret_dict = defaultdict(lambda:[])
	# {raceID: {lap#: [driverID, laptime]}}
	_ret_dict_dict = defaultdict(lambda:defaultdict(lambda:[]))
	for d in Data:
		# {raceId, driverId :{ lap: laptime]] 
		# _ret_dict[str(d[0]) +"," + str(d[1])][d[2]] = d[5]
		_ret_dict[int(d[0])].append(np.array([int(d[1]), int(d[2]), int(d[5])]))
		# {raceID: {lap#: [driverID, laptime]}}
		_ret_dict_dict[int(d[0])][int(d[2])].append([int(d[1]), int(d[5])])
	# keys = sorted(_ret_dict_dict.keys(), lambda _key: int(_key))
	keys = _ret_dict_dict.keys()
	for key in keys:
		_keys = _ret_dict_dict[key].keys()
		for _key in _keys:
			_ret_dict_dict[key][_key].sort(key=itemgetter(1))
			# print _ret_dict_dict[key][_key]
	return (dataObtained, Data, _ret_dict,_ret_dict_dict)

def InsertFirstLapChange(headings, main_data, RaceLapDict):

	_ret_data = []
	# obtain additional data
	_ret_dict_list = defaultdict(lambda:[])
 	# main_data = ['raceId', 'driverId', 'constructorId', 'rank', 'points', 'grid', 'position', 'positionOrder', "positionText"]
	# initial dataset
	headings.append("firstLapChange")
	for main_d in main_data:
		endingPosition = 1
		initialLength = len(main_d)
		# print "main_data"
		# print main_data
		# print str(RaceLapDict[int(main_d[0])][int(main_d[2])])
		# print RaceLapDict[int(main_d[0])][int(main_d[2])]
		# {raceID: {lap#: [driverID, laptime]}}
		for d in RaceLapDict[int(main_d[0])][1]:

			if(int(d[0]) == int(main_d[1])):
				_ret_dict_list[main_d[1]].append([main_d[0], main_d[5], endingPosition, main_d[7]])
				main_d.append(int(main_d[5]) - endingPosition)
				_ret_data.append(main_d)
				break
			else:
				endingPosition += 1

		if(len(main_d) == initialLength):
				# _ret_dict_list[main_d[1]].append([main_d[0], main_d[5], main_d[7], main_d[7]])
				main_d.append(-999)
				# del main_d

	# del main_data 
	# main_data = _ret_data
	# print main_data
	return _ret_dict_list

def InsertPitStopsTime(headings, main_data, PitStopsDict):
	headings.append("pitStops")
	keysList = PitStopsDict.keys()
	index = 0
	for main_d in main_data:

		pitTime = ""
		index += 1
		if(index == 23778):
			break
		if((main_d[0]+ "," + main_d[1]) in keysList):
			stops = sorted(PitStopsDict[str(main_d[0])+ "," + str(main_d[1])].keys(), key=lambda _key:int(_key))
			for stop in stops:
				pitTime += str(PitStopsDict[str(main_d[0])+ "," + str(main_d[1])][stop] + ",")
		main_d.append(pitTime)

def getRaceID_Grid_FirstLapPosition_FinalPosition():
	ResultHeadings, ResultData = getDataFromResults("results.csv")
	PitStopsHeadings, PitStopsData, PitStopsDict = getPitStops("pitStops.csv")
	LapTimesHeadings, LapTimesData, LapTimesDict, RaceLapDict = getLapTimes("lapTimes.csv")
	return InsertFirstLapChange(ResultHeadings, ResultData, RaceLapDict)

def generateDataset():
	ResultHeadings, ResultData = getDataFromResults("results.csv")
	PitStopsHeadings, PitStopsData, PitStopsDict = getPitStops("pitStops.csv")
	LapTimesHeadings, LapTimesData, LapTimesDict, RaceLapDict = getLapTimes("lapTimes.csv")
	InsertFirstLapChange(ResultHeadings, ResultData, RaceLapDict)
	keys = PitStopsDict.keys()
	InsertPitStopsTime(ResultHeadings, ResultData, PitStopsDict)

	_data_needed = []
	for data in ResultData:
		if((data[7] >= "A") & (data[7] <= "Z")):
			continue
		else:
			_data_needed.append(data)

	_data_needed.insert(0,ResultHeadings)



	saveLListAsCSV("PreprocessedDataset1", _data_needed)

def getPreprocessedData(filepath):
	"""
	Parameters
	----------
	filepath: string
		The directory to the file relative to the parentPath
		# [raceId, driverId, constructorId, rank, points, grid, position, positionOrder, positionText , firstLapChange, pitStops]
	Returns
	-------
	tuple
		(headings, data, dictionary)
	"""
	RecentDriversList = getRecentDrivers(2000)
	circuitRaceList = getCircuitRaceList("races.csv")
	circuitRaceKeys = circuitRaceList.keys()
	PreprocessedData = getDataset(filepath)
	dataObtained = PreprocessedData.next()
	# Data = list(PreprocessedData)
	Data = []
	for data in PreprocessedData:
		if(ifExist(data[1], RecentDriversList)):
			for key in circuitRaceKeys:
				if(data[0] in circuitRaceList[key]):
					Data.append(data)
	print "Data from file: " + str(dataObtained)

	return (dataObtained, Data)

def getCircuitRaceList(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	dict{key:[list]}
		{circuitID: [raceID]}

	"""
	circuit_Data = getDataset(filepath)
	dataObtained = circuit_Data.next()
	RecentTracksList = getRecentTracks()
	print "Data from file: " + str(dataObtained)
	print "Data Extracted: " + 'circuitID ' + " raceID"
	circuitDict_raceList = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	for race_circuit in circuit_Data:
		# print race_circuit
		if(race_circuit[2] in RecentTracksList):
			circuitDict_raceList[race_circuit[2]].append(race_circuit[0]) # {circuitID: [raceID]}
	return circuitDict_raceList

def getDriverIDName(filepath):
	"""
		filepath: drivers.csv

	Returns:
	--------
	dictionary:
		{DriverID: DriverName}
	"""
	driversData = getDataset(filepath)
	dataObtained = driversData.next()
	print "Data from file: " + str(dataObtained)
	print "Data Extracted: " + 'driverID ' + " driverName"
	driverIDNameDict = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	for data in driversData:
		driverIDNameDict[data[0]] = data[1] + " " + data[2]
	return driverIDNameDict

def getOverallStatisticsOfFirstLapChange(headings):
	"""
		for overall statistics
	"""
	headings.append("DriverId")
	headings.append("DriverName")
	# headings.append("CircuitId")
	headings.append("FirstLapChangeList")
	headings.append("FirstLapChangeMin")
	headings.append("FirstLapChangeMax")
	headings.append("FirstLapChangeFirstQuartile")
	headings.append("FirstLapChangeMedian")
	headings.append("FirstLapChangeThirdQuartile")
	headings.append("FirstLapChangeMean")
	headings.append("FirstLapChangeSd")
	_ret_list = []

	circuitRaceList = getCircuitRaceList("races.csv")
	PreprocessedDataHeadings, PreprocessedDataset = getPreprocessedData("PreprocessedDataset1.csv")
	driverIDNameDict = getDriverIDName("drivers.csv")

	# temperary data structure
	# {driverId: {circuitId: [first lap change]}}
	_dict_dict_list = defaultdict(lambda:defaultdict(lambda:[])) 

	for data in PreprocessedDataset:
		circuitKeys = circuitRaceList.keys()
		for circuitKey in circuitKeys:
			if(data[0] in circuitRaceList[circuitKey]):
				_dict_dict_list[data[1]][circuitKey].append(data[9])

	# data structure to remap the driverIDs, constructorIDs and circuitIDs
	driversKeys = sorted(_dict_dict_list.keys(), key = lambda _key: int(_key))
	for driversKey in driversKeys:
		_driverID = driversKey
		_driverName = driverIDNameDict[_driverID]
		_FirstLapChangeList = ""
		_FirstLapChangeMin = 0.0
		_FirstLapChangeMax = 0.0
		_FirstLapChangeFirstQuartile = 0.0
		_FirstLapChangeMedian = 0.0
		_FirstLapChangeThirdQuartile = 0.0
		_FirstLapChangeMean = 0.0
		_FirstLapChangeSd = 0.0
		_tempContainer = []
		driverCircuitsKeys = sorted(_dict_dict_list[driversKey].keys(), key = lambda _key: int(_key))
		for driverCircuitsKey in driverCircuitsKeys:
			for firstLapChangeVal in _dict_dict_list[driversKey][driverCircuitsKey]:
				if(firstLapChangeVal != "-999"):
					_FirstLapChangeList += (firstLapChangeVal + ",")
					_change = int(firstLapChangeVal)
					print "_change"
					print _change
					_tempContainer.append(_change)
		_tempContainer.sort(key=lambda _key: int(_key))
		# print _FirstLapChangeList
		if(len(_tempContainer) != 0):
			_FirstLapChangeMin=_tempContainer[0]
			_FirstLapChangeMax=_tempContainer[-1]
			_FirstLapChangeFirstQuartile = _tempContainer[len(_tempContainer)/4]
			_FirstLapChangeMedian=_tempContainer[len(_tempContainer)/2]
			_FirstLapChangeThirdQuartile = _tempContainer[len(_tempContainer)/4 *3]
			_FirstLapChangeMean=np.sum(np.array(_tempContainer))/len(_tempContainer)
			_FirstLapChangeSd=np.sqrt(np.sum(((np.array(_tempContainer)-_FirstLapChangeMean)**2))/len(_tempContainer))
		_ret_list.append([_driverID, _driverName, _FirstLapChangeList, _FirstLapChangeMin, _FirstLapChangeMax, _FirstLapChangeFirstQuartile,
			_FirstLapChangeMedian, _FirstLapChangeThirdQuartile, _FirstLapChangeMean, _FirstLapChangeSd])

	_ret_list.insert(0,headings)
	saveLListAsCSV("PreprocessedDataset2", _ret_list)

def getCircuitSpecificStatisticsOfFirstLapChange(headings):
	"""
		for circuit specific statistics
	"""
	headings.append("DriverId")
	headings.append("DriverName")
	headings.append("CircuitId")
	headings.append("CircuitName")
	headings.append("FirstLapChangeList")
	headings.append("FirstLapChangeMin")
	headings.append("FirstLapChangeMax")
	headings.append("FirstLapChangeFirstQuartile")
	headings.append("FirstLapChangeMedian")
	headings.append("FirstLapChangeThirdQuartile")
	headings.append("FirstLapChangeMean")
	headings.append("FirstLapChangeSd")
	_ret_list = []

	circuitRaceList = getCircuitRaceList("races.csv")
	PreprocessedDataHeadings, PreprocessedDataset = getPreprocessedData("PreprocessedDataset1.csv")
	circuitNameDict = getRecentTracksName()
	driverIDNameDict = getDriverIDName("drivers.csv")
	# temperary data structure
	# {driverId: {circuitId: [first lap change]}}
	_dict_dict_list = defaultdict(lambda:defaultdict(lambda:[])) 

	for data in PreprocessedDataset:
		circuitKeys = circuitRaceList.keys()
		for circuitKey in circuitKeys:
			if(data[0] in circuitRaceList[circuitKey]):
				_dict_dict_list[data[1]][circuitKey].append(data[9])

	# print _dict_dict_list["4"]["32"]
	driversKeys = sorted(_dict_dict_list.keys(), key = lambda _key: int(_key))
	for driversKey in driversKeys:
		_driverID = driversKey
		_driverName = driverIDNameDict[_driverID]
		_circuitID = ""
		_circuitName = ""
		_FirstLapChangeList = ""
		_FirstLapChangeMin = 0.0
		_FirstLapChangeMax = 0.0
		_FirstLapChangeFirstQuartile = 0.0
		_FirstLapChangeMedian = 0.0
		_FirstLapChangeThirdQuartile = 0.0
		_FirstLapChangeMean = 0.0
		_FirstLapChangeSd = 0.0
		driverCircuitsKeys = sorted(_dict_dict_list[driversKey].keys(), key = lambda _key: int(_key))
		for driverCircuitsKey in driverCircuitsKeys:
			# _tempSumOfFirstLapChange = 0.0;
			_tempContainer = []
			_circuitID = driverCircuitsKey
			_circuitName = circuitNameDict[_circuitID]
			for firstLapChangeVal in _dict_dict_list[driversKey][driverCircuitsKey]:
				if(firstLapChangeVal != "-999"):
					_FirstLapChangeList += (firstLapChangeVal + ",")
					_change = int(firstLapChangeVal)
					_tempContainer.append(_change)
			_tempContainer.sort(key=lambda _key: int(_key))
			if(len(_tempContainer) != 0):
				_FirstLapChangeMin=_tempContainer[0]
				_FirstLapChangeMax=_tempContainer[-1]
				_FirstLapChangeFirstQuartile = _tempContainer[len(_tempContainer)/4]
				_FirstLapChangeMedian=_tempContainer[len(_tempContainer)/2]
				_FirstLapChangeThirdQuartile = _tempContainer[len(_tempContainer)/4 *3]
				_FirstLapChangeMean=np.sum(np.array(_tempContainer))/len(_tempContainer)
				_FirstLapChangeSd=np.sqrt(np.sum(((np.array(_tempContainer)-_FirstLapChangeMean)**2))/len(_tempContainer))
			_ret_list.append([_driverID, _driverName, _circuitID, _circuitName, _FirstLapChangeList, _FirstLapChangeMin, _FirstLapChangeMax, _FirstLapChangeFirstQuartile,
				_FirstLapChangeMedian, _FirstLapChangeThirdQuartile, _FirstLapChangeMean, _FirstLapChangeSd])

		# print _FirstLapChangeList
		# if(len(_tempContainer) != 0):
		# 	_FirstLapChangeMin=_tempContainer[0]
		# 	_FirstLapChangeMax=_tempContainer[-1]
		# 	_FirstLapChangeFirstQuartile = _tempContainer[len(_tempContainer)/4]
		# 	_FirstLapChangeMedian=_tempContainer[len(_tempContainer)/2]
		# 	_FirstLapChangeThirdQuartile = _tempContainer[len(_tempContainer)/4 *3]
		# 	_FirstLapChangeMean=np.sum(np.array(_tempContainer))/len(_tempContainer)
		# 	_FirstLapChangeSd=np.sqrt(np.sum(((np.array(_tempContainer)-_FirstLapChangeMean)**2))/len(_tempContainer))
		# _ret_list.append([_driverID, _FirstLapChangeList, _FirstLapChangeMin, _FirstLapChangeMax, _FirstLapChangeFirstQuartile,
		# 	_FirstLapChangeMedian, _FirstLapChangeThirdQuartile, _FirstLapChangeMean, _FirstLapChangeSd])

	_ret_list.insert(0,headings)
	saveLListAsCSV("PreprocessedDataset3", _ret_list)

if __name__ == '__main__':
	generateDataset()
	OverallStatisticsHeadings = []
	CircuitSpecificStatisticsHeadings = []
	getOverallStatisticsOfFirstLapChange(OverallStatisticsHeadings)
	getCircuitSpecificStatisticsOfFirstLapChange(CircuitSpecificStatisticsHeadings)

