#//////////////////////////////////////////////////////////////////////////



from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, abort, flash, jsonify
import json, requests
from werkzeug.utils import secure_filename
import base64
from base64 import encodebytes
from datetime import timedelta



app = Flask(__name__)
app.secret_key = "secretkey"



#REQUEST-FROM-OUTSIDE
#//////////////////////////////////////////////////////////////////////////
##//////////////////////////////////////////////////////////////////////////
##//////////////////////////////////////////////////////////////////////////


@app.route("/product/all", methods = ["GET"])
def prouctall():
	alamatserver = "http://localhost:5055/ecanteen/getproduct/"
	head = request.headers.get('apikey')
	datajson={}
	headers = {'Content-Type':'application/json', 'Accept':'text/plain', 'apikey':"{}".format(head)}
	data_json = json.dumps(datajson)
	datas = requests.get(alamatserver, data=data_json, headers=headers)
	rows = json.loads(datas.text)
	print("product/all")
	return rows

@app.route("/product/<int:prodid>", methods = ["GET"])
def prouctbyid(prodid):
	productid = prodid
	datajson={'prodid': productid}
	data_json = json.dumps(datajson)

	head = request.headers.get('apikey')
	alamatserver = "http://localhost:5055/ecanteen/product/"
	headers = {'Content-Type':'application/json', 'Accept':'text/plain', 'apikey':"{}".format(head)}

	datas = requests.get(alamatserver, data=data_json, headers=headers)
	rows = json.loads(datas.text)
	return rows

@app.route("/product/<string:user_id>", methods = ["GET"])
def prouctbyuser(user_id):
	user = user_id

	datajson={'user_id': user}
	data_json = json.dumps(datajson)

	head = request.headers.get('apikey')
	alamatserver = "http://localhost:5055/ecanteen/productbyuser/"
	headers = {'Content-Type':'application/json', 'Accept':'text/plain', 'apikey':"{}".format(head)}
	

	datas = requests.get(alamatserver, data=data_json, headers=headers)
	rows = json.loads(datas.text)
	return rows


#//////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////
##//////////////////////////////////////////////////////////////////////////


#GET-API-KEY
#//////////////////////////////////////////////////////////////////////////

@app.route("/apikey")
def apikey():
	try :
		alamatserver = "http://localhost:5055/ecanteen/apikey"
		datajson={}
		headers = {'Content-Type':'application/json', 'Accept':'text/plain', 'getapikey':'ineedapikey'}
		data_json = json.dumps(datajson)
		kirimdata = requests.get(alamatserver, data=data_json, headers=headers)
		print("sudah mau dapet apikey")
		rows = json.loads(kirimdata.text)
		return jsonify(rows)
	
	except KeyError:
		print("KeyError at apikey")
		return redirect(url_for("login"))


@app.route('/guide')
def guide():
	return render_template("guide.html")


#AUTH-USER-SESSION
#//////////////////////////////////////////////////////////////////////////

def auth_user(user):
	session['logged_in'] = True
	session['user_id'] = users.id
	session['username'] = users.username
	#flash('You are logged in as %s' % (users.username))

# get the user from the session
def get_current_user():
	if session.get('logged_in'):
		return session['username']


#REGISTER/JOIN
#//////////////////////////////////////////////////////////////////////////

@app.route('/join', methods=['GET', 'POST'])
def join():
	if request.method == 'POST' and request.form['username']:
		zusername = request.form['username']
		#zemail = request.form['email']
		zpassword = request.form['password']

		datajoin = {
		"username" : zusername,
		#"email" : zemail,
		"password" : zpassword
		}

		datajoin_json = json.dumps(datajoin)
		alamatserver = "http://localhost:5055/ecanteen/loginauth"
		headers = {'Content-Type':'application/json', 'Accept':'text/plain', 'apikey':'itsnotapikey'}
		kirimdata = requests.post(alamatserver, data=datajoin_json, headers=headers)
		return render_template("login.html")

	return render_template("join.html")


#LOGIN
#//////////////////////////////////////////////////////////////////////////

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		zusername = request.form['username']
		zpassword = request.form['password']

		datalogin = {
		"username" : zusername,
		"password" : zpassword
		}

		datalogin_json = json.dumps(datalogin)
		alamatserver = "http://localhost:5055/ecanteen/loginauth"
		headers = {'Content-Type':'application/json', 'Accept':'text/plain', 'apikey':'itsnotapikey'}
		kirimdata = requests.get(alamatserver, data=datalogin_json, headers=headers)
		cow = json.loads(kirimdata.text)
		print(cow)

		# Save the form data to the session object
		if cow=="berhasil":
			print("iniclientberhasil")
			session['username'] = zusername
			print(session['username'])
			return redirect(url_for('login'))
			#return "<p>ini berhasil</p>"
		
		if cow=="gagal":
			print("iniclientgagal")
			return "<p>ini gagal</p>"
			"""
			session['email'] = request.form['email_address']
			return redirect(url_for('get_email'))
			"""

	return render_template("login.html")


#LOGOUT
#//////////////////////////////////////////////////////////////////////////

@app.route('/logout')
def logout():
	# Clear the email stored in the session object
	session.pop('username', default=None)
	return render_template("login.html")


#INDEX-HOME
#//////////////////////////////////////////////////////////////////////////

@app.route("/")
def index():
	return render_template("homepage.html")


#ADD-PRODUCT
#//////////////////////////////////////////////////////////////////////////

@app.route("/add", methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		usernow = session['username']
		print(usernow)

		fname = request.form["name"]
		fdesc = request.form["desc"]
		fprice = request.form["price"]
		fquantity = request.form["quantity"]
		fcategory = request.form["category"]
		fileobj = request.files["image"]

		file_extensions =  ["JPG","JPEG","PNG","JPE","JFIF"]
		uploaded_file_extension = fileobj.filename.split(".")[1]

		data = fileobj.stream.read()
		hasil = base64.b64encode(data)
		hasil = hasil.decode()

		dataproduct = {
		"user_id" : usernow,
		"desc" : fdesc,
		"name" : fname,
		"price" : fprice, 
		"quantity" : fquantity,
		"category" : fcategory,
		"image" : hasil
		}

		dataproduct_json = json.dumps(dataproduct)
		alamatserver = "http://localhost:5055/ecanteen/"
		headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
		kirimdata = requests.post(alamatserver, data=dataproduct_json, headers=headers)
		return redirect(url_for("view"))
	else:
		return render_template("add.html")


#VIEW-ALL-PRODUCT-IN-DATABASE
#//////////////////////////////////////////////////////////////////////////

@app.route("/viewall")
def viewall():
	alamatserver = "http://localhost:5055/ecanteen"
	datas = requests.get(alamatserver)
	rows = json.loads(datas.text)
	return render_template("viewall.html",rows = rows)


#VIEW-USER-PRODUCT
#//////////////////////////////////////////////////////////////////////////

@app.route("/view")
def view():
	try :
		currentuser = session['username']
		datauser = {"username" : currentuser}	
		alamatserver = "http://localhost:5055/ecanteen/myproduct"
		
		headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
		datauser_json = json.dumps(datauser)
		kirimdata = requests.get(alamatserver, data=datauser_json, headers=headers)
		rows = json.loads(kirimdata.text)
		return render_template("view.html", rows=rows)
	
	except KeyError:
		print("KeyError at View")
		return redirect(url_for("login"))


#UPDATE-SELECTED-PRODUCT
#//////////////////////////////////////////////////////////////////////////

@app.route("/update" ,methods = ["GET","POST"])
def update():
	if request.method == "POST":
		userid = request.form["user_id"]
		prodid = request.form["id"]
		prodname = request.form["name"]
		prodprice = request.form["price"]
		prodquan = request.form["quantity"]
		prodcateg = request.form["category"]
		proddesc = request.form["desc"]

	
		return render_template("update_product.html", 
			userid=userid,
			proddesc=proddesc,
			prodid=prodid,
			prodname=prodname,
			prodprice=prodprice,
			prodquan= prodquan,
			prodcateg=prodcateg
			)

	else:
		return render_template("update_product.html")


#UPDATE-OK
#//////////////////////////////////////////////////////////////////////////

@app.route("/updaterecord",methods = ["GET","POST"])
def updaterecord():
	if request.method == "POST":
		try:
			fuser = request.form["user_id"]
			print(fuser)
			fid = request.form["id"]
			print(fid)
			print("gg")
			sesuser = session['username']
			if(fuser == sesuser):
				print("if user update ses")

				fid = request.form["id"]
				fdesc = request.form["desc"]
				fname = request.form["name"]
				fprice = request.form["price"]
				fquantity = request.form["quantity"]
				fcategory = request.form["category"]

				dataproduct = {
				"id" : fid,
				"desc" : fdesc,
				"name" : fname,
				"price" : fprice, 
				"quantity" : fquantity,
				"category" : fcategory,
				}

				dataproduct_json = json.dumps(dataproduct)
				alamatserver = "http://localhost:5055/ecanteen/"
				headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
				kirimdata = requests.put(alamatserver, data=dataproduct_json, headers=headers)
				msg = "Product Successfully Updated"
				#return render_template("success.html",msg = msg)
				return render_template("view.html")
		except:
			msg = "sorry, error occured"
			print("except update")
		finally:
			print("finally update")
			return redirect(url_for("view"))
	else:
		print("else update")
		return redirect(url_for("view"))


#UPDATE-IMG
#//////////////////////////////////////////////////////////////////////////

@app.route("/chimg" ,methods = ["GET","POST"])
def chimg():
	if request.method == "POST":
		prodid = request.form["id"]
		prodname = request.form["name"]
		user_id = request.form["user_id"]
		previmage = request.form["image"]
	
		return render_template("update_image.html", 
			userid=user_id, 
			prodid=prodid,
			prodname=prodname,
			previmg=previmage
			)
	else:
		return render_template("update_image.html")


#UPDATE-IMG-OK
#//////////////////////////////////////////////////////////////////////////

@app.route("/updateimage",methods = ["GET","POST"])
def updateimage():
	if request.method == "POST":
		try:
			fuser = request.form["user_id"]
			print(fuser)

			fid = request.form["id"]
			print(fid)

			sesuser = session['username']
			
			if(fuser == sesuser):
				print("if user change image")

				fileobj = request.files["image"]

				file_extensions =  ["JPG","JPEG","PNG","JPE","JFIF"]
				uploaded_file_extension = fileobj.filename.split(".")[1]

				data = fileobj.stream.read()
				hasil = base64.b64encode(data)
				hasil = hasil.decode()

				dataproduct = {"image" : hasil, "id" : fid}

				dataproduct_json = json.dumps(dataproduct)
				alamatserver = "http://localhost:5055/ecanteen/updateimg"
				headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
				kirimdata = requests.put(alamatserver, data=dataproduct_json, headers=headers)
				msg = "Product Successfully Updated"
				#return render_template("success.html",msg = msg)
				return render_template("view.html")
		except:
			msg = "sorry, error occured"
			print("except update img")
		finally:
			print("finally update img")
			return redirect(url_for("view"))
	else:
		print("else update img")
		return redirect(url_for("view"))


#DELETE-SELECTED-PRODUCT
#//////////////////////////////////////////////////////////////////////////

@app.route("/deleterecord",methods = ["GET","POST"])
def deleterecord():
	if request.method == "POST":
		try:
			fuser = request.form["user_id"]
			print(fuser)
			fid = request.form["id"]
			print(fid)
			print("gg")
			sesuser = session['username']
			if(fuser == sesuser):
				print("if user delete ses")
				dataproduct = {"id" : fid, "user_id" : fid}
				dataproduct_json = json.dumps(dataproduct)
				alamatserver = "http://localhost:5055/ecanteen"
				headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
				kirimdata = requests.delete(alamatserver, data=dataproduct_json, headers=headers)
				return render_template("view.html")
			else:
				return "<p>Not Working</p>"
		except:
			msg = "sorry, error occured"
			print("except del")
		finally:
			print("finally del")
			return redirect(url_for("view"))
	else:
		print("else del")
		return redirect(url_for("view"))


if __name__ == "__main__":  
	app.run(
		host = '0.0.0.0',
		debug = 'True',
		port = 5000
		)