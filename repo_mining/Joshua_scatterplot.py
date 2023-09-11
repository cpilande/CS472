import csv


repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

file = repo.split('/')[1]

fileInput = 'data/file_' + file + 'author' + '.csv'
fileCSV = open(fileInput, 'r')
reader = csv.reader(fileCSV)
