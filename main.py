import requests
import os
import urllib
def commit_count(project, sha='main', token='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'):
    """
    Return the number of commits to a project
    """
    token = token or os.environ.get('GITHUB_API_TOKEN')
    url = f'https://api.github.com/repos/{project}/commits'
    # url = project + '/commits'
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

commit_count_ = commit_count("freeCodeCamp/freeCodeCamp")
print(commit_count_)