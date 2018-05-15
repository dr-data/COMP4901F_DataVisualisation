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
		data_col = csv.reader(x.replace('\0', '') for x in csvfile)
		# data_col = csv.reader(csvfile)
		if(filepath.find('constructorResults') != -1):
			for data in data_col:
				yield [data[1], data[2]]	# [raceID, constructorID]
		if(filepath.find('races') != -1):
			for data in data_col:
				yield [data[0], data[1], data[3], data[4]]	# [raceID, year, circuitID, circuit name]
		if(filepath.find('results') != -1):
			for data in data_col:
				try:
					# if(data[14] == ""):
					# 	continue
					# 	yield [data[1], data[2], data[3], str(-1)] # [raceID, driverID, constructorID, missing rank]
					# else:
					yield [data[1], data[2], data[3], data[14], data[9], data[5], data[6], data[8]] 
					# [raceID, driverID, constructorID, rank, points, grid, postion, positionOrder]
				except ValueError:
				    yield [data[1], data[2], data[3], -1, data[9], data[5], data[6], data[8]]		# [raceID, driverID, constructorID, missing rank]
		if(filepath.find('constructors.csv') != -1):
			for data in data_col:
				yield [data[0], data[2]]	# [ConstructorID, ConstructorName]
		if(filepath.find('drivers.csv') != -1):
			for data in data_col:
				yield [data[0], data[4], data[5]]	# [DriverID, Driver's forename, Drivers' surname]
		if(filepath.find('track_data_final') != -1):
			for data in data_col:
				yield data[0:36]
		if(filepath.find('pitStops') != -1):
			for data in data_col:
				yield data
		if(filepath.find('lapTimes') != -1):
			for data in data_col:
				yield data
		if(filepath.find('PreprocessedDataset1') != -1):
			for data in data_col:
				yield data			



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

def ifExist(item, itemList):
	return (item in itemList)

if __name__ == "__main__":
	print "start"

	print "end"
