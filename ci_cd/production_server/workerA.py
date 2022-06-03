from celery import Celery
from numpy import loadtxt
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras
from save_model import ModelWrapper

def load_model():
    # load json and create model
    loaded_model = ModelWrapper.loadModel("NN_model")
    return loaded_model

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task
def get_predictions(input_repo):
    model = load_model()
    prediction = model.predict(input_repo)
    return prediction

@celery.task
def get_accuracy(input_repo):
    prediction = get_predictions(input_repo)
    actual = input_repo["stargazers_count"]
    mse = np.mean((prediction - actual.values) ** 2)
    #print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
    return mse

