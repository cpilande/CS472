import matplotlib.pyplot as pt
from datetime import date
import seaborn  # color pallete generator
import csv

fig, ax = pt.subplots()
with open('./data/file_rootbeer_brandon.csv', 'r') as touchesCsv:
    reader = csv.reader(touchesCsv)
    header = False
    authors = {}
    fileCount = 0
    authorCount = 0
    lastFile = None

    for author, filename, year, month, day in reader:
        # Scan the header
        if not header:
            # generate a color_palette with n_authors colors
            palette = seaborn.color_palette("husl", int(author))

            year, month, day = [[
                int(item) for item in value.split('|')
            ] for value in [year, month, day]]  # deconstruct the header

            # reconstruct the origin commit date
            origin = date(year[0], month[0], day[0])
            # reconstruct the latest commit date
            latest = date(year[1], month[1], day[1])

            header = True

            continue

        commitDate = date(int(year), int(month), int(day))

        if not lastFile or lastFile != filename:  # track the filename
            lastFile = filename
            fileCount += 1

        if not authors.get(author):
            authors[author] = [
                [],
                [],
                palette[authorCount]  # assign each author a unique color
            ]
            authorCount += 1

        # Determine the commits time length from the origin
        y = abs(commitDate - origin).days // 7

        authors[author][0].append(fileCount)  # store the x point
        authors[author][1].append(y)  # store the y point

    for author in authors:

        xPoints, yPoints, color = authors.get(author)

        ax.scatter(xPoints, yPoints,
                   color=color, label=author)  # plot the points by author

    ax.legend(loc='upper right', fontsize=8,
              title="Authors")  # add the authors legend

    pt.xlabel('File Number')  # label the x axis
    pt.ylabel('Weeks')  # label the y axis
    pt.title('Source File Commit Data')  # add a title
    pt.show()  # show the points
