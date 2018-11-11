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

def getDriverRankRace(dataset, targetFilter = None):
	"""
	Parameters
	----------
	dataset: list
		[raceID, driverID, constructorID, rank]

	targetFilter: list (Optional) # if specified, return {rank: [raceID]} corresponds to the specified driverID
		[driverID]

	Returns
	-------
	dict{dict{}}
		{driverID: {rank:[raceID]}}
	"""
	ret_dict = defaultdict(lambda: defaultdict(lambda: []))
	for data in dataset:
		# if(data[1] == '1'):
		# 	print data[0] + ":" + data[3] + '\n'

		# prune the one which doesn't have a rank due to various status: unfinished
		if(data[3] == '-1'):
			continue
		else:
			if(targetFilter == None):
				ret_dict[data[1]][data[3]].append(data[0])
			else:
				if(data[1] in targetFilter):
					ret_dict[data[1]][data[3]].append(data[0])

	# print ret_dict
	return ret_dict

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
	print targetDict.keys()
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

def convertDriverRankRacetoDriverYearRank(DRR_data, yearDict_raceList):
	"""
	Parameters
	----------
	DRR_data:dict{dict{list}}
		{driverID:{rank:[raceID]}}

	yearDict_raceList: dict{list}
		{year:[raceID]}

	Returns
	-------
	ret_dict: dict{dict{string}}
		{driverID:{year:rank}}

	"""
	ret_dict = defaultdict(lambda:defaultdict(lambda:""))
	keys_drr = sorted(DRR_data.keys(), key=lambda _key: int(_key))
	for key_drr in keys_drr:
		rank_year = convertRaceToYear(DRR_data[key_drr], yearDict_raceList)
		# print rank_year
		keys_ry = sorted(rank_year.keys(), key=lambda _key: int(_key))
		for key_ry in keys_ry:
			for year in rank_year[key_ry]:
				# print year
				# print key_ry
				ret_dict[key_drr][year] = key_ry
	# print ret_dict
	return ret_dict

def plotDict_YearRank(YR_dict, driverID = ""):
	"""
	Parameters
	----------
	YR_dict: dict{}
		{year:rank}

	Returns
	-------
	None

	Output
	------
	Plot a diagram rank versus year

	"""
	xAxis = map(int,sorted(YR_dict.keys(), key=lambda _key: int(_key)))
	yAxis = []
	for x in xAxis:
		yAxis.append(int(YR_dict[str(x)]))
	fig = plt.figure(1)
	plt.plot(xAxis,yAxis, marker ='o')
	plt.axis([1950,2017, 0, 25])
	plt.ylim(25, 0)
	plt.xlabel('Year')
	plt.ylabel('Rank')
	plt.title('Rank versus Year' + '(Driver ID = ' + str(driverID) +')')
	plt.show()

def getActiveDrivers(dataset, threshold = 6,rule = "raceID" ):
	"""
	Parameters
	----------
	dataset: 
		"raceID":
			{driverID: {rank:[raceID]}}
		"year":
			{driverID: {rank:[raceID]}} is converted into {driverID:{year:rank}}
	rule: string
		"raceID": filter according to the number of raceIDs
		"year"	: filter according to the number of years
	threshold: int

	Returns
	-------
		"raceID":
		ret_dict: dict{dict{list}}
			{driverID: {rank:[raceID]}}
		"year"
		DYR_data: dict{dict{}}
			{driverID:{year:rank}}

	"""
	# Need to double check this if statement
	if(rule == "raceID"):
		# ret_dict = defaultdict(lambda: defaultdict(lambda: []))
		ret_dict = copy.deepcopy(dataset)
		keys_d = sorted(ret_dict.keys(), key=lambda _key: int(_key))
		for key_d in keys_d:
			_size = 0
			keys_r = sorted(ret_dict[key_d].keys(), key=lambda _key: int(_key))
			for key_r in keys_r: 
				_size += len(ret_dict[key_d][key_r])
				# print ret_dict[key_d][key_r]
			if(_size < threshold):
				ret_dict.pop(key_d)
		return ret_dict
	# DONE functioning
	elif(rule == "year"):
		yearDict_raceList = getYearRaceID("races.csv")
		DYR_data = convertDriverRankRacetoDriverYearRank(dataset, yearDict_raceList)
		# ret_dict = defaultdict(lambda:{})
		keys_dyr = sorted(DYR_data.keys(), key=lambda _key: int(_key))
		for key_dyr in keys_dyr:
			_size = len(DYR_data[key_dyr].keys())
			if(_size < threshold):
				DYR_data.pop(key_dyr)
		return DYR_data


if __name__ == "__main__":
	dataset = getRaceDriverConstRankPts("results.csv")
	yearDict_raceList = getYearRaceID("races.csv")
	# print yearDict_raceList
	DRR_data = getDriverRankRace(dataset)
	print DRR_data
	DYR_data = convertDriverRankRacetoDriverYearRank(DRR_data, yearDict_raceList)
	# plotDict_YearRank(DYR_data["27"], "27")
 	
	activeDriversYear = getActiveDrivers(DRR_data, 3, "year")
	activeDriversRaceID = getActiveDrivers(DRR_data, 100, "raceID")
	# print "activeDriversYear"
	# print activeDriversYear
	# print "activeDriversRaceID"
	# print activeDriversRaceID
	keys = sorted(activeDriversYear.keys(), key=lambda _key: int(_key))
	for key in keys:
		plotDict_YearRank(activeDriversYear[key], key)