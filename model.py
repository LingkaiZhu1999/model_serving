from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras import layers
from tensorflow.keras import activations
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os


df=pd.read_csv("updateddata.csv")
df.head()

df = df.drop(columns=["stargazers_count", "watchers_count", "watchers", "id", "full_name"])

def Support_Vector_Regression(request):
    if request.method == 'POST':
        try:
            file_name = request.POST['filename']
            my_file = "media/user_{0}/processed_csv/{1}".format(request.user, file_name)
            features = request.POST.getlist('features')
            features_list = []
            for feature in features:
                feature = feature[1:-1]
                feature = feature.strip().split(", ")
                for i in feature:
                    features_list.append(i[1:-1])
            label = request.POST['label']
            ratio = request.POST['ratio']
X_train, X_test, y_train, y_test = TestTrainSplit(my_file, features_list, label, int(ratio))
regressor.fit(X_train, y_train)
           y_pred = regressor.predict(X_test)
           result = mean_squared_error(y_test, y_pred)
           print(result)

        return render(request, 'MLS/result.html', {"model": "Support_Vector_Regression",
                                                       "metrics": "MEAN SQUARE ROOT",
                                                       "result": result})
       except Exception as e:
           return render(request, 'MLS/result.html', {"model": "Support_Vector_Regression",
                                                       "metrics": "MEAN SQUARE ROOT",
                                                       "Error": e})