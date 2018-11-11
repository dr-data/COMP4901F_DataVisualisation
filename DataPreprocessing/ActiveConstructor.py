from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt

def getConstructorRaceList(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	dict{key:[list]}
		{constructorID: [raceID]}

	"""
	cons_Data = getDataset(filepath)
	dataObtained = cons_Data.next()
	print "Data Extracted: " + str(dataObtained)
	consDict_raceList = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	for race_cons in cons_Data:
		consDict_raceList[race_cons[1]].append(race_cons[0]) # {constructorID: [raceID]}
	return consDict_raceList

def getConstructorFrequency(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	list
		[constructorID, race frequency]

	"""
	consDict_raceList = getConstructorRaceList(filepath)
	keys = sorted(consDict_raceList.keys(), key=lambda _key: int(_key))
	for key in keys:
		yield [key, len(consDict_raceList[key])]

def _getFreqCons(cons_Data, threshold = 0, listOut = False):
	"""
	Parameters
	----------
	cons_Data: dict or list
		It is a dictionary if constructor data is {consID: [raceID]}
		It is a list if constructor data is [consID, race frequency]
	threshold : int
		The threshold value of the filter
	listOut: int or list
		default: return frequency
		True: return race list

	Returns
	-------
		default: return frequency
		True: return race list

	"""
	if(listOut):
		keys = sorted(cons_Data.keys(), key=lambda _key: int(_key))
		for key in keys:
			if(len(cons_Data[key]) < threshold):
				del cons_Data[key]
		return cons_Data
	else:
		return (consFreq for consFreq in cons_Data if consFreq[1] > threshold)

def getActiveCons(filepath, threshold = 0, listOut = False):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath
 	threshold : int
		The threshold value of the filter
	listOut: int or list
		default: return frequency
		True: return race list

	Returns
	-------
	default (False): [consID, race frequency]
	True: {consID: [raceID]}

	"""
	if(listOut):
		consRaceList = getConstructorRaceList(filepath)
		return _getFreqCons(consRaceList, threshold, listOut)
	else:
		consFreq = getConstructorFrequency(filepath)
		return _getFreqCons(consFreq, threshold, listOut)


def plotActiveCons(filepath, threshold = 0):
	"""
	This function plots the scatter plot of the active constructor

	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	None

	"""
	activeCons = getActiveCons(filepath,threshold)

	xAxis = []
	yAxis = []
	for cons in activeCons:
		xAxis.append(cons[0])
		yAxis.append(cons[1])

	# print xAxis
	# print yAxis
	fig = plt.figure(1)
	plt.plot(xAxis,yAxis, 'ro')
	plt.xlabel('constructor ID')
	plt.ylabel('race frequency')
	plt.title('race frequency versus constructor ID' + '(Threshold = ' + str(threshold) +')')
	saveFigureAsPNG("race frequency versus constructor ID"+ '(Threshold = ' + str(threshold) + ' )',fig)
	plt.show()


if __name__ == "__main__":
	print "start"
	allConstructors = getActiveCons("constructorResults.csv")
	activeConsFreq = getActiveCons("constructorResults.csv", 100)
	activeConsRace	= getActiveCons("constructorResults.csv", 100, True)
	consFrequency = getConstructorFrequency("constructorResults.csv")
	consRaceList = getConstructorRaceList("constructorResults.csv")
	plotActiveCons("constructorResults.csv", 0)
	plotActiveCons("constructorResults.csv", 100)
	saveListAsTxt('allConstructors', allConstructors)
	saveListAsTxt('activeConsFreq', activeConsFreq)
	saveDictAsTxt('activeConsRace', activeConsRace)
	saveListAsTxt('consFrequency', consFrequency)
	saveDictAsTxt('consRaceList', consRaceList)

	print "end"
