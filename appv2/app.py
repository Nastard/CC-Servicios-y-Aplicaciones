from flask import Flask, url_for, render_template, make_response
from PIL import Image
import os.path
import svgwrite
import random
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
	s = '''Prueba con:
	<ul><li>/servicio/v2/prediccion/24horas/</li>
	<li>/servicio/v2/prediccion/48horas/</li>
	<li>/servicio/v2/prediccion/72horas/</li></ul>
	'''

	return s

@app.route('/servicio/v2/prediccion/24horas/')
def pred_v1_24():
	client = MongoClient('0.0.0.0', 27017)
	db = client.practica2
	coll = db.san_francisco_ar_24.find()
	client.close()

	salida = "["
	for c in coll:
		salida = salida+"{ \"hour\": \""+str(c["hour"])+"\", \"temp\": \""+str(c["temp"])+"\", \"hum\": \""+str(c["hum"])+"\"}, "

	salida = salida[:len(salida) - 2]
	salida = salida+"]"
	return salida

@app.route('/servicio/v2/prediccion/48horas/')
def pred_v1_48():
	client = MongoClient('0.0.0.0', 27017)
	db = client.practica2
	coll = db.san_francisco_ar_48.find()
	client.close()

	salida = "["
	for c in coll:
		salida = salida+"{ \"hour\": \""+str(c["hour"])+"\", \"temp\": \""+str(c["temp"])+"\", \"hum\": \""+str(c["hum"])+"\"}, "

	salida = salida[:len(salida) - 2]
	salida = salida+"]"
	return salida

@app.route('/servicio/v2/prediccion/72horas/')
def pred_v1_72():
	client = MongoClient('0.0.0.0', 27017)
	db = client.practica2
	coll = db.san_francisco_ar_72.find()
	client.close()

	salida = "["
	for c in coll:
		salida = salida+"{ \"hour\": \""+str(c["hour"])+"\", \"temp\": \""+str(c["temp"])+"\", \"hum\": \""+str(c["hum"])+"\"}, "

	salida = salida[:len(salida) - 2]
	salida = salida+"]"
	return salida
