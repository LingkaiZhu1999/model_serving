import argparse
import os

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import model_from_json

import ray
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.integration.keras import TuneReportCallback

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
dataset = pd.read_csv('training_data.csv')
# split into input (X) and output (y) variables
X = dataset.drop(columns=['stargazers_count', 'id', 'private'])
y = dataset['stargazers_count']
scaler = MinMaxScaler()
X = scaler.fit_transform(X, y)

def train_github(config):
    # https://github.com/tensorflow/tensorflow/issues/32159
    import tensorflow as tf

    batch_size = 64
    num_classes = 1
    epochs = 2000
    xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=.2, shuffle=True)
    # num_input_layer = X.shape[1]
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(40, activation="relu"),
            tf.keras.layers.Dense(config["hidden"], activation="relu"),
            tf.keras.layers.Dropout(0.03),
            tf.keras.layers.Dense(10, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="relu"),
        ]
    )

    model.compile(
        loss="mse",
        optimizer=tf.keras.optimizers.Adam(learning_rate=config["lr"]),
    )
    print(config['amsgrad'])

    model.fit(
        xTrain,
        yTrain,
        batch_size=batch_size,
        epochs=epochs,
        verbose=0,
    )

    predictions = model.predict(xTest).ravel()
    accuracy = np.mean((predictions - yTest)**2)
    tune.report(accuracy=accuracy)


def tune_github(num_training_iterations):
    sched = AsyncHyperBandScheduler(
        time_attr="training_iteration", max_t=1000, grace_period=20
    )

    analysis = tune.run(
        train_github,
        name="exp",
        scheduler=sched,
        metric="accuracy",
        mode="min",
        num_samples=15,
        resources_per_trial={"cpu": 2, "gpu": 0},
        stop={ "training_iteration": num_training_iterations},
        config={
            "threads": 2,
            "lr": tune.uniform(0.001, 0.1),
            "hidden": tune.randint(100, 200),
        },
    )
    print("Best hyperparameters found were: ", analysis.best_config)


if __name__ == "__main__":
    ray.init("auto")
    print("ok")
    tune_github(num_training_iterations=500)
