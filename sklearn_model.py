import pandas
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

# load the dataset
dataset = pandas.read_csv('training_data.csv')
# split into input (X) and output (y) variables
X = dataset.drop(columns=['stargazers_count', 'id', 'private'])
y = dataset['stargazers_count']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
decision_tree_regressor = DecisionTreeRegressor(random_state=0)
decision_tree_regressor.fit(X_train, y_train)
y_pred = decision_tree_regressor.predict(X_test)
accuracy = np.mean((y_pred-y_test)**2)
print(accuracy)
model_file_name = "decision_tree.pkl"
with open(model_file_name, 'wb') as file:
    pickle.dump(decision_tree_regressor, file)

