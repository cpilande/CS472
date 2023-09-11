import json
import requests
import csv
import pandas as pd

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

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["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"]

#Reads the .csv file as a dataframe
df = pd.read_csv('data/file_rootbeer.csv')
df['Filename'] = df['Filename'].astype(str)

#Creates a new file to output file name, authors, and dates of touch into
f = open("data/authorTouches.txt", "w")
f.write("File Name,Author,Date\n")

for indx in df.index: #Traverses through each file in the .csv file
    print(str( df['Filename'][indx]) + " is being searched for...")
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)
            #print(jsonCommits)
            
            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage

            for shaObject in jsonCommits:
                commits = 0
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lstTokens, ct)

                filesjson = shaDetails['files']

                authorsjson=shaDetails['commit']

                for filenameObj in filesjson:
                    check = 0
                    
                    filename = filenameObj['filename']
                    
                    if filename == df['Filename'][indx]: #Checks if file name is equal to the one in the .csv file
                       
                        for authorObj in authorsjson: #Accesses the author's name
                            authorObj=authorsjson['author']
                            
                            for nameObj in authorObj:
                                nameObj = authorObj['name']
                                
                                #Writes the file name, the name of the author, and the date
                                f.write(filename + ",")
                                f.write(nameObj + ",")
                                f.write(authorObj['date'] + "\n")
                                break
                            break
                        break
                        
                            
            print("Page " + str(ipage) + " is finished processing...")                         
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
   
   
   
f.close()
