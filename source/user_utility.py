from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt

"""
	change the directory
"""
os.chdir('..')
parentPath = os.getcwd() + os.path.sep
dataPath = parentPath + "Dataset/"
statsPath = parentPath + "Statistics/"
figPath = parentPath + "Figures/"

# functions to obtain the active drivers

def getDataset(filepath):
	"""
	Parameters
	----------
	filepath : string
		The filepath relative to the parentPath

	Returns
	-------
	list
		'constructorResults' : [raceID, constructorID]
		'races' : [raceID, year, circuitID, circuit name]

	"""
	dataDir = dataPath + filepath
	with open(dataDir, 'rb') as csvfile:
		data_col = csv.reader(csvfile)
		if(filepath.find('constructorResults') != -1):
			for data in data_col:
				yield [data[1], data[2]]	# [raceID, constructorID]
		if(filepath.find('races') != -1):
			for data in data_col:
				yield [data[0], data[1], data[3], data[4]]	# [raceID, year, circuitID, circuit name]

def saveListAsTxt(filename, data):
	statsDir = statsPath + filename + '.txt'
	f = open(statsDir, 'w')
	dataList = list(data)
	for d in dataList:
		f.write(str(d).strip().rstrip("]").lstrip("[") + "\n")
	f.close()

def saveDictAsTxt(filename, data):
	statsDir = statsPath + filename + '.txt'
	f = open(statsDir, 'w')
	keys = data.keys()
	keys.sort()
	for key in keys:
		f.write(str(key) + " " + str(data[key]).strip().rstrip("']").lstrip("['").replace("', '", " ") + "\n")
	f.close()

def saveFigureAsPNG(filename, fig):
	figDir = figPath + filename + '.png'
	fig.savefig(figDir)

if __name__ == "__main__":
	print "start"

	print "end"
