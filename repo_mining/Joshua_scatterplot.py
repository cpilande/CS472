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
		next(reader)
		print(authorName + "\n" + fileName + "\n" +unproccessedDate)


		

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

file = repo.split('/')[1]

fileInput = 'data/file_' + file + 'author' + '.csv'
fileCSV = open(fileInput, 'r')
reader = csv.reader(fileCSV)

scatterPlot(reader)