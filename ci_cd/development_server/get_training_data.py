import requests
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

def get_data(page, per_page, length):
    """
    get training data of 1000 repo
    :param page:
    :param per_page:
    :param length:
    :return:
    """
    token = os.getenv('GITHUB_TOKEN', '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')
    query = "stars:>=50"
    order = "order=desc"
    page_ = "page="+str(page)
    per_page_ = "per_page="+str(per_page)
    query_url = f"https://api.github.com/search/repositories?q={query}&{order}&{page_}&{per_page_}"
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers)
    print(r.json())
    repos = r.json()['items']
    while 'next' in r.links.keys():
        r = requests.get(r.links['next']['url'], headers=headers)
        repos.extend(r.json()['items'])
        if len(repos) >= length:
            break
    data_ = []
    for repo in repos:
        data = {}
        default_branch = repo['default_branch']
        repo_url = repo['url']
        num_commit = commit_count(repo_url, default_branch)
        repo['num_commit'] = num_commit
        for key, value in repo.items():
            if type(value) in [int, float, bool]:
                data[key] = value
        data_.append(data)
    return data_
def main():
    repos_training = get_data(page=1, per_page=100, length=1000)
    with open('training_data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=repos_training[0].keys())
        writer.writeheader()
        writer.writerows(repos_training)



if __name__=="__main__":
    main()

# with open("sample.json", "w") as outfile:
#     json.dump(repos, outfile)
# print(len(repos))

