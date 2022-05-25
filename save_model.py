import pickle
from typing import Any
import keras


def saveModel(model: Any, modelName: str):
    """Pickle an object, useful for saving models that lack a dedicated save method"""
    with open(f"{modelName}.pickle", "wb") as f:
        pickle.dump(model, f)


def loadModel(filename: str):
    """Load a model saved by pickle"""
    try:
        with open(filename, "rb") as f:
            model = pickle.loads(filename)
    except:
        print("Error opening file")

    return model


def loadKerasModel(filepath: str):
    """"""
    model = keras.models.load_model(filepath)
    return model
