import json
import requests
import csv
import os

repo = 'scottyab/rootbeer'
lstTokens = []

input_csv = 'data/file_rootbeer.csv'
output_csv = 'data/file_authors_dates.csv'

# GitHub Authentication function
def github_auth(url, lstTokens, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lstTokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

if not os.path.exists('data'):
    os.makedirs('data')

# Read the files list from the generated CSV
with open(input_csv, 'r') as f:
    reader = csv.reader(f)
    file_list = list(reader)[1:]  # Skip the header row

# Open the output CSV and write the header row
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Filename", "Author", "Date"])
    
    ct = 0
    # For every file, get list of commits that touched it
    for row in file_list:
        filename = row[0]
        print(f'Getting data for file: {filename}')
        
        ipage = 1
        while True:
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={ipage}&path={filename}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)
            
            if not jsonCommits or len(jsonCommits) == 0:
                break
            
            for commit in jsonCommits:
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']
                writer.writerow([filename, author, date])
            
            ipage += 1
