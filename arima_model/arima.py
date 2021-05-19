import pandas as pd
import pmdarima as pm
from pymongo import MongoClient

def model(columna, n_periods):
	model = pm.auto_arima(columna, start_p=1, start_q=1,
	                      test='adf',       # use adftest to find optimal 'd'
	                      max_p=3, max_q=3, # maximum p and q
	                      m=1,              # frequency of series
	                      d=None,           # let model determine 'd'
	                      seasonal=False,   # No Seasonality
	                      start_P=0,
	                      D=0,
	                      trace=True,
	                      error_action='ignore',
	                      suppress_warnings=True,
	                      stepwise=True)
	# fc contains the forecasting
	fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
	return fc

def insertar(db, df, n_periods, coll):
	print("Haciendo predicciones...")
	fc_temp = model(df.temperatura, n_periods)
	fc_hum = model(df.humedad, n_periods)

	nombre_coll = "san_francisco_arima_"+str(n_periods)
	if nombre_coll in db.list_collection_names():
		coll.delete_many({})

	print("Insertando...")
	hora = 0
	for i in range(n_periods):
		coll.insert_one({"hour":str(hora)+":00", "temp":fc_temp[i], "hum":fc_hum[i]})
		hora = (hora +1)%24

print("Conectandose...")
client = MongoClient('0.0.0.0', 27017)
db = client.practica2
coll = db.san_francisco.find()
df = pd.DataFrame.from_dict(coll)

insertar(db, df, 24, db.san_francisco_arima_24)
insertar(db, df, 48, db.san_francisco_arima_48)
insertar(db, df, 72, db.san_francisco_arima_72)

client.close()
print("Listo")
