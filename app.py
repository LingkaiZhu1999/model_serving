"""
Main file for the front-end server

"""


from inspect import getmodule
from flask import Flask, render_template, request
import numpy


from fetch_data import GithubCrawler
import validators
from save_model import ModelWrapper
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'


model_wrapper = ModelWrapper.loadModel("best_model")

if model_wrapper.metrics:
    for key, value in model_wrapper.metrics.items():
        print(type(value))
        if type(value) == numpy.float64:
            if abs(value) > 1:
                model_wrapper.metrics[key] = round(value)
            else:
                model_wrapper.metrics[key] = round(value, 3)


bot = GithubCrawler(token="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")


@app.route("/", methods=["GET"])
def index():
    """Home page"""

    return render_template("index.html", metrics=model_wrapper.metrics)


@app.route("/", methods=["POST"])
def predict():
    """Route for getting a prediction on a url"""
    url = request.form["repo_url"]
    if not validators.url(url):
        print("Invalid url")
        return render_template("index.html", error="Invalid url", metrics=model_wrapper.metrics)

    repo = bot.fetchRepoFromURL(url)

    if type(repo) != pd.DataFrame:
        return render_template("index.html", error="Repository not found", metrics=model_wrapper.metrics)

    ### Load model ###

    prediction = model_wrapper.predict(repo)
    actual = repo["stargazers_count"]
    return render_template("index.html", result={"prediction": prediction, "actual": actual.values[0]}, metrics=model_wrapper.metrics)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5555", debug=True)
