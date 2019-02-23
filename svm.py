import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
# use seaborn plotting defaults
import seaborn as sns;
from sklearn.datasets.samples_generator import make_blobs
data = pd.read_csv('SVM.csv')
tf1= data['tf1'].values
tf2= data['tf2'].values
X=tf1[0]
y=tf2[0]

plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
