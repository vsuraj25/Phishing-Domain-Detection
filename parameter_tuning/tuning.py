## Importing Libraries
import pandas as pd
import numpy as np
import warnings
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
import yaml
from datetime import datetime

warnings.filterwarnings("ignore")

## Main Function for hyperparameter tuning 

def perform_rcv():
    x_train = pd.read_csv('artifacts/data_transformation/train_test_data/x_train.csv')
    x_test = pd.read_csv('artifacts/data_transformation/train_test_data/x_test.csv')
    y_train = pd.read_csv('artifacts/data_transformation/train_test_data/y_train.csv')
    y_test = pd.read_csv('artifacts/data_transformation/train_test_data/y_test.csv')

    params_path = 'parameter_tuning//param_grid.yaml'

    param_config = read_params(params_path)

    param_grid = param_config["RandomForestClassifier"]

    rcv_result = randomsearch_tuning(param_grid=param_grid, x_train=x_train, y_train=y_train, x_test=x_test,y_test=y_test )

    return rcv_result

## Custom function for RandomSearchCV and for saving best metrics and parameters 
def randomsearch_tuning(param_grid , x_train, y_train, x_test, y_test):

    hptune_result = {}

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    classifier = RandomForestClassifier()

    rcv = RandomizedSearchCV(estimator = classifier, param_distributions = param_grid, n_iter = 500, cv = 5, verbose = 2)
    rcv.fit(x_train, y_train)

    best_params = rcv.best_params_
    
    best_estimator = rcv.best_estimator_
    y_pred = best_estimator.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    rcv_result = 'parameter_tuning//rcv_result.yaml'
    
    params_and_metrics = {"best_params" : best_params, "metrics" : {"accuracy" : float(accuracy), "precision": float(precision), "recall" : float(recall)}}

    with open(rcv_result) as res:
        hptune_result = yaml.safe_load(res)
        hptune_result[timestamp] = params_and_metrics

    with open(rcv_result, 'w+') as res:
        yaml.dump(hptune_result, res)

    return hptune_result

## Reading Parameters
def read_params(params_path):
    with open(params_path) as yaml_file:
        params_config = yaml.safe_load(yaml_file)
    return params_config

## Run RCV
perform_rcv()




