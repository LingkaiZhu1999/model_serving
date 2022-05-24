

from sys import argv
import requests
import pandas as pd
import os


class GithubCrawler:

    def __init__(self) -> 'GithubCrawler':
        self.baseURL = "https://api.github.com"
        try:
            self.auth = os.environ["token"]
        except KeyError:
            print("Failed fetching github api token,\nhave you set the enviroment variable 'token' with your github developer api key?")
            exit(1)
        self.header = {"Authorization": self.auth}

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

    def fetchExample(self):
        """Show an example of the data sent by the GitHub search API"""
        query = f"stars:>50&sort=stars&order=desc&per_page=1"
        response = requests.get(
            f"{self.baseURL}/search/repositories?q={query}", self.header).json()
        print(response["items"][0])

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

            wantedTypes = [int, float, bool]
            for repo in repositories:

                item = {

                    "id": repo["id"],
                    "full_name": repo["full_name"],

                }
                for key, value in repo.items():
                    if key == "id":
                        continue

                    if type(value) in wantedTypes:
                        item[key] = value

                # print(item)

                repos.append(item)

            if "next" in response.links.keys():
                response = requests.get(
                    response.links["next"]["url"], self.header)

        result = pd.DataFrame(repos)

        return result


if __name__ == "__main__":

    bot = GithubCrawler()
    nRepos = int(input("Enter number of repos to fetch "))
    result = bot.fetchRepos(nRepos=nRepos)

    filename = input("Enter filename of where to store csv ")
    result.to_csv(filename)
