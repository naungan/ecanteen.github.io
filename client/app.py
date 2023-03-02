from flask import Flask, render_template, request, redirect, url_for
import json, requests
from werkzeug.utils import secure_filename
import base64
from base64 import encodebytes

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html");

@app.route("/add")
def add():
	return render_template("add.html")

@app.route("/product/<int:id>", methods = ["GET"])
def prouctbyid(id):
	productid = id
	alamatserver = "https://naunganku.com/ecanteen/ecanteen/{}".format(id)
	datas = requests.get(alamatserver)
	rows = json.loads(datas.text)
	return rows

@app.route("/product/all", methods = ["GET"])
def prouctall():
	alamatserver = "https://naunganku.com/ecanteen/ecanteen/all"
	datas = requests.get(alamatserver)
	rows = json.loads(datas.text)
	return rows

@app.route("/view")
def view():
	alamatserver = "https://naunganku.com/ecanteen/ecanteen"
	datas = requests.get(alamatserver)
	rows = json.loads(datas.text)
	return render_template("view.html",rows = rows)

@app.route("/delete")
def delete():
	return render_template("delete.html")

@app.route("/update")
def update():
	return render_template("update_product.html")

@app.route("/savedetails",methods = ["POST"])
def saveDetails():
	msg = "asyu"
	fname = request.form["name"]
	fprice = request.form["price"]
	fquantity = request.form["quantity"]
	fcategory = request.form["category"]
	fileobj = request.files["image"]

	file_extensions =  ["JPG","JPEG","PNG","JPE","JFIF"]
	uploaded_file_extension = fileobj.filename.split(".")[1]

	data = fileobj.stream.read()
	hasil = base64.b64encode(data)
	hasil = hasil.decode()
	print("upload image ready!")

		#b64_string = base64.b64encode(fileobj.read())
		#fileobj = str(b64_string)
		#print(fileobj)

	
	dataproduct = {
	"name" : fname,
	"price" : fprice, 
	"quantity" : fquantity,
	"category" : fcategory,
	"image" : hasil
	}

	dataproduct_json = json.dumps(dataproduct)
	alamatserver = "https://naunganku.com/ecanteen/ecanteen/"
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	kirimdata = requests.post(alamatserver, data=dataproduct_json, headers=headers)
	msg = "Product Successfully Added"
	#return render_template("success.html",msg = msg)
	return render_template("success.html",msg = msg)

@app.route("/deleterecord",methods = ["GET","POST"])
def deleterecord():
	msg = "msg"
	if request.method=="GET":
		return render_template("delete_record.html",msg = msg)
	elif request.method == "POST":
		try:
			fid = request.form["id"]
			dataproduct = {"id" : fid}
			dataproduct_json = json.dumps(dataproduct)
			alamatserver = "https://naunganku.com/ecanteen/ecanteen"
			headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
			kirimdata = requests.delete(alamatserver, data=dataproduct_json, headers=headers)
			msg = "sudah"
			return render_template("delete_record.html",msg = msg)
		except:
			msg = "sorry, error occured"
			print("except del")
		finally:
			print("finally del")
			return render_template("delete_record.html",msg = msg)
	else:
		print("else del")
		return render_template("delete_record.html",msg = msg)

@app.route("/updaterecord",methods = ["GET","POST"])
def updaterecord():
	msg = "asyu"
	fid = request.form["id"]
	fname = request.form["name"]
	fprice = request.form["price"]
	fquantity = request.form["quantity"]
	fcategory = request.form["category"]
	fileobj = request.files["image"]

	file_extensions =  ["JPG","JPEG","PNG","JPE","JFIF"]
	uploaded_file_extension = fileobj.filename.split(".")[1]

	data = fileobj.stream.read()
	hasil = base64.b64encode(data)
	hasil = hasil.decode()

		#b64_string = base64.b64encode(fileobj.read())
		#fileobj = str(b64_string)
		#print(fileobj)

	
	dataproduct = {
	"id" : fid,
	"name" : fname,
	"price" : fprice, 
	"quantity" : fquantity,
	"category" : fcategory,
	"image" : hasil
	}

	dataproduct_json = json.dumps(dataproduct)
	alamatserver = "https://naunganku.com/ecanteen/ecanteen/"
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	kirimdata = requests.put(alamatserver, data=dataproduct_json, headers=headers)
	msg = "Product Successfully Updated"
	#return render_template("success.html",msg = msg)
	return render_template("success.html",msg = msg)

if __name__ == "__main__":  
    app.run(
    	host = '0.0.0.0',
        debug = 'True',
        port = 5000
    	) 