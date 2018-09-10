#importacion de librerias
# pip install pandas
# pip install urllib3
import pandas as pd
import urllib3

#lectura del data set
alltickers = pd.read_csv('data/WIKI-datasets-codes.csv')
#obtiene el primer columna WIKI/'name'
datasets = alltickers.ix[:,0]

#recorremos el data set
for i, row in datasets.iteritems():
	#url de descarga
	baseurl = "https://www.quandl.com/api/v3/datasets/"
	finalurl = ".csv?api_key=Y4AwT-TnxC_aybNKccqd&collapse=none"
	tickersample = row

	#instancia de urllib3
	http = urllib3.PoolManager(timeout=65)
	#lectura y extracion de archivos al directorio WIKI
	mydata = http.request('GET', baseurl+tickersample+finalurl, decode_content=True)

	#establece el nombre del archivo
	to_write = open(tickersample+".csv","w")

	#escribe el archivo .csv dentro del directorio WIKI
	to_write.write(mydata.data)
	to_write.close()
	print("success")
