# Se ha consultado el siguiente enlace, en concreto Autoregression:
# https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/

import pandas as pd
from pymongo import MongoClient
from statsmodels.tsa.ar_model import AutoReg,ar_select_order

def model(columna, n_periods):
	data = columna
	f = n_periods
	mod = ar_select_order(data.ravel(), maxlag=15, old_names=True)
	AutoRegfit = AutoReg(data, trend='c', lags=mod.ar_lags, old_names=True).fit()
	yhat = AutoRegfit.predict(start=len(data),end=len(data)+f-1,dynamic=False)
	return yhat

def insertar(db, df, n_periods, coll):
	print("Haciendo predicciones...")
	fc_temp = model(df.temperatura, n_periods)
	fc_hum = model(df.humedad, n_periods)

	nombre_coll = "san_francisco_rf_"+str(n_periods)
	if nombre_coll in db.list_collection_names():
		coll.delete_many({})

	print("Insertando...")
	hora = 0
	for t,h in zip(fc_temp, fc_hum):
		coll.insert_one({"hour":str(hora)+":00", "temp":t, "hum":h})
		hora = (hora +1)%24

print("Conectandose...")
client = MongoClient('0.0.0.0', 27017)
db = client.practica2
coll = db.san_francisco.find()
df = pd.DataFrame.from_dict(coll)

insertar(db, df, 24, db.san_francisco_rf_24)
insertar(db, df, 48, db.san_francisco_rf_48)
insertar(db, df, 72, db.san_francisco_rf_72)

client.close()
print("Listo")
