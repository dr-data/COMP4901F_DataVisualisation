from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt
from Visualisation_3 import getRecentTracks
from operator import itemgetter
import numpy as np
from user_utility import getDataset, saveFigureAsPNG, saveListAsTxt, saveDictAsTxt, saveLListAsCSV, ifExist

def getCircuitInfoList(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	dict{key:[list]}
		{circuitID: [track information]}

	"""
	circuit_Data = getDataset(filepath)
	dataObtained = circuit_Data.next()
	print "Data from file: " + str(dataObtained)
	print "Data Extracted: " + 'circuitID ' + " raceInfo"
	circuitDict_InfoList = defaultdict(lambda:np.array([]))	# initialise the dictionary value to an empty list
	for circuitInfo in circuit_Data:
		# print race_circuit
		for i in xrange(len(circuitInfo)):
			if((i > 8) & (i < 1009)):
				# print circuitInfo[i]
				# if( circuitInfo[i] != ""):
				circuitDict_InfoList[circuitInfo[1]] = np.append(circuitDict_InfoList[circuitInfo[1]], np.int(circuitInfo[i]))
				# else:
					# print circuitInfo[1]
	return circuitDict_InfoList

def shiftRightNTimes(n, data):
	"""
	n : shift right n times
	data : a list to be shifted right

	Returns:
	--------
	list
	"""
	_ret_list = np.append(data[len(data) - n:len(data)],data[0:len(data) - n])
	# print data[0:10]
	# print (_ret_list[0:10])
	return _ret_list

def optimisedSimilarity(data1, data2):
	"""
	for simplicity, data1 has a lower index than data2
	find similarity between data1 and data2

	returns:
	int: n shifts needed
	list: the shifted list of data2
	"""
	_list_of_similarity = []
	if(len(data1) != len(data2)):
		raise -1
	for i in xrange(len(data2)):
		tempList1 = data1
		tempList2 = shiftRightNTimes(i,data2)
		similarity = 0
		for j in xrange(len(tempList1)):
			if(tempList1[j] == tempList2[j]):
				similarity += 1
		# similarity = np.sum(_booleanStatus)
		# similarity = np.sum((tempList1 - tempList2)**2) / 1000.0
		_list_of_similarity.append(similarity)
	n = np.argmax(_list_of_similarity)
	# print n
	# print _list_of_similarity[n]
	return (n, _list_of_similarity[n])

def getCovarianceMatrix(dataset):
	"""
	Inputs:
	------
	dicts: dataset

	Returns:
	-------
	list of list: n by n matrix
	list of list: [[circuitID1, circuitID2, n, circuitID2 Info]]
	"""
	_ret_list_of_list = np.zeros((len(dataset), len(dataset)))
	_ret_list_of_list2 = []
	_covarianceMatrix_headings = []
	dataset_keys = sorted(dataset.keys(), key = lambda _key: int(_key))
	for index1 in xrange(len(dataset_keys)):
		_covarianceMatrix_headings.append("CircuitId_" + dataset_keys[index1])
		for index2 in xrange(len(dataset_keys)):
			if(index1 == index2):
				continue	
			n, _similarity = optimisedSimilarity(dataset[dataset_keys[index1]], dataset[dataset_keys[index2]])
			_ret_list_of_list[index1][index2] = _similarity
			_ret_list_of_list[index2][index1] = _similarity
			temp_list = list(shiftRightNTimes(n,dataset[dataset_keys[index2]]).astype(int))
			temp_list.insert(0, n)
			temp_list.insert(0, dataset_keys[index2])
			temp_list.insert(0, dataset_keys[index1])
			_ret_list_of_list2.append(temp_list)
	_ret_list_of_list2.sort(key=itemgetter(0))
	# print _ret_list_of_list2
	return(_covarianceMatrix_headings, _ret_list_of_list, _ret_list_of_list2)

def  createDataFrame(listOfList, typeOfDataFrame, headings = None):
	if(typeOfDataFrame == "covarianceMatrix"):
		if(headings == None):
			raise -1
		_ret_list_of_list = list(listOfList)
		_ret_list_of_list.insert(0, headings)
		return _ret_list_of_list
	elif(typeOfDataFrame == "similarityList"):
		headings = ["circuitId1", "circuitId2", "n"]
		for i in xrange(1000):
			headings.append("P" + str(i + 1))
		_ret_list_of_list = listOfList
		_ret_list_of_list.insert(0, headings)
		return _ret_list_of_list

if __name__ == "__main__":
	print "start"

	"""
		obtain the frequency of active circuit and plot a scatter plot
	"""
	circuitDict_InfoList = getCircuitInfoList("new_track_data.csv")
	# print len(circuitDict_InfoList["20"])
	# shiftRightNTimes(4, circuitDict_InfoList["20"])
	# optimisedSimilarity(circuitDict_InfoList["20"], circuitDict_InfoList["18"])
	covarianceMatrixHeadings, covarianceMatrix, similarityList = getCovarianceMatrix(circuitDict_InfoList)
	CovarianceMatrix = createDataFrame(covarianceMatrix, "covarianceMatrix", covarianceMatrixHeadings)
	SimilarityInfoList = createDataFrame(similarityList, "similarityList", [])	
	saveLListAsCSV("CovarianceMatrixOfCircuits", CovarianceMatrix)
	saveLListAsCSV("SimilarityInfoList", SimilarityInfoList)


	print "end"
