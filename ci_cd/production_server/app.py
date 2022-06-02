"""
Main file for the front-end server
"""


from flask import Flask, render_template, request
from workerA import get_predictions, load_model, get_accuracy
from fetch_data import GithubCrawler
import validators
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'

bot = GithubCrawler(token="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")


@app.route("/", methods=["GET"])
def index():
    """Home page"""
    return render_template("index.html")


@app.route("/", methods=["POST"])
def predict():
    """Route for getting a prediction on a url"""
    url = request.form["repo_url"]
    if not validators.url(url):
        print("Invalid url")
        return render_template("index.html", error="Invalid url")

    repo = bot.fetchRepoFromURL(url)

    if type(repo) != pd.DataFrame:
        return render_template("index.html", error="Repository not found")

    ### Load model ###
    # model = loadModel()
    prediction = get_predictions(repo)
    accuracy = get_accuracy(repo)
    actual = repo["stargazers_count"]
    return render_template("index.html", result={"prediction": prediction, "actual": actual.values[0], "accuracy": accuracy})


if __name__ == "__main__":
    app.run(port="4000", debug=True)