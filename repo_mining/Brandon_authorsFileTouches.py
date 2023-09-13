import time
import json
import requests
import csv

import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function


def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo


# unique commits
files = {}
# lastCommit Date
lastDate = None
# authors (used for color palette)
authors = {}


def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    origin = latest = None

    try:
        # loop though all the commit pages until the last returned empty page
        while True:

            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + \
                repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit

                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']

                date = time.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

                if not origin or date < origin:
                    origin = date

                if not latest or date > latest:
                    latest = date

                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    '''Check for files in any src directory with extension .java or .so'''
                    if 'src' in filename and any(ext in filename for ext in ['.java', '.cpp', '.c', '.kt']):
                        file = files.get(filename, [])
                        if not file:
                            files[filename] = []

                        count = dictfiles.get(filename, 0) + 1

                        files[filename].append([
                            author, filename, date.tm_year, date.tm_mon, date.tm_mday
                        ])  # store the author, filename, year, month, day

                        authors[author] = authors.get(
                            author, 0)+1  # unique authors

                        dictfiles[filename] = count

            ipage += 1
    except Exception as e:
        print("Error receiving data", e)
        exit(0)

    return origin, latest


# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ['''Omitted''']

dictfiles = dict()
origin, latest = countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '_brandon.csv'

''' Custom header outputs #authors, filename, (originYear|latestYear), (OriginMon|latestMon), (OriginMDay|LatestMDay)'''
rows = [f'{len(authors)}', "Filename",
        f"{origin.tm_year}|{latest.tm_year}",
        f"{origin.tm_mon}|{latest.tm_mon}",
        f"{origin.tm_mday}|{latest.tm_mday}"]

fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():

    writer.writerows(files[filename])

    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
