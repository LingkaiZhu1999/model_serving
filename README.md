# Data-Engineering-II-Project

Data Engineering II, project 3

# Fetch data

To use the fetch_data.py script, first set an environment variable "token" with your GitHub developer api key

# How to use ModelWrapper
The modelwrapper class is used to save a model along with its feature selection and scaling process, use it like: model_process = ModelWrapper(MODEL, FEATURE_SELECTION_FUNCTION, SCALER)

Then you can save the model in a standard way no matter what the model was in the first place. Method for this is .save("DIRECTORY_NAME") where the directory name is what the model directory will be called.

To load a model, use the following syntax:
model_process = ModelWrapper.loadModel("DIRECTORY_NAME"). Where directory name is the name of the model directory

# Flask fron-end
To start the front-end server, run the app.py file, needed html files for this application resides in the templates folder



