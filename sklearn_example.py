import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load data
dataset_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
data = pd.read_csv(dataset_url, sep=';')

# print(data.shape)
# (1599, 12) - meaning 1599 samples and 12 features (csv columns)

# print(data.describe())
# Lists features count, mean, std, min, max, etc

# Split data into training and test sets
y = data.quality
X = data.drop('quality', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.2, 
                                                    random_state=123, 
                                                    stratify=y)
# Declare data preprocessing steps
pipeline = make_pipeline(preprocessing.StandardScaler(),
                         RandomForestRegressor(n_estimators=100,
                                               random_state=123))

# to list the tunable hyperparameters
# print(pipeline.get_params())

# Declare hyperparameters to tune
hyperparameters = { 'randomforestregressor__max_features' : [ 'sqrt', 'log2'],
                  'randomforestregressor__max_depth': [None, 5, 3, 1]}


# Tune model using cross-validation pipeline
clf = GridSearchCV(pipeline, hyperparameters, cv=10)
 
clf.fit(X_train, y_train)

# Refit on the entire training set
# No additional code needed if clf.refit == True (default is True)
 
# Evaluate model pipeline on test data
pred = clf.predict(X_test)
print( r2_score(y_test, pred) )
print( mean_squared_error(y_test, pred) )
 
# Save model for future use
joblib.dump(clf, 'models/rf_regressor.pkl')

# To load: clf2 = joblib.load('rf_regressor.pkl')