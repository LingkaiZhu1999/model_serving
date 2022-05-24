import requests
import os
import json
from pprint import pprint
import os
import urllib
import csv

def commit_count(project, sha='main', token='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'):
    """
    Return the number of commits to a project
    """
    token = token or os.environ.get('GITHUB_API_TOKEN')
    # url = f'https://api.github.com/repos/{project}/commits'
    url = project + '/commits'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'token {token}',
    }
    params = {
        'sha': sha,
        'per_page': 1,
    }
    resp = requests.request('GET', url, params=params, headers=headers)
    if (resp.status_code // 100) != 2:
        raise Exception(f'invalid github response: {resp.content}')
    # check the resp count, just in case there are 0 commits
    commit_count = len(resp.json())
    last_page = resp.links.get('last')
    # if there are no more pages, the count must be 0 or 1
    if last_page:
        # extract the query string from the last page url
        qs = urllib.parse.urlparse(last_page['url']).query
        # extract the page number from the query string
        commit_count = int(dict(urllib.parse.parse_qsl(qs))['page'])
    return commit_count

def get_data():
    token = os.getenv('GITHUB_TOKEN', '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')
    query = "stars:>=50"
    order = "order=desc"
    page = "page=10"
    per_page = "per_page=100"
    query_url = f"https://api.github.com/search/repositories?q={query}&{order}&{page}&{per_page}"
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers)
    repos = r.json()['items']
    repo_url = []
    while 'next' in r.links.keys():
        r = requests.get(r.links['next']['url'], headers=headers)
        repos.extend(r.json()['items'])
        if len(repos) == 1000:
            break
    data_ = dict({'commits': [], 'forks': [], 'watchers': [], 'size': [], 'star': [], 'open_issue':[]})
    for repo in repos:
        default_branch = repo['default_branch']
        repo_url = repo['url']
        num_commit = commit_count(repo_url, default_branch)
        fork = repo['forks']
        watcher = repo['watchers']
        star_gazers = repo['stargazers_count']
        size = repo['size']
        open_issue = repo['open_issues']
        data_['commits'].append(num_commit)
        data_['forks'].append(fork)
        data_['watchers'].append(watcher)
        data_['star'].append(star_gazers)
        data_['size'].append(size)
        data_['open_issue'].append(open_issue)
    return data_

def main():
    data = get_data()
    with open('data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows(data)

if __name__=="__main__":
    main()

# with open("sample.json", "w") as outfile:
#     json.dump(repos, outfile)
# print(len(repos))

