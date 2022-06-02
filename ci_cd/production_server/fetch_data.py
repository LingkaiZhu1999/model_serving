

from email import header
from logging import raiseExceptions
from sys import argv
import requests
import pandas as pd
import os
import urllib


class GithubCrawler:

    def __init__(self, token="") -> 'GithubCrawler':

        self.baseURL = "https://api.github.com"
        if token == "":
            try:
                self.auth = os.environ["token"]
            except KeyError:
                print("Failed fetching github api token,\nhave you set the enviroment variable 'token' with your github developer api key?")
                exit(1)
        else:
            self.auth = token
        self.header = {"Authorization": self.auth}
        self.wanted_keys = ['watchers_count', "watchers", 'has_issues', 'has_projects', 'has_downloads', 'has_wiki', 'has_pages', 'forks_count',
                            'archived', 'disabled', 'open_issues_count', 'allow_forking', 'is_template', 'forks', 'open_issues', 'score', "stargazers_count"]

    def checkRateLimit(self):
        """Show the current rate limit of the user"""
        response = requests.get(f"{self.baseURL}/rate_limit",
                                self.header)
        if response.status_code == 200:
            response = response.json()
            print(response)
        else:

            print("Error sending request")
            print(response.status_code)
            print(response.reason)

    def fetchRepoFromURL(self, url: str) -> pd.DataFrame:
        """Get the metadata associated with a repository's URL"""
        full_name = url.replace("https://github.com/", "")
        full_name = "/".join(full_name.split("/", 2)[:2])
        print(f"Fetching repo with name: {full_name}")
        return self.fetchSpecificRepo(full_name)

    def fetchExample(self):
        """Show an example of the data sent by the GitHub search API"""
        query = f"stars:>50&sort=stars&order=desc&per_page=1"
        response = requests.get(
            f"{self.baseURL}/search/repositories?q={query}", self.header).json()
        print(response["items"][0])

    # From George´s amazing commit counter code
    def commit_count(self, project, sha='main', token='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'):
        """
        Return the number of commits to a project
        """

        url = f'https://api.github.com/repos/{project}/commits'
        # url = project + '/commits'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'token {self.auth}',
        }
        params = {
            'sha': sha,
            'per_page': 1,
        }
        resp = requests.get(url, headers=headers)
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

    def fetchSpecificRepo(self, full_name: str):
        """Fetch a specific repository, full_name is the name of the owner as well as the 
           repository name on the forman OWNER/REPO_NAME"""

        response = requests.get(
            f"{self.baseURL}/repos/{full_name}", headers=self.header)

        if response.status_code != 200:
            print("Error sending request")
            print(response.status_code)
            print(response.reason)
            print(response.text)
            return
        wantedTypes = [int, float, bool]
        repo = response.json()

        item = {

            "id": repo["id"],
            "full_name": repo["full_name"],

        }

        for key, value in repo.items():
            if key in self.wanted_keys:
                item[key] = value
        # Add number of commits
        item["n_commits"] = self.commit_count(
            repo["full_name"], self.auth)
        return pd.DataFrame([item])

    def fetchRepos(self, nRepos=1000) -> pd.DataFrame:
        """Get nRepos many repositories"""
        reposPerPage = 100 if nRepos >= 100 else nRepos
        query = f"stars:>50&sort=stars&order=desc&per_page={reposPerPage}"
        response = requests.get(
            f"{self.baseURL}/search/repositories?q={query}", self.header)

        repos = []

        while len(repos) < nRepos:

            if response.status_code != 200:
                print("Error sending request")
                print(response.reason)
                break

            repositories = response.json()["items"]
            for repo in repositories:

                item = {

                    "id": repo["id"],
                    "full_name": repo["full_name"],

                }
                for key, value in repo.items():
                    if key in self.wanted_keys:
                        item[key] = value
                print(item["full_name"])
                # Add number of commits
                item["n_commits"] = self.commit_count(
                    repo["full_name"], self.auth)

                repos.append(item)

            if "next" in response.links.keys():
                response = requests.get(
                    response.links["next"]["url"], self.header)

        result = pd.DataFrame(repos)

        return result


if __name__ == "__main__":

    ## Testing

    bot = GithubCrawler()
    # nRepos = int(input("Enter number of repos to fetch "))
    # result = bot.fetchRepos(nRepos=nRepos)

    # filename = input("Enter filename of where to store csv ")
    # result.to_csv(filename, index_label=False, index=False)
    print(bot.fetchRepoFromURL("https://github.com/modin-project/modin"))

    # repo = bot.fetchSpecificRepo("flutter/flutter")
    # print(repo.info())
