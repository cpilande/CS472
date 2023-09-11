import csv
import regex as re
import matplotlib.pyplot as plot

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

		dateYear = re.sub("\-.*","",dateWithoutTime)
		# dateMonth = re.sub("","",dateYear)
		# dateDay = re.sub("","",dateMonth)
		next(reader)

		# pointList = [authorName, fileName, dateWithoutTime]
		print(authorName + "\n" + fileName + "\n" + dateYear)


		

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

file = repo.split('/')[1]

fileInput = 'data/file_' + file + 'author' + '.csv'
fileCSV = open(fileInput, 'r')
reader = csv.reader(fileCSV)

scatterPlot(reader)