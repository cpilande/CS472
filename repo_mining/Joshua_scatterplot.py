import csv
import regex as re
import matplotlib.pyplot as plot
import random


def createNewColor(authorName, authorColorDict):
	if authorName not in authorColorDict:
		authorColorDict[authorName] =  [random.random() , random.random() , random.random()]

def trackFileName(fileName, fileNameList):
	if fileName not in fileNameList:
		fileNameList.append(fileName)

def trackDate(listedDate, trackedDates):
	if listedDate not in trackedDates:
		trackedDates.append(listedDate)

def scatterPlot(reader):
	next(reader)
	next(reader)

	for row in reader:
		unproccessedName = row[0]
		unproccessedDate = row[1]

		nameCompounded= re.sub('[0-9]*_', '', unproccessedName)
		authorName = re.sub(":\s.*", '', nameCompounded)
		fileName = re.sub(".*:\s" , '', nameCompounded)

		dateWithoutTime = re.sub("T.*", '', unproccessedDate)
		
		createNewColor(authorName, authorColorDictionary)
		trackFileName(fileName, fileNameList)
		trackDate(dateWithoutTime, dateList)
		plot.scatter(
			fileNameList.index(fileName),
			dateList.index(dateWithoutTime),
			color=authorColorDictionary[authorName]
			)
		
		# dateYear = dateWithoutTime[0:4]
		# dateMonth = dateWithoutTime[5:7]
		# dateDay = dateWithoutTime[8:11]
		next(reader)

		# pointList = [authorName, fileName, dateWithoutTime]
		# print(authorName + fileName + dateWithoutTime)
		# print(authorName +  fileName + dateYear + dateMonth + dateDay)
	plot.xlabel('files')
	plot.ylabel('weeks')
	plot.show()


repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

file = repo.split('/')[1]

fileInput = 'data/file_' + file + 'author' + '.csv'
fileCSV = open(fileInput, 'r')
reader = csv.reader(fileCSV)

authorColorDictionary = dict()
fileNameList = []
dateList = []

scatterPlot(reader)