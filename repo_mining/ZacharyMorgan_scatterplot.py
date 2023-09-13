import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import pandas as pd
from datetime import datetime

# If not using jupyter to compile this, use the code below
#data = pandas.read_csv(r'data\file_rootbeer.csv')

# for jupyter notebook
data = pd.read_csv('file_rootbeer.csv')

currentDay = datetime.today().strftime('%Y-%m-%d')

data['Timestamp'] = pd.to_datetime(data['Timestamp'], format = '%Y-%m-%d')
data['TimeFormat'] = data['Timestamp'].astype(str).str[:10]
weekList = []
# Calculate the difference of weeks since last commit
for ind in data.index:
    curr = datetime.strptime(currentDay, '%Y-%m-%d')
    commDate = data['TimeFormat'][ind]
    commDate = datetime.strptime(commDate, '%Y-%m-%d')
    diff = curr - commDate
    weekList.append(diff.days//7)

data['Weeks'] = weekList

fileNumbers = []
fileDict = {val: idx for idx, val in enumerate(data['Filename'].unique())}
for i in data.index:
    grabName = data['Filename'][i]
    fileNumbers.append(fileDict.get(grabName))
data['FileNumber'] = fileNumbers

# Create a dictionary to match the authors with a color that will be stored in
# a color array below
authorColor = []
authDict = {val: idx for idx, val in enumerate(data['Author'].unique())}
for i in data.index:
    grabName = data['Author'][i]
    authorColor.append(authDict.get(grabName))

# Random color hex values made with a generator
colorMapping = np.array(['#cfecef', '#6a2fdf', '#2b0ccc', '#c6609a', '#f56473',
                     '#e8d26c', '#c0ed45', '#c98c49', '#2d7414', '#c6dcf9',
                     '#dfd704', '#e21668', '#081011', '#bed6f6', '#8f5c26'])

plt.scatter(data['FileNumber'], data['Weeks'], c = colorMapping[authorColor])
plt.title("Author Activity")
plt.xlabel("File")
plt.ylabel("Weeks")
plt.show()