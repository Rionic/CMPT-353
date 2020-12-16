import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from skimage.color import rgb2lab
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

df = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

y = df.city.values
X = df.iloc[:,2:].values
X2 = df2.iloc[:,2:].values
X_train, X_valid, y_train, y_valid = train_test_split(X, y)
model = make_pipeline(StandardScaler(), SVC())
model.fit(X_train, y_train)
print(model.score(X_valid, y_valid))
predictions = model.predict(X2)
pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)
