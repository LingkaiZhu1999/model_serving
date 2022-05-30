
import pickle
from random import random

import pandas as pd
from typing import Tuple, Callable
import keras
import random
import string
import os
import numpy as np
import fnmatch
import shutil


class ModelWrapper:
    """Class to wrap a model with preprocessing, used to make it easier to make 
       predictions when preprocessing needs to be replicated on the new data

       NOTE: Do not scale the data in the preprocessing function! Instead give the scaler object used when first training the model as an argument


       To make predictions with this wrapper, simply use the predict method"""

    def __init__(self, model, preProcess: Callable[[pd.DataFrame], Tuple[np.ndarray, np.ndarray]], scaler=None) -> None:
        self.model = model
        self.redoPreProcessing = preProcess
        self.object_name = "".join(random.choices(string.ascii_letters, k=7))
        self.scaler = scaler

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        print(self.model)
        _input, label = self.redoPreProcessing(data)
        if self.scaler:
            _input = self.scaler.transform(_input)
        prediction = self.model.predict(_input)

        return prediction

    def saveModel(self, dirname: str):
        """Serialize both the model and the preprocessing function"""
        if os.path.isdir(dirname):
            overwite = input("Dir exists, overwrite? [y/n] ")
            if overwite.lower() == "y":
                shutil.rmtree(dirname)
            else:
                print("=== Aborting ===")
                return

        dir = f"{os.path.dirname(os.path.realpath(__file__))}/{dirname}"
        os.mkdir(dir)
        tmp = self.model
        if hasattr(self.model.__class__, 'save') and callable(getattr(self.model.__class__, 'save')):
            self.model.save(f"{dir}/{self.object_name}_model")
            self.model = None

        with open(f"{dir}/{self.object_name}_pickle", "wb") as f:
            pickle.dump(self, f)
        self.model = tmp

    @classmethod
    def loadModel(cls, dirpath: str) -> 'ModelWrapper':
        """Load both the model and the preprocessing used when training the model.



            Used as ModelWrapper.loadModel("PATH_TO_DIR")
        """
        for file in os.listdir(dirpath):
            print(file)
            if fnmatch.fnmatch(file, "*_pickle"):
                with open(f"{dirpath}/{file}", "rb") as f:
                    model_wrapper = pickle.load(f)

        if model_wrapper is None:
            print("Error loading model")
            return
        if not model_wrapper.model:
            model_wrapper.model = keras.models.load_model(
                f"{dirpath}/{model_wrapper.object_name}_model")

        return model_wrapper


if __name__ == "__main__":
    # model = keras.models.load_model("NN_model")

    # m_wrapper = ModelWrapper(model, preProcess)
    # m_wrapper.saveModel("first_test_model")

    loadedModelWrapper = ModelWrapper.loadModel("first_test_model")

    print(loadedModelWrapper.model)
