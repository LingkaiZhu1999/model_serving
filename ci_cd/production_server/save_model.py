from pickle import NONE
import dill as pickle
from random import random

import pandas as pd
from typing import Tuple, Callable
from tensorflow import keras
import random
import string
import os
import numpy as np
import fnmatch
import shutil
from sklearn.preprocessing import MinMaxScaler

from fetch_data import GithubCrawler


class ModelWrapper:
    """Class to wrap a model with preprocessing, used to make it easier to make 
       predictions when preprocessing needs to be replicated on the new data

       NOTE: Do not scale the data in the preprocessing function! Instead give the scaler object used when first training the model as an argument


       To make predictions with this wrapper, simply use the predict method"""

    def __init__(self, model, featureSelectionFunction: Callable[[pd.DataFrame], Tuple[np.ndarray, np.ndarray]], scaler=None, metrics=None) -> None:
        self.model = model
        self.redoFeatureSelection = featureSelectionFunction
        self.object_name = "".join(random.choices(string.ascii_letters, k=7))
        self.scaler = scaler
        self.metrics = metrics
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Predict result on new data.

           Expects to receive data in the same format as given by the GitHubCrawler's fetch functions
        """
        _input, label = self.redoFeatureSelection(data)
        # Scale data if it was done when training the model
        # scaler = MinMaxScaler()
        # _input = scaler.fit_transform(_input, label)
        if self.scaler:
            _input = self.scaler.transform(_input)
        prediction = self.model.predict(_input)

        # Round the prediction result
        return round(prediction.ravel()[0])

    def save(self, dirname: str):
        """Serialize both the model and the feature selection function"""
        if os.path.isdir(dirname):
            overwite = input("Dir exists, overwrite? [y/n] ")
            if overwite.lower() == "y":
                shutil.rmtree(dirname)
            else:
                print("=== Aborting ===")
                return

        # Create a directory where the model will be saved
        dir = f"{os.path.dirname(os.path.realpath(__file__))}/{dirname}"
        os.mkdir(dir)
        tmp = self.model
        # Check if we can save the model with its own method
        if hasattr(self.model.__class__, 'save') and callable(getattr(self.model.__class__, 'save')):
            self.model.save(f"{dir}/{self.object_name}_model")
            self.model = None  # If the model can be saved like this there is a high chance that pickle wont be able to serialize it for some reason, so we temprarily remove the model attribute

        # Dump the model
        with open(f"{dir}/{self.object_name}_pickle", "wb") as f:
            pickle.dump(self, f)
        # Reset the model so we can continue to use this object
        self.model = tmp

    @classmethod
    def loadModel(cls, dirpath: str) -> 'ModelWrapper':
        """Load both the model and the preprocessing used when training the model.



            Used as ModelWrapper.loadModel("PATH_TO_MODEL_DIR")
        """
        for file in os.listdir(dirpath):
            # The main pickle file
            if fnmatch.fnmatch(file, "*_pickle"):
                with open(f"{dirpath}/{file}", "rb") as f:
                    model_wrapper = pickle.load(f)

        # This will be true if the model was saved with keras, since we set the model attribute to None
        if not model_wrapper.model:
            # Load the model itself with keras APIs
            model_wrapper.model = keras.models.load_model(
                f"{dirpath}/{model_wrapper.object_name}_model")

        return model_wrapper


if __name__ == "__main__":
    # model = keras.models.Model()

    # from custom_preprocessing import preProcess

    # m_wrapper = ModelWrapper(model, preProcess)
    # m_wrapper.saveModel("first_test_model")

    # loadedModelWrapper = ModelWrapper.loadModel("best_model")

    # keras.models.load_model("test")

    # Test
    url = "https://github.com/faif/python-patterns"
    bot = GithubCrawler(token="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")

    repo = bot.fetchRepoFromURL(url)

    model = ModelWrapper.loadModel("best_model")
    prediction = model.predict(repo)
    actual = repo["stargazers_count"]

    # print(loadedModelWrapper.model)
