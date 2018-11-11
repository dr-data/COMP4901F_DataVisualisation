from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
import numpy as np
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt, saveDDictAsTxt,\
						saveListAsCSV, saveLListAsCSV, zeros, ones, saveBitMapAsCSV
from ActiveCircuit import getActiveCircuit
from ActiveConstructor import getActiveCons

# dataset information

minYear = 1950
maxYear = 2018
totalYearElapsed = maxYear - minYear + 1

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
		targeDict can be {consID: [raceID]} or {circuitID: [raceID]}
	yearDict_raceList: dict
		{year: dict}
	freqOut: dict of dict of list
		False: {circuitID:[year]}
		True: {consID: {year: frequency}}
	Returns
	-------
	freqOut == False 
		{circuitID: [year]} or {consID: [year]}
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

def losslessCompression(dict_of_list):
	"""
	Note:
	Lossless Compression is a simple compression of the information to store the
	ones and zeros of the bitmap

	Example
	-------
	[0 3 1 5 1 2]
	--> meaning the number at the odd positions represent number of zeros
		the number at the even positions represent the number of ones
	Deciphering the meaningn of the list:
	0 zeros
	3 ones
	1 zeros
	5 ones
	1 zeros
	2 ones

	After decoding the list:
	1 1 1 0 1 1 1 1 1 0 1 1


	Parameters
	----------
	dict_of_list: dict 

	Returns
	-------
	dict of list 


	"""
	ret_dict_list = defaultdict(lambda:[])
	keys_t = sorted(dict_of_list.keys(), key=lambda _key: int(_key))
	for key_t in keys_t:
		curYear = minYear
		for year in sorted(dict_of_list[key_t]):
			yearDiff = int(year) - curYear
			if ((yearDiff == 0) & (curYear == minYear)):
				ret_dict_list[key_t].append(0)
				ret_dict_list[key_t].append(1)
				curYear = int(year)
				continue
			if(yearDiff == 1):
				if ((curYear == minYear)& (len(ret_dict_list[key_t]) == 0)):
					ret_dict_list[key_t].append(1)
					ret_dict_list[key_t].append(1)
					curYear = int(year)
					continue
				else:
					value = ret_dict_list[key_t].pop()
					value += 1
					ret_dict_list[key_t].append(value)
					curYear = int(year)
					continue

			if (yearDiff > 1):
				if((curYear == minYear) & (len(ret_dict_list[key_t]) == 0)):
					ret_dict_list[key_t].append(yearDiff)
					ret_dict_list[key_t].append(1)
					curYear = int(year)
					continue
				else:
					ret_dict_list[key_t].append(yearDiff-1)
					ret_dict_list[key_t].append(1)
					curYear = int(year)
					continue
		if(curYear <= maxYear):
			ret_dict_list[key_t].append(maxYear - curYear)
		# to check the consistency of the number of years ( maxYear - minYear +1)
		if sum(ret_dict_list[key_t]) != (maxYear - minYear +1):
			print str(key_t) + " : " + str(sum(ret_dict_list[key_t]))
			print sorted(dict_of_list[key_t], key=lambda _key: int(_key))
			print ret_dict_list[key_t]

	return ret_dict_list

def buildBitMap(compressed_data):
	"""
	Parameters
	----------
	compressed_data: dict of list
		The compressed_data is the losslessCompression of the bitmap

	Returns
	-------
	dict of list
		{"keyList": keys_t, "bitmap": ret_maplist}

	"""
	keys_t = sorted(compressed_data.keys(), key=lambda _key: int(_key))
	ret_maplist = []
	for key_t in keys_t:
		status_01 = False # status to print 1's or 0's
		temp = []
		for n in compressed_data[key_t]:
			if status_01:
				temp.extend(ones(n))
				status_01 = False
			else:
				temp.extend(zeros(n))
				status_01 = True
		ret_maplist.append(temp)
	return {"keyList": keys_t ,"bitmap": ret_maplist}

def displayBitMap(bitmap_key, mapName):
	"""
	Parameters
	----------
	bitmap_key: dict of list
		Takes in the input generated by the buildBitMap function and 
		visualises the bitmap in a black and white diagram
		Black: Active
		White: Inactive

	mapName: string
		The diagrams/ visualisations generated would be saved as <mapName>.PNG

	Returns:
	NO return

	"""
	output = plt.figure(1)
	fig = plt.imshow(bitmap_key['bitmap'],cmap='Greys', interpolation='nearest')
	plt.xlabel('Year Elapsed since 1950 (Ends in Year 2018)')
	plt.ylabel(mapName)
	plt.title('Bit Map of ' + mapName)
	fig.axes.get_xaxis().set_visible(False)
	fig.axes.get_yaxis().set_visible(False)
	saveFigureAsPNG('Bit Map of ' + mapName, output)
	plt.show()

if __name__ == "__main__":
	yearDict_raceList = getYearRaceID("races.csv")
	activeCircuitRace = getActiveCircuit("races.csv", -1, True)
	activeConsRace = getActiveCons("constructorResults.csv", -1, True)
	print len(activeConsRace)

	# just to obtain the statistics of circuit_year and constructor_year_frequency
	circuit_year_dict = convertRaceToYear(activeCircuitRace, yearDict_raceList, False)
	cons_year_freq_dict = convertRaceToYear(activeConsRace, yearDict_raceList, True)
	saveDictAsTxt("CircuitYear", circuit_year_dict)
	saveDDictAsTxt("ConstructorYearFreq", cons_year_freq_dict)

	# obtaining constructor bit map and circuit bit map
	cons_year_dict = convertRaceToYear(activeConsRace, yearDict_raceList, False)
	compressed_cons_year = losslessCompression(cons_year_dict)
	# print sorted(circuit_year_dict['6'], key=lambda _key: int(_key))
	saveDictAsTxt("cons_year(compressed)", compressed_cons_year)
	cons_bitmap = buildBitMap(compressed_cons_year)

	# print circuit_year_dict
	compressed_circuit_year = losslessCompression(circuit_year_dict)
	# print compressed_circuit_year
	saveDictAsTxt("circuit_year(compressed)", compressed_circuit_year)
	circuit_bitmap = buildBitMap(compressed_circuit_year)
	# print bitmap['keyList']
	# print bitmap['bitmap']
	displayBitMap(cons_bitmap, "Active Constructor")
	displayBitMap(circuit_bitmap, "Active Circuit")
	# saveListAsTxt("Bitmap_of_Active_Constructor", cons_bitmap['bitmap'])
	# saveLListAsCSV("Bitmap_of_Active_Constructor_LList", cons_bitmap['bitmap'])
	saveBitMapAsCSV("Bitmap_of_Active_Constructor", cons_bitmap)
	saveBitMapAsCSV("Bitmap_of_Active_Circuit", circuit_bitmap)




					
