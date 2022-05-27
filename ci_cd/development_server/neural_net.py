# first neural network with keras tutorial
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import model_from_json
import pandas as pd
from tensorflow import keras

# load the dataset
dataset = pd.read_csv('training_data.csv')
# split into input (X) and output (y) variables
X = dataset.drop(columns=['stargazers_count', 'id', 'private'])
y = dataset['stargazers_count']

# define the keras model

#model.add(Dense(12, input_dim=8, activation='relu'))
#model.add(Dense(8, activation='relu'))
#model.add(Dense(1, activation='sigmoid')

num_input_layer = X.shape[1]
### neural networks
input = keras.Input(shape=num_input_layer)
layer = keras.layers.Dense(40, activation="relu")(input)
layer = keras.layers.Dense(100, activation="relu")(layer)
layer = keras.layers.Dropout(.03)(layer)
layer = keras.layers.Dense(10, activation="relu")(layer)
layer = keras.layers.Dense(1, activation="relu")(layer)


# compile the keras model
model = keras.models.Model(inputs=input, outputs=layer)
optimizer = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(loss="mse", optimizer=optimizer)
scaler = MinMaxScaler()
xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=.1, shuffle=True)
# fit the keras model on the dataset
model.fit(xTrain, yTrain, epochs=500, verbose=0)

# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# make class predictions with the model
predictions = loaded_model.predict_classes(X)
# summarize the first 5 cases
for i in range(5):
    print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
