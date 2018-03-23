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
	keys = consDict_raceList.keys()
	keys.sort()
	for key in keys:
		yield [key, len(consDict_raceList[key])]

def getMostFreqCons(cons_Data, threshold = 0):
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
	# for consDict_raceList in cons_Data:
	# 	if consDict_raceList[1] > threshold:
	# 		yield consDict_raceList
	return (consDict_raceList for consDict_raceList in cons_Data if consDict_raceList[1] > threshold)

def getActiveCons(filepath, threshold = 0):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath
	threshold : int
		The threshold value of the filter 

	Returns
	-------
	dict{key:[list]}
		{constructorID: [raceID]}

	"""

	consFreq = getConstructorFrequency(filepath)
	return getMostFreqCons(consFreq, threshold = threshold)


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

	print xAxis
	print yAxis
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
	activeConstructors = getActiveCons("constructorResults.csv", 100)
	consFrequency = getConstructorFrequency("constructorResults.csv")
	consRaceList = getConstructorRaceList("constructorResults.csv")
	plotActiveCons("constructorResults.csv", 0)
	plotActiveCons("constructorResults.csv", 100)
	saveListAsTxt('allConstructors', allConstructors)
	saveListAsTxt('activeConstructors', activeConstructors)
	saveListAsTxt('consFrequency', consFrequency)
	saveDictAsTxt('consRaceList', consRaceList)

	print "end"
