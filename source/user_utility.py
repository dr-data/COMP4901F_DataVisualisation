from collections import defaultdict
import csv 
import json
import os
from os.path import join
from matplotlib import pyplot as plt
import csv

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

def saveListAsCSV(filename, data):
	statsDir = statsPath + filename + '.csv'
	with open(statsDir, "w") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    for val in data:
	        writer.writerow([val]) 

def saveLListAsCSV(filename, data):
	statsDir = statsPath + filename + '.csv'
	with open(statsDir, "w") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows(data)

def saveBitMapAsCSV(filename, data):
	statsDir = statsPath + filename + '.csv'
	output = open(statsDir, "w")
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow(["year"] + [str(year) for year in range(1950, 2019)])
	for x in xrange(len(data['keyList'])):
	    writer = csv.writer(output, lineterminator='\n')
	    outputList = []
	    outputList.append(int(data['keyList'][x]))
	    outputList.extend(data['bitmap'][x])
	    writer.writerow(outputList)

def saveDictAsTxt(filename, data):
	statsDir = statsPath + filename + '.txt'
	f = open(statsDir, 'w')
	keys = sorted(data.keys(), key=lambda _key: int(_key))
	for key in keys:
		f.write(str(key) + " " + str(data[key]).strip().rstrip("']").lstrip("['").replace("', '", " ") + "\n")
	f.close()

def saveFigureAsPNG(filename, fig):
	figDir = figPath + filename + '.png'
	fig.savefig(figDir)

def saveDDictAsTxt(filename, data):
	statsDir = statsPath + filename + '.txt'
	f = open(statsDir, 'w')
	keys_t = sorted(data.keys(), key=lambda _key: int(_key))
	for key_t in keys_t:
		f.write(str(key_t) + " \t ")
		keys_y = sorted(data[key_t].keys(), key=lambda _key: int(_key))
		for key_y in keys_y:
			f.write(str(key_y) + " : " + str(data[key_t][key_y]) + " \t ")
		f.write("\n")
	f.close()

def zeros(n):
	ret_list = []
	for x in xrange(n):
		ret_list.append(0)
	return ret_list

def ones(n):
	ret_list = []
	for x in xrange(n):
		ret_list.append(1)
	return ret_list


if __name__ == "__main__":
	print "start"

	print "end"
