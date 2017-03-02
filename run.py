#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session, g, redirect, url_for, jsonify
from collections import deque
import shelve, os, pymongo, hashlib
import twitterapi

MONGO_URL = os.environ.get('MONGOHQ_URL')

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Concexion MongoDB
connection = pymongo.MongoClient(MONGO_URL)
db = connection.app61834194
collection = db.users
collection2 = db.lawyers
tipoCasos = db.Casos
#collection2.insert({'name': "Pepe", 'surname': "Garcia", 'telf': "000 000 000"})

t = [] #Lista para guardar los links
cola = deque(t) #Cola implementada con deque


nfw = twitterapi.numFollowers('CanalUGR')
nfr = twitterapi.numFriends('CanalUGR')
location = twitterapi.location('CanalUGR')

@app.route("/index", methods=['GET','POST'])
def  index():
	cola.clear()
	if request.method == 'POST':
		session.pop('user',None)
		usr = str(request.form['username'])
		pwd = str(request.form['password'])
		user = collection.find_one({'name':usr})
		h = hashlib.sha1(pwd.encode('utf-8'))
		pwdc = str(h.hexdigest())
		if user:
			if  user['password'] == pwdc:
				session['user'] = usr
				return redirect(url_for('indexloged'))
			else:
				return render_template('index.html', followers = nfw, friends = nfr)
		else:
			return render_template('index.html', followers = nfw, friends = nfr)
	else:
		return render_template('index.html', followers =
		 nfw, friends = nfr)

@app.route("/info")
def  info():
	if g.user:
		user = collection.find_one({'name':session['user']})
		pwd = user['password']
		ema = user['email']

		if len(cola) == 3:
			link3 = cola[0]
			link2 = cola[1]
			link1 = cola[2]
		elif len(cola) == 2:
			link3 = ''
			link2 = cola[0]
			link1 = cola[1]
		else:
			link3 = ''
			link2 = ''
			link1 = cola[0]

		if len(cola) == 3:
			cola.popleft()
			cola.append('Profile')
		else:
			cola.append('Profile')

		return render_template('info.html', name = session['user'], password = pwd, email = ema, link1 = link1, link2 = link2, link3 = link3)
	else:
		return redirect(url_for('index'))

@app.route("/indexloged")
def  indexloged():
	if g.user:
		if len(cola) == 3:
			cola.popleft()
			cola.append('Home')
		else:
			cola.append('Home')
		return render_template('indexloged.html', name = session['user'], followers = nfw, friends = nfr)
	else:
		return redirect(url_for('index'))

@app.route("/getLocation")
def  getLocation():
	return 	location

@app.route("/lawyers")
def  lawyers():
	if g.user:
		if len(cola) == 3:
			cola.popleft()
			cola.append('Lawyers')
		else:
			cola.append('Lawyers')
		return render_template('lawyers.html', name = session['user'])
	else:
		return redirect(url_for('index'))


@app.route("/pagination", methods=['GET'])
def  pagination():
	limit = 10 #cantidad de filas por pagina
	offset = int(request.args.get('offset','')) #número desde donde comienza la pagina
	tam = collection2.count()

	starting_id = collection2.find().sort('_id',pymongo.ASCENDING)
	last_id = starting_id[offset]['_id']

	#$gte selecciona todos los  documentos >= last_id
	datos = collection2.find({'_id':{'$gte' : last_id}}).sort('_id',pymongo.ASCENDING).limit(limit)

	output = []

	for i in datos:
		output.append({'Name': i['name'], 'Surname': i['surname'],'Telf': i['telf']})

	return jsonify({'Datos':output, 'Tam': tam})

@app.route("/news")
def  news():
	if g.user:
		if len(cola) == 3:
			cola.popleft()
			cola.append('News')
		else:
			cola.append('News')
		return render_template('news.html', name = session['user'])
	else:
		return redirect(url_for('index'))

@app.route("/getData", methods=['GET'])
def  getData():
	datos = tipoCasos.find()
	output = []

	for i in  datos:
		output.append({'name': i['name'], 'categories': i['categories'],'data': i['data']})

	return jsonify({'Datos':output})

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route("/dropsession")
def  dropsession():
	cola.clear()
	session.pop('user',None)
	return render_template('index.html', followers = nfw, friends = nfr)

@app.route("/register")
def  register():
	 return render_template('register.html')

@app.route("/removeuser")
def  removeuser():
	user = collection.find_one({'name':session['user']})
	collection.remove(user)
	return redirect(url_for('index'))

@app.route("/update", methods=['GET','POST'])
def  update():
	if request.method == 'POST':
		usr = str(request.form['username'])
		pwd = str(request.form['password'])
		ema = str(request.form['email'])
		user = collection.find_one({'name':session['user']})
		user['name'] = usr
		user['email'] = ema

		if user['password'] != pwd:
			h = hashlib.sha1(pwd.encode('utf-8'))
			pwdc = str(h.hexdigest())
			user['password'] = pwdc

		collection.save(user)
		cola.clear()
		return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))


@app.route("/registerlogin", methods=['GET','POST'])
def  registerlogin():
	if request.method == 'POST':
		usr = str(request.form['username'])
		pwd = str(request.form['password'])
		ema = str(request.form['email'])
		h = hashlib.sha1(pwd.encode('utf-8'))
		pwdc = str(h.hexdigest())
		collection.insert({'name':usr, 'password':pwdc, 'email':ema})
		cola.clear()
		return render_template('index.html', followers = nfw, friends = nfr)
	else:
		return redirect(url_for('register'))

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=False)
