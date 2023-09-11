import json
import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt

import os

# Function used to convert the list into a dataframe.
# It is then converted into a list of numbers
# so it can be graphed int o a scatterplot
def convertToList(lst, enum):
    x = []
    for i in lst:
        if i not in x:
            x.append(i)
    for i in lst: #Gives each element an id
        enum.append(x.index(i))

def most_common(lst): #Finds the most common element
    return max(set(lst), key=lst.count)

#Returns the count of the most frequent element
def number_of_most_frequent(List): 
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter): #if the frequency is greater,
            counter = curr_frequency #set it to maximum
            num = i
    return counter

#Returns the count of the least frequent element
def number_of_least_frequent(List):
    counter = 1 #Initialize to 1, least number of commits
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency<counter): #if the frequency is less,
            counter = curr_frequency #set it to minimum
            num = i
    return counter

#Reads the file previously generated, containing the file name
#   the author, and the date of the touch
df = pd.read_csv('data/authorTouches.txt')

#Sorts the date values by most recent to oldest 
df.sort_values('Date')

#Processes the list of files
fileList = df['File Name'].tolist()
fileEnum = []
convertToList(fileList, fileEnum)

# Outputs the  most recently modified fiels
recentFiles = fileList[:16]
recentFiles = set(list(recentFiles))

#Processes the list of authors
authorList = df['Author'].tolist()
authorEnum = []
convertToList(authorList, authorEnum)

# Outtputs the first 3 authors
recentCommits = authorList[:3]

# Finds the author who committed the least
leastFrequent = min(authorList, key=authorList.count)

#Processes the list of dates
dateList = df['Date'].tolist()
dateEnum = []

# Adding value to each week
# Most recent week is 0
for index, item in enumerate(dateList):
    dateEnum.append(index)

#Creates a new file to output file name, authors, and dates of touch into
f = open("data/Summary.txt", "w")
f.write("Report Summary\n")
f.write("Developer with most commits: " + most_common(authorList) + ", " + str(number_of_most_frequent(authorList)) + " number of commits. \n")
f.write("Developer with least commits: " + leastFrequent + ", " + str(number_of_least_frequent(authorList)) + " number of commits.\n")
f.write("Most recent commits made by: " + str(recentCommits))
f.write("\nMost recent files modified: " + str(recentFiles))
f.write("\nTotal commits performed: " + str(len(dateList)) + "\n")
f.write("\nCommits List (by most recent)\n")
f.write("FileID, File Name\n")

for x, y in zip(fileEnum, fileList):
    f.write(str(x) + "," + str(y) + "\n")

#Creates the scatterplot
plt.title("Author Activity")
plt.xlabel("Files")
plt.ylabel("Weeks")

plt.scatter(fileEnum, dateEnum, c = authorEnum)
plt.show()