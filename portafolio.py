import os
import pandas as pd
from numpy import *
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats.stats import pearsonr
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random as rd
random = rd.random

def year2day(rate):
    return (pow(1+rate,1/365)-1)

def estandar(file):
    df = pd.read_csv("WIKI/"+ file)
    cambio = (df['Close'] - df['Open'])/df['Open']
    est = np.std(cambio)
    print(np.mean(cambio))
    print(year2day(0.38))

estandar("AAL.csv")

data = pd.read_csv("result/allregressions.csv")
data = data.set_index('File')
data = pd.concat([data['Oil'],data['Wheat'], data['Beta'] ],axis=1, join='inner')

#proyeccion 3d
fig = plt.figure()
axx = fig.add_subplot(111, projection='3d')
axx.scatter(xs = data['Oil'],ys=data['Wheat'],zs=data['Beta'],c='green',s=0.1)
plt.xlabel('Oil')
plt.ylabel('Wheat')
axx.set_zlabel('Beta')

diff = list()
for i, row in data.iterrows():
    diff.append( np.linalg.norm(np.subtract([-1,-1,0] , list(row))))

diffs = pd.DataFrame(diff,index=data.index)
diffs.columns = ["dist"]
diffs = diffs.sort_values('dist')

diffs.hist(bins=50)

#proyeccion de grafica
ndif = (diffs[diffs["dist"]<1])
for i, row in ndif.iterrows():
	print(i)
	axx.scatter(xs = data['Oil'][i],ys=data['Wheat'][i],zs=data['Beta'][i],c='blue',s=10+(50-row*100))

plt.show()
