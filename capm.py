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

#lectura de los archivos del directorio WIKI
files = pd.Series(os.listdir('WIKI'))
wheat = pd.read_csv('data/cleanwheat.csv')
oil = pd.read_csv('data/OIL_WTI.csv')

#Definicion de index
wheati = wheat.set_index('Date')
oili = oil.set_index('Date')
#definicios de columana para oil
oili.columns = ['Oil']
#extraccion de columna price
wheati = wheati['Price']
#define un nombre para trigo
wheati.name = 'Wheat'

#lecutra de datos de bolsa de new work
sp = pd.read_csv('data/NYSE_SPY.csv')
#defini index a date
spi = sp.set_index('Date')
#extrae columna Open
spopen = spi['Open']
#define nombre
spopen.name = 'spopen'
years = 6.07
rf = 0.00384

def getLinearCoefficients(a1,a2,a3,y):
	# union de todos los datos Trigo, Oil, spopen, Asset con panda
	alldata = pd.concat([a1, a2, a3 ,y ], axis = 1, join = "inner" ).dropna()
	# union de Oil y Trigo con panda
	data = pd.concat([alldata['Oil'],alldata['Wheat']],axis=1,join="inner")
	# extraccion de Asset para serie
	target = pd.Series(alldata['Asset'])
	#instancia de LinearRegression
	lin = LinearRegression()
	ax = lin.fit(data.as_matrix(),target.as_matrix())

	#extraccion del primer dato de sopoen
	rows = alldata['spopen'].shape[0]

	#instancia de lista
	spindex = list()
	for i in range(0,rows-1):
		#esteblece index para spopen
		spindex.append((alldata['spopen'][i+1]-alldata['spopen'][i])/alldata['spopen'][i])

	Assetindex = list()
	for i in range(0,rows-1):
		#esteblece index para Asset
		Assetindex.append((alldata['Asset'][i+1]-alldata['Asset'][i])/alldata['Asset'][i])
	#diferencia de sopen del minimo y maximo
	dif = alldata['spopen'][0]-alldata['spopen'][rows-1]
	#Modelo de valoracion de activos financieros
	rm = (dif/years)/alldata['spopen'][rows-1]
	rho = np.cov(spindex, Assetindex, ddof = 0)[0][1]
	beta = rho/np.var(spindex)
	ra = rf + beta*(rm -rf)
	betara = list(ax.coef_) + [beta,ra]
	return betara

allrelations = pd.DataFrame(columns=['File','Oil','Wheat','Beta', 'Return'])
for i, row in files.iteritems():
	#lectura de los archivos de precios
	ff = pd.read_csv('WIKI/'+row)
	#definicion de index a date
	ff = ff.set_index('Date')
	#extraccion de precio alto
	newf = ff['High']
	#definicion de nombre Asset
	newf.name = 'Asset'
	#llamada al metodo para generar el coeficiente
	mlcoef = getLinearCoefficients(wheati,oili,spopen,newf)
	print(i,row,mlcoef)
	allrelations = allrelations.append({'File': row,'Oil' : mlcoef[0], 'Wheat' : mlcoef[1], 'Beta' : mlcoef[2], 'Return' : mlcoef[3]}, ignore_index=True)

allrelations.to_csv('result/allregressions.csv')
