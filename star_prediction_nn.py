import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class StarPrediction:
    def __init__(self):
        super().__init__()
        # Dataset contains 1000 records
        data_frame = pd.read_csv("/data/data1000.csv")
        X = data_frame[["has_issues", "has_projects", "has_downloads", "has_wiki", "has_pages", "forks_count",
                        "archived", "disabled", "open_issues_count", "allow_forking", "is_template", "forks",
                        "open_issues", "score"]]
        Y = data_frame[["stargazers_count"]]
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=None, shuffle=True)


if __name__ == '__main__':
   app = StarPrediction()
