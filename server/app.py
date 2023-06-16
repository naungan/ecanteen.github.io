#//////////////////////////////////////////////////////////////////////////


import base64
import sqlite3
import json
from flask import Flask, render_template, request, url_for, redirect, flash, make_response, jsonify
from werkzeug.utils import secure_filename
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask_restful import Resource, Api, reqparse
from hashlib import md5
import datetime
from datetime import timedelta
import secrets
import time


#//////////////////////////////////////////////////////////////////////////


app = Flask(__name__)
api = Api(app)

truekey = str(secrets.token_urlsafe(16))
app.secret_key = truekey
truekey = truekey


#DATABASE-ECANTEEN
#//////////////////////////////////////////////////////////////////////////

db = SqliteDatabase('ecanteen.db')

class BaseModel(Model):
	class Meta:
		database = db

class users(BaseModel):
	username = TextField(unique=True)
	password = TextField()
	join_date = DateTimeField()

class products(BaseModel):
	id = AutoField()
	user = ForeignKeyField(users, backref='products')
	name = TextField()
	desc = TextField()
	price = IntegerField()
	quantity = IntegerField()
	category = TextField()
	image = TextField()

def create_tables():
	with db:
		db.create_tables([users, products])


#OTHER-REQUEST
#//////////////////////////////////////////////////////////////////////////

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


class productbyuser(Resource):
	def get(self):
		head = request.headers.get('apikey')
		print(request.headers)
		if head == truekey:

			parserData = reqparse.RequestParser()
			parserData.add_argument('user_id')

			parserAmbilData = parserData.parse_args()
			zuser = parserAmbilData.get('user_id')
			print(zuser)

			rows = products.select().where(products.user_id==zuser)
			datas=[]
			for row in rows:
				datas.append({
					'id':row.id,
					'name':row.name,
					'user_id':row.user_id,
					'desc':row.desc,
					'price':row.price,
					'quantity':row.quantity,
					'category':row.category,
					'image':row.image
					})
			return jsonify(datas)

			"""
			INI-TEST
			kirimdata =[]
			kirimdata.append({"berhasil":"berhasil"})
			print("get product")
			return jsonify(kirimdata)

			"""
		else:
			return jsonify('id = "Error"')

api.add_resource(productbyuser, '/ecanteen/productbyuser/', endpoint = 'productbyuser')



class product(Resource):
	def get(self):
		head = request.headers.get('apikey')
		print(request.headers)
		if head == truekey:

			parserData = reqparse.RequestParser()
			parserData.add_argument('prodid')

			parserAmbilData = parserData.parse_args()
			zprodid = parserAmbilData.get('prodid')
			print(zprodid)

			rows = products.select().where(products.id==zprodid)
			datas=[]
			for row in rows:
				datas.append({
					'id':row.id,
					'name':row.name,
					'user_id':row.user_id,
					'desc':row.desc,
					'price':row.price,
					'quantity':row.quantity,
					'category':row.category,
					'image':row.image
					})
			return jsonify(datas)

			"""
			INI-TEST
			kirimdata =[]
			kirimdata.append({"berhasil":"berhasil"})
			print("get product")
			return jsonify(kirimdata)

			"""
		else:
			return jsonify('id = "Error"')

api.add_resource(product, '/ecanteen/product/', endpoint = 'product')

#//////////////////////////////////////////////////////////////////////////

class getproduct(Resource):
	def get(self):
		head = request.headers.get('apikey')
		print(request.headers)
		if head == truekey:

			rows = products.select()
			datas=[]

			for row in rows:
				datas.append({
					'id':row.id,
					'name':row.name,
					'user_id':row.user_id,
					'desc':row.desc,
					'price':row.price,
					'quantity':row.quantity,
					'category':row.category,
					'image':row.image
					})
			return jsonify(datas)

			"""
			INI-TEST
			kirimdata =[]
			kirimdata.append({"berhasil":"berhasil"})
			print("get product")
			return jsonify(kirimdata)

			"""
		else:
			return jsonify('key = "Error"')
api.add_resource(getproduct, '/ecanteen/getproduct/', endpoint = 'getproduct')

#//////////////////////////////////////////////////////////////////////////
"""
@app.route('/read')
def readdata():
	rows = products.select()    
	datas=[]

	for row in rows:
		datas.append({
			'id':row.id,
			'name':row.name,
			'price':row.price,
			'desc':row.desc,
			'quantity':row.quantity,
			'category':row.category,
			'image':row.image
		})
	return jsonify(datas)
"""
#//////////////////////////////////////////////////////////////////////////


#GET-API-KEY
#//////////////////////////////////////////////////////////////////////////

class apikey(Resource):
	def get(self):
		head = request.headers.get('getapikey')
		print(request.headers)
		if head == "ineedapikey":
			kirimdata =[]
			kirimdata.append({'apikey':truekey})
			print("get apikey")
			return jsonify(kirimdata)
		else:
			return jsonify("key-error")
api.add_resource(apikey, '/ecanteen/apikey/', endpoint = 'apikey')


#LOGIN-AUTH
#//////////////////////////////////////////////////////////////////////////

class LoginAuth(Resource):

#REGISTER
#//////////////////////////////////////////////////////////////////////////	

	def post(self):
		head = request.headers.get('apikey')
		if head == "itsnotapikey":
			parserData = reqparse.RequestParser()
			parserData.add_argument('username')
			#parserData.add_argument('email')
			parserData.add_argument('password')

			parserAmbilData = parserData.parse_args()
			zUser = parserAmbilData.get('username')
			#zEmail = parserAmbilData.get('email')
			zPass = parserAmbilData.get('password')

			NewPass = md5(zPass.encode('utf-8')).hexdigest()

			saveuser = users.create(
				username = zUser,
				#email = zEmail,
				password = NewPass,
				join_date = datetime.datetime.now()
				)

			rows = users.select().where(users.username==zUser)
			return jsonify(rows)
		else:
			return jsonify("join not ok")


#LOGIN-USER
#//////////////////////////////////////////////////////////////////////////

	def get(self):
		head = request.headers.get('apikey')
		if head == "itsnotapikey":
			print(request.headers)
			parserData = reqparse.RequestParser()
			parserData.add_argument('username')
			parserData.add_argument('password')

			parserAmbilData = parserData.parse_args()
			zUser = parserAmbilData.get('username')
			zPass = parserAmbilData.get('password')
			try:
				pw_hash = md5(zPass.encode('utf-8')).hexdigest()
				ihuser = users.get((users.username == zUser) & (users.password == pw_hash))
			except users.DoesNotExist:
				print("invalid login")
				rows = "tidak berhasil login"
				return jsonify(rows)
				
			else:
				print("password valid")
				rows = "berhasil"
				return jsonify(rows)
		else:
			return jsonify("login not ok")

api.add_resource(LoginAuth, '/ecanteen/loginauth/', endpoint = 'loginauth')


#INDEX-FOR-TEST
#//////////////////////////////////////////////////////////////////////////

@app.route('/')
def masukkeindeks():
	return "Server Ready Masbro"


#USER-GET-PRIVATE-PRODUCT
#//////////////////////////////////////////////////////////////////////////

class yourproduct(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('username')

		parserAmbilData = parserData.parse_args()
		zUser = parserAmbilData.get('username')

		rows = products.select().where(products.user_id==zUser)

		kirimdata=[]
		print("MyProduct")

		for row in rows:
			kirimdata.append({
				'id':row.id,
				'user_id':row.user_id,
				'name':row.name,
				'desc':row.desc,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
			})
		return jsonify(kirimdata)

api.add_resource(yourproduct, '/ecanteen/myproduct/', endpoint = 'yourproduct')


#CRUD-PRODUCT-CLIENT
#//////////////////////////////////////////////////////////////////////////

class product(Resource):

	#VIEW-ALL-PRODUCT
	#//////////////////////////////////////////////////////////////////////////
	def get(self):
		rows = products.select()
		datas=[]

		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'desc':row.desc,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
			})
		return jsonify(datas)


	#ADD-PRODUCT
	#//////////////////////////////////////////////////////////////////////////
	
	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('user_id')
		parserData.add_argument('desc')
		parserData.add_argument('name')
		parserData.add_argument('price')
		parserData.add_argument('quantity')
		parserData.add_argument('category')
		parserData.add_argument('image')

		parserAmbilData = parserData.parse_args()
		zUser = parserAmbilData.get('user_id')
		zdesc = parserAmbilData.get('desc')
		zName = parserAmbilData.get('name')
		zPrice = parserAmbilData.get('price')
		zQuantity = parserAmbilData.get('quantity')
		zCategory = parserAmbilData.get('category')
		zImage = parserAmbilData.get('image')


		saveproduct = products.create(
			user_id = zUser,
			name = zName,
			desc = zdesc,
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
				'desc':row.desc,
				'user_id':row.user_id,
				'name':row.name,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
				})
			return jsonify(datas)

	#DELETE-PRODUCT
	#//////////////////////////////////////////////////////////////////////////

	def delete(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id')
		parserData.add_argument('user_id')

		parserAmbilData = parserData.parse_args()
		zID = parserAmbilData.get('id')
		userID = parserAmbilData.get('user_id')
		product_delete = products.delete().where(products.id==zID)
		product_delete.execute()

		rows = products.select()    
		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'desc':row.desc,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
				})
			return jsonify(datas)


	#UPDATE-PRODUCT
	#//////////////////////////////////////////////////////////////////////////

	def put(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id')
		parserData.add_argument('desc')
		parserData.add_argument('name')
		parserData.add_argument('price')
		parserData.add_argument('quantity')
		parserData.add_argument('category')

		parserAmbilData = parserData.parse_args()
		zID = parserAmbilData.get('id')
		zdesc = parserAmbilData.get('desc')
		zName = parserAmbilData.get('name')
		zPrice = parserAmbilData.get('price')
		zQuantity = parserAmbilData.get('quantity')
		zCategory = parserAmbilData.get('category')

		qry=products.update({products.name:zName, products.price:zPrice, products.quantity:zQuantity, products.category:zCategory, products.desc:zdesc}).where(products.id==zID)
		qry.execute()

		rows = products.select()    
		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'desc':row.desc,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
				})
			return jsonify(datas)

api.add_resource(product, '/ecanteen/', endpoint="ecanteen")


#UPDATE-SELECTED-PRODUCT-IMAGE
#//////////////////////////////////////////////////////////////////////////
class updateimg(Resource):
	def put(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('image')
		parserData.add_argument('id')

		parserAmbilData = parserData.parse_args()
		zimg = parserAmbilData.get('image')
		zid = parserAmbilData.get('id')

		qry=products.update({products.image:zimg}).where(products.id==zid)
		qry.execute()

		print("updateimg")

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

api.add_resource(updateimg, '/ecanteen/updateimg/', endpoint = 'updateimg')

if __name__ == '__main__':
	create_tables()
	app.run(
		host = '0.0.0.0',
		debug = 'True',
		port=5055
		)