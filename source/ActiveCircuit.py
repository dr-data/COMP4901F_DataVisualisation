from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt

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
	keys = sorted(circuitDict_raceList.keys(), key=lambda _key: int(_key))
	for key in keys:
		yield [key, len(circuitDict_raceList[key])]

def _getFreqCircuit(circuit_Data, threshold = 0, listOut = False):
	"""
	Parameters
	----------
	circuit_Data: dict or list
		It is a dictionary if circuit data is {circuitID: [raceID]}
		It is a list if circuit data is [circuitID, race frequency]
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
		keys = sorted(circuit_Data.keys(), key=lambda _key: int(_key))
		for key in keys:
			if(len(circuit_Data[key]) < threshold):
				del circuit_Data[key]
		return circuit_Data
	else:
		return (circuitFreq for circuitFreq in circuit_Data if circuitFreq[1] > threshold)

def getActiveCircuit(filepath, threshold = 0, listOut = False):
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
	default (False): [circuitID, race frequency]
	True: {circuitID: [raceID]}

	"""
	if(listOut):
		circuitRaceList = getCircuitRaceList(filepath)
		# print circuitRaceList
		return _getFreqCircuit(circuitRaceList, threshold, listOut)
	else:
		circuitFreq = getCircuitFrequency(filepath)
		return _getFreqCircuit(circuitFreq, threshold, listOut)

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

	# print xAxis
	# print yAxis
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
	activeCircuitFreq = getActiveCircuit("races.csv", 20)
	activeCircuitRace = getActiveCircuit("races.csv", 20, True)
	circuitFrequency = getCircuitFrequency("races.csv")
	circuitRaceList = getCircuitRaceList("races.csv")
	plotActiveCircuit("races.csv", 0)
	plotActiveCircuit("races.csv", 20)
	saveListAsTxt('allCircuit', allCircuit)
	saveListAsTxt('activeCircuitFreq', activeCircuitFreq)
	saveDictAsTxt('activeCircuitRace', activeCircuitRace)
	saveListAsTxt('circuitFrequency', circuitFrequency)
	saveDictAsTxt('circuitRaceList', circuitRaceList)
	print "end"
