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

def getActiveDrivers():
	"""
	Parameters
	----------
	[raceID, driverID, constructorID, rank, points]

	{year: {driverID:{ points : 0, rank : "", constructorID: ""}}}
	then convert to 
	{driverID: {year:{"rank" : rank, "points": points, "constructorID": consID}}}

	Returns
	-------
	ret_dict: dict{dict{[list]}}
		{driverID: {year:{"rank" : rank, "points": points, "constructorID": consID}}}
	"""
	RDCRP_data = getRaceDriverConstRankPts("results.csv") #[raceID, driverID, constructorID, rank, points]
	yearDict_raceList = getYearRaceID("races.csv")
	keys_yr = sorted(yearDict_raceList.keys(), key= lambda _key: int(_key))
	# print keys_yr
	# print yearDict_raceList["1950"]
	ret_dict = defaultdict(lambda:defaultdict(lambda:{rank: "", points: 0.0, constructorID: ""}))
	imm_dict = defaultdict(lambda:defaultdict(lambda:{"points": 0.0, "rank": "", "constructorID": ""}))
	error_list = []
	for data in RDCRP_data:
		year = _getYearFromRaceID(data[0], yearDict_raceList, keys_yr)
		# print year
		imm_dict[year][data[1]]["points"] += float(data[4])
		if(imm_dict[year][data[1]]["constructorID"] != ""
			and imm_dict[year][data[1]]["constructorID"] != data[2]):
			# raise ValueError
			# print "sudden change in constructorID" 
			# print "data"
			# print data
			# print "driverID"
			# print imm_dict[year]["driverID"]
			# print "new constructorID"
			# print data[2]
			# print "old constructorID"
			# print imm_dict[year]["constructorID"]
			error_list.append([data[1],year, imm_dict[year][data[1]]["constructorID"], data[2]])
			imm_dict[year][data[1]]["constructorID"] = data[2]
			# raise ValueError
		else:
			imm_dict[year][data[1]]["constructorID"] = data[2]
	print "error_list"
	print sorted(error_list, key=lambda d: d[1])
	# print imm_dict
	keys_immdict = sorted(imm_dict.keys(), key=lambda _key: int(_key))
	# print keys_immdict

	ret_dict_list = defaultdict(lambda:[])
	for key_immdict in keys_immdict:
		keys_driver = sorted(imm_dict[key_immdict], key=lambda _key:int(_key))
		imm_list = []
		for key_driver in keys_driver:
			imm_list.append([key_driver, imm_dict[key_immdict][key_driver]["points"], imm_dict[key_immdict][key_driver]["constructorID"], 0])
		imm_list = sorted(imm_list, key=lambda d: d[1], reverse = True)
		# print "year"
		# print key_immdict
		# print "imm_list"
		# print imm_list
		_rank = 1
		for item in imm_list:
			item[3] = _rank
			_rank += 1
		ret_dict_list[key_immdict] = imm_list
	# print ret_dict_list["2007"]


def getRecentDrivers(startingYear):
	"""
	Parameters
	----------
	[raceID, driverID, constructorID, rank, points]

	{year: {driverID:{ points : 0, rank : "", constructorID: ""}}}
	then convert to 
	{driverID: {year:{"rank" : rank, "points": points, "constructorID": consID}}}

	Returns
	-------
	ret_dict: dict{dict{[list]}}
		{driverID: {year:{"rank" : rank, "points": points, "constructorID": consID}}}
	"""
	RDCRP_data = getRaceDriverConstRankPts("results.csv") #[raceID, driverID, constructorID, rank, points]
	yearDict_raceList = getYearRaceID("races.csv")
	keys_yr = sorted(yearDict_raceList.keys(), key= lambda _key: int(_key))
	def ifExist(driverID, _DriverIDList):
		return (driverID in _DriverIDList)

	_ret_DriverIDList = []
	for data in RDCRP_data:
		year = _getYearFromRaceID(data[0], yearDict_raceList, keys_yr)
		# print year
		if(int(year) > startingYear):
			if(ifExist(data[1], _ret_DriverIDList)):
				 i = 1 # dummy operation
			else:
				_ret_DriverIDList.append(data[1])
	return _ret_DriverIDList	
	

if __name__ == '__main__':
	# getActiveDrivers()
	print len(getRecentDrivers(2000))
