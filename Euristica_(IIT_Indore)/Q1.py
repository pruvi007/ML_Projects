# -*- coding: utf-8 -*-
"""q1_euristica.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mQcrTL2Dy9sZcFeBnQWeBifYSNEz4aTD
"""

import numpy as np 
from sklearn.linear_model import LinearRegression
import pandas as pd 
from sklearn import preprocessing
from sklearn.kernel_approximation import RBFSampler

data = pd.read_csv('train_data.csv').values
Y = data[:,-1]
X = data[:,0:4]
X = preprocessing.scale(X)
rbf_feature = RBFSampler(gamma=1)
X = rbf_feature.fit_transform(X)
# print(X[1])
model = LinearRegression()
model.fit(X,Y)

data = pd.read_csv('test_data.csv').values
data = preprocessing.scale(data)
data = rbf_feature.fit_transform(data)
predictions = model.predict(data)
with open("1submission.csv", "w") as f:	
    for i in range(len(predictions)):
        f.write(str(predictions[i]))
        f.write('\n')
print(len(predictions))
print("done")