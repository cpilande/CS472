import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
from collections import defaultdict
import numpy as np
import os
import random

# Read the data and organize it in a usable structure
data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

with open('data/file_authors_dates.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header 

    for row in reader:
        filepath, author, date = row
        filename = os.path.basename(filepath)  # Get only the filename, ignore directories
        date = datetime.strptime(date.split('T')[0], '%Y-%m-%d')
        data[filename][author][date] += 1

# Calculate the weeks since the first commit for each commit date
first_commit_date = min(date for filenames in data.values() for authors in filenames.values() for date in authors.keys())

# Create scatter plot using matplotlib
plt.figure(figsize=(10, 6))

authors = set()
for filename in data:
    for author in data[filename]:
        authors.add(author)

authors = list(authors)

# Create a list of unique colors, using a colormap for the first 20 and random colors for the others
colors = plt.cm.tab20(np.linspace(0, 1, min(20, len(authors))))
colors = list(colors) + [(random.random(), random.random(), random.random(), 1.0) for _ in range(len(authors) - 20)]
color_map = {author: colors[i] for i, author in enumerate(authors)}

for filename in data:
    for author in data[filename]:
        commit_dates = list(data[filename][author].keys())
        weeks_since_first_commit = [(date - first_commit_date).days // 7 for date in commit_dates]
        plt.scatter([filename] * len(weeks_since_first_commit), weeks_since_first_commit, c=[color_map[author]] * len(weeks_since_first_commit), label=author, alpha=0.7, s=50)  # Set a fixed size for all dots

# Add labels, legend, and title
plt.xlabel('Files')
plt.ylabel('Weeks Since First Commit')
plt.title('File Touches vs Weeks Since First Commit by Author')
plt.xticks(rotation=90)

# Create the custom legend
handles = [plt.Line2D([0], [0], marker='o', color='w', label=author, markersize=10, markerfacecolor=color_map[author]) for author in authors]
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
