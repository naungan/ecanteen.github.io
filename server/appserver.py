import base64
import sqlite3
import json
from flask import Flask, render_template, request, url_for, redirect, flash, make_response, jsonify
from werkzeug.utils import secure_filename
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask_restful import Resource, Api, reqparse 

app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('ecanteen.db')

class BaseModel(Model):
    class Meta:
        database = db

class products(BaseModel):
	id = AutoField()
	name = TextField()
	price = IntegerField()
	quantity = IntegerField()
	category = TextField()
	image = TextField()

@app.route('/')
def masukkeindeks():
    return "Server Ready Masbro"

@app.route('/ecanteen/<int:id>')
def productbyid(id):
	zid = id
	rows = products.select().where(products.id==id)
	datas=[]

	for row in rows:
		datas.append({
			'id':row.id,
			'name':row.name,
			'price':row.price,
			'quantity':row.quantity,
			'category':row.category,
			'image':row.image
			})
	return jsonify(datas)

@app.route('/ecanteen/all')
def productall():
    rows = products.select()
    datas=[]

    for row in rows:
        datas.append({
            'id':row.id,
            'name':row.name,
            'price':row.price,
            'quantity':row.quantity,
            'category':row.category,
            'image':row.image
        })
    return jsonify(datas)

@app.route('/read')
def readdata():
    rows = products.select()    
    datas=[]

    for row in rows:
        datas.append({
            'id':row.id,
            'name':row.name,
            'price':row.price,
            'quantity':row.quantity,
            'category':row.category,
            'image':row.image
        })
    return jsonify(datas)

class product(Resource):
	def get(self):
	    rows = products.select()    
	    datas=[]

	    for row in rows:
	        datas.append({
	            'id':row.id,
	            'name':row.name,
	            'price':row.price,
	            'quantity':row.quantity,
	            'category':row.category,
	            'image':row.image
	        })
	    return jsonify(datas)

	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('name')
		parserData.add_argument('price')
		parserData.add_argument('quantity')
		parserData.add_argument('category')
		parserData.add_argument('image')

		parserAmbilData = parserData.parse_args()
		zName = parserAmbilData.get('name')
		zPrice = parserAmbilData.get('price')
		zQuantity = parserAmbilData.get('quantity')
		zCategory = parserAmbilData.get('category')
		zImage = parserAmbilData.get('image')

		saveproduct = products.create(
			name = zName,
			price = zPrice,
			quantity = zQuantity,
			category = zCategory,
			image = zImage
			)

		rows = products.select()    
		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
				})
			return jsonify(datas)

	def delete(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id')

		parserAmbilData = parserData.parse_args()
		zID = parserAmbilData.get('id') 
		product_delete = products.delete().where(products.id==zID)
		product_delete.execute()

		rows = products.select()    
		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
				})
			return jsonify(datas)

	def put(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id')
		parserData.add_argument('name')
		parserData.add_argument('price')
		parserData.add_argument('quantity')
		parserData.add_argument('category')
		parserData.add_argument('image')

		parserAmbilData = parserData.parse_args()
		zID = parserAmbilData.get('id')
		zName = parserAmbilData.get('name')
		zPrice = parserAmbilData.get('price')
		zQuantity = parserAmbilData.get('quantity')
		zCategory = parserAmbilData.get('category')
		zImage = parserAmbilData.get('image')

		qry=products.update({products.name:zName, products.price:zPrice, products.quantity:zQuantity, products.category:zCategory, products.image:zImage}).where(products.id==zID)
		qry.execute()

		rows = products.select()    
		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
				})
			return jsonify(datas)

api.add_resource(product, '/ecanteen/', endpoint="ecanteen/")

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5055
        )