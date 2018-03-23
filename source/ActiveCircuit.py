from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt
"""
	change the directory
"""
os.chdir('..')
parentPath = os.getcwd() + os.path.sep
dataPath = parentPath + "Dataset/"
statsPath = parentPath + "Statistics/"
figPath = parentPath + "Figures/"

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
	print "Data from file: " + str(dataObtained)
	print "Data Extracted: " + 'circuitID ' + " raceID"
	circuitDict_raceList = defaultdict(lambda:[])	# initialise the dictionary value to an empty list
	for race_circuit in circuit_Data:
		# print race_circuit
		circuitDict_raceList[race_circuit[2]].append(race_circuit[0]) # {circuitID: [raceID]}
	return circuitDict_raceList

def getCircuitFrequency(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	list
		[circuitID, race frequency]

	"""
	circuitDict_raceList = getCircuitRaceList(filepath)
	keys = circuitDict_raceList.keys()
	keys.sort()
	for key in keys:
		yield [key, len(circuitDict_raceList[key])]

def getMostFreqCircuit(circuit_Data, threshold = 0):
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
	# for circuitDict_raceList in circuit_Data:
	# 	if circuitDict_raceList[1] > threshold:
	# 		yield circuitDict_raceList
	return (circuitDict_raceList for circuitDict_raceList in circuit_Data if circuitDict_raceList[1] > threshold)

def getActiveCircuit(filepath, threshold = 0):
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
		{circuitID: [raceID]}

	"""

	circuitFreq = getCircuitFrequency(filepath)
	return getMostFreqCircuit(circuitFreq, threshold = threshold)

def plotActiveCircuit(filepath, threshold = 0):
	"""
	This function plots the scatter plot of the active circuittructor

	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	None

	"""
	activeCircuit = getActiveCircuit(filepath,threshold)

	xAxis = []
	yAxis = []
	for circuit in activeCircuit:
		xAxis.append(circuit[0])
		yAxis.append(circuit[1])

	print xAxis
	print yAxis
	fig = plt.figure(1)
	plt.plot(xAxis,yAxis, 'ro')
	plt.xlabel('circuit ID')
	plt.ylabel('race frequency')
	plt.title('race Frequency Vs Circuit ID' + '(Threshold = ' + str(threshold) + ' )')
	saveFigureAsPNG("race frequency versus circuit ID"+ '(Threshold = ' + str(threshold) + ' )',fig)
	plt.show()


if __name__ == "__main__":
	print "start"

	"""
		obtain the frequency of active circuit and plot a scatter plot
	"""
	allCircuit = getActiveCircuit("races.csv")
	activeCircuit = getActiveCircuit("races.csv", 20)
	circuitFrequency = getCircuitFrequency("races.csv")
	circuitRaceList = getCircuitRaceList("races.csv")
	plotActiveCircuit("races.csv", 0)
	plotActiveCircuit("races.csv", 20)
	saveListAsTxt('allCircuit', allCircuit)
	saveListAsTxt('activeCircuit', activeCircuit)
	saveListAsTxt('circuitFrequency', circuitFrequency)
	saveDictAsTxt('circuitRaceList', circuitRaceList)
	print "end"
