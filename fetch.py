import requests
import os
import json
from pprint import pprint

limit = 1

query_url = f'https://api.github.com/search/repositories?q=sort=stars&order=desc&per_page={limit}'

r1 = requests.get(query_url)
repos = r1.json()['items']
for repo in repos:
    r2 = requests.get(repo['commits_url'][:-6])
    commits = r2.json()
    watchers = repo['watchers']
    print(commits)
    print(watchers)
all_contributors = list()
page_count = 1
while True:
    contributors = requests.get("https://api.github.com/repos/rubinius/rubinius/contributors?page=%d"%page_count)
    if contributors != None and contributors.status_code == 200 and len(contributors.json()) > 0:
        all_contributors = all_contributors + contributors.json()
    else:
        break
    page_count = page_count + 1
count=len(all_contributors)
print("-------------------%d" %count)