import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras import layers
from tensorflow.keras import activations


class StarPrediction:
    def __init__(self):
        super().__init__()
        data_frame = pd.read_csv("data1000")
        X = data_frame[
            ["has_issues", "has_projects", "has_downloads", "has_wiki", "has_pages", "forks_count", "watchers_count",
             "archived", "disabled", "open_issues_count", "allow_forking", "is_template", "forks",
             "open_issues", "score"]]
        Y = data_frame[["stargazers_count"]]

        data_frame = data_frame[data_frame['watchers_count'].notna()]
        data_frame = data_frame[data_frame['has_issues'].notna()]
        data_frame = data_frame[data_frame['has_projects'].notna()]
        data_frame = data_frame[data_frame['has_downloads'].notna()]
        data_frame = data_frame[data_frame['has_wiki'].notna()]
        data_frame = data_frame[data_frame['has_pages'].notna()]
        data_frame = data_frame[data_frame['forks_count'].notna()]
        data_frame = data_frame[data_frame['archived'].notna()]
        data_frame = data_frame[data_frame['disabled'].notna()]
        data_frame = data_frame[data_frame['open_issues_count'].notna()]
        data_frame = data_frame[data_frame['allow_forking'].notna()]
        data_frame = data_frame[data_frame['is_template'].notna()]
        data_frame = data_frame[data_frame['forks'].notna()]
        data_frame = data_frame[data_frame['open_issues'].notna()]
        data_frame = data_frame[data_frame['score'].notna()]

        X["has_issues"] = X["has_issues"].astype(np.float32)
        X["has_projects"] = X["has_projects"].astype(np.float32)
        X["has_downloads"] = X["has_downloads"].astype(np.float32)
        X["has_wiki"] = X["has_wiki"].astype(np.float32)
        X["is_template"] = X["is_template"].astype(np.float32)
        X["has_pages"] = X["has_pages"].astype(np.float32)
        X["archived"] = X["archived"].astype(np.float32)
        X["disabled"] = X["disabled"].astype(np.float32)
        X["allow_forking"] = X["allow_forking"].astype(np.float32)

        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=None, shuffle=True)
        input_dimension = x_train.shape[1]

        model = Sequential()
        model.add(layers.Dense(4, activation=activations.relu))
        # model.add(Dense(units=5, kernel_initializer='normal', activation='tanh'))
        model.add(Dense(1, kernel_initializer='normal'))

        # Adam optimization is a stochastic gradient descent method that is based on
        # adaptive estimation of first-order and second-order moments.
        model.compile(loss='mean_squared_error', optimizer='adam')
        # Fitting the ANN to the Training set
        model.fit(x_train, y_train, batch_size=500, epochs=10000, verbose=1)
        predictions = model.predict(x_test)
        mse = np.mean((predictions - y_test) ** 2)
        print(mse)


if __name__ == '__main__':
   app = StarPrediction()
