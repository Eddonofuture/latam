import pandas as pd
import numpy as np
import time
import sys
import json
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

import warnings
warnings.filterwarnings('ignore')
mlflow.sklearn.autolog()
mlflow.set_experiment("Felipe Veloso")
print(mlflow.get_tracking_uri())

x_train = pd.read_csv('datasets/x_train.csv', header = None).to_numpy()
y_train = np.ravel(pd.read_csv('datasets/y_train.csv', header = None).to_numpy())
x_test = pd.read_csv('datasets/x_test.csv', header = None).to_numpy()
y_test = np.ravel(pd.read_csv('datasets/y_test.csv', header = None).to_numpy())

with mlflow.start_run():
    
    logReg = LogisticRegression(class_weight = 'balanced')
    model = logReg.fit(x_train, y_train)
    print('predict?')
    start = time.time()
    y_pred = model.predict(x_test)
    end = time.time()
    print("Tiempo en predicción:", end - start, "[s]")
    mlflow.log_param("prediction_time",  (end - start))
    # mlflow.log_param("confusion_matrix_pred", confusion_matrix(y_test, y_pred))
    mlflow.log_metric("precision_label_0_0pred", precision_score(y_test, y_pred, pos_label=0))
    mlflow.log_metric("recall_label_0_pred", recall_score(y_test, y_pred, pos_label=0))
    mlflow.log_metric("f1score_label_0_pred", f1_score(y_test, y_pred, pos_label=0))
    mlflow.log_metric("precision_label_1_pred", precision_score(y_test, y_pred, pos_label=1))
    mlflow.log_metric("recall_label_1_pred", recall_score(y_test, y_pred, pos_label=1))
    mlflow.log_metric("f1score_label_1_pred", f1_score(y_test, y_pred, pos_label=1))
    print(classification_report(y_test, y_pred))

