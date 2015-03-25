# FarmInv controller
#debugger
import pdb

#imports
from functools import wraps
from flask import Flask, render_template, request, session, flash, redirect, url_for 
from flask.ext.sqlalchemy import SQLAlchemy
import config
from forms import AddTaskForm, RegisterForm, LoginForm, SearchDateForm

import datetime

#COnfiguration
app = Flask(__name__)
#pulls configuration from file
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Entry, Broiler, Layer, Pig, User

####OLD CODE

#configuation
#DATABASE = 'farmInv.db'
#USERNAME = 'admin'
#PASSWORD = 'admin'
#SECRET_KEY = '90fd909a93'

#pulls in app configuation by looking for UPPERCASE variable
#app.config.from_object(__name__)

####END OLD CODE




#####no longer needed
#import sqlite3
#function for connection to the DATABASE
#def connect_db():
	#return sqlite3.connect(app.config['DATABASE'])
#####End No Longer Needed

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			u = User.query.filter_by(
				name=request.form['name'],
				password=request.form['password']
				).first()
			if u is None:
				error = 'Invalid username or passowrd.'
				return render_template("login.html", form=form, error=error)
			else:
				session['logged_in'] = True
				flash('Your are logged in. Go Crazy.')
				return redirect(url_for('main'))
		else:
			return render_template("login.html", form=form, error=error)

	if request.method == 'GET':
			return render_template('login.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = AddTaskForm(request.form)
	#pdb.set_trace()
	if request.method == 'POST':
		if form.validate_on_submit():
			new_entry = Entry(
				form.entryDate.data,
				form.batch.data,
				form.action.data,
				form.actionNo.data,
				form.value.data,
				form.notes.data)
			## TEMPORARY SKIP
			db.session.add(new_entry)
			db.session.commit()

	###OLD CODE
			entryDate = form.entryDate.data
			batch = form.batch.data
			action = form.action.data
			actionNo = form.actionNo.data
			value = form.value.data
			notes = form.notes.data
			
			#dbTable = batch[:-3]
			#pdb.set_trace()
			if ("Sheep" or "Duck") in batch:
				flash('New entry was successfully posted!')
				return redirect(url_for('main'))

			#start new code
			if action == "Purchase":
				cvpb = value / actionNo
				#batch_detail = [batch, entryDate, actionNo, cvpb, 0, 0, 0, 0, 0, 0, value]
				if "Broiler" in batch:
					create_broiler = Broiler(batch, entryDate, actionNo, float(cvpb), 0, 0, 0, 0.0, 0.0, 0.0, float(value))
					db.session.add(create_broiler)
				elif "Layer" in batch:
					create_layer = Layer(batch, entryDate, actionNo, float(cvpb), 0, 0, 0, 0.0, 0.0, 0.0, float(value))
					db.session.add(create_layer)
				elif "Pig" in batch:
					create_pig = Broiler(batch, entryDate, actionNo, float(cvpb), 0, 0, 0, 0.0, 0.0, 0.0, float(value))
					db.session.add(create_pig)
					
				db.session.commit()
				flash('New entry was successfully posted!')
				return redirect(url_for('main'))
			else:
				if "Broiler" in batch:
					#pdb.set_trace()
					table = Broiler
					record = db.session.query(Broiler).filter_by(batch=batch).first()
				elif "Layer" in batch:
					table = Layer
					record = db.session.query(Layer).filter_by(batch=batch).first()
				elif "Pig" in batch:
					table = Pig
					record = db.session.query(Pig).filter_by(batch=batch).first()

				#ogAlive = ogData[2]
				#ogCVPB = ogData[3]
				#ogSlaughtered = ogData[4]
				#ogSold = ogData[5]
				#ogDead = ogData[6]
				#ogFeed = ogData[7]
				#ogTime = ogData[8]
				#ogSales = ogData[9]
				#ogExp = ogData[10]
				#flag = False					

			if action == "Dead" or action == "Lost":
				#update Dead data for batch, but data from animals table or form will be negative
				newVal = int(record.dead) - int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"dead": newVal})
				alive = int(record.alive) + int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"alive": alive})

			#may need to use str(action)
			elif "Slaughter" in action:
				#update slaughtered data
				#pdb.set_trace()
				newVal = int(record.special) - int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"special": newVal})
				
				alive = int(record.alive) + int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"alive": alive})
										
				newVal2 = float(record.sales) + float(value)
				db.session.query(table).filter_by(batch=batch).update({"sales": newVal2})
				
			elif action == "Tray":
				#pdb.set_trace()
				newVal = int(record.special) + int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"special": newVal})
				
				newVal2 = float(record.sales) + float(value)
				db.session.query(table).filter_by(batch=batch).update({"sales": newVal2})

			elif action == "Sold":
				newVal = int(record.sold) - int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"sold": newVal})
				
				newVal2 = float(record.sales) + float(value)
				db.session.query(table).filter_by(batch=batch).update({"sales": newVal2})

				alive = int(record.alive) + int(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"alive": alive})

			elif action == "Feed":
				newVal = float(record.feed) + float(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"feed": newVal})
				
				newVal2 = float(record.exp) + float(value)
				db.session.query(table).filter_by(batch=batch).update({"exp": newVal2})
				

			elif action == "Time":
				newVal = float(record.time) + float(actionNo)
				db.session.query(table).filter_by(batch=batch).update({"time": newVal})
				
				newVal2 = float(record.exp) + float(value)
				db.session.query(table).filter_by(batch=batch).update({"exp": newVal2})


			#End new code
			db.session.commit()
			flash('New entry was successfully posted!')
		return redirect(url_for('main'))

	####////OLD CODE

#USer Registartation
@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				form.name.data,
				form.email.data,
				form.password.data)
			db.session.add(new_user)
			db.session.commit()
			flash('Thanks for registering. Please Login.')
			return redirect(url_for('login'))
		else:
			return render_template('register.html', form=form, error=error)
	if request.method == 'GET':
		return render_template('register.html', form=form)
		
@app.route('/report', methods=['GET','POST'])
@login_required
def report():
	error = None
	form=SearchDateForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			startDate = form.startDate.data
			endDate = form.endDate.data
			posts = db.session.query(Entry).filter(Entry.entryDate.between(startDate, endDate)).order_by(Entry.entryDate.desc())

			#get summary data
			#layerTray = db.session.query(Entry).func.sum(Entry.special).label('trays')
			#pdb.set_trace()

			# Meat Shop
			tray1 = 0
			trayValue1 = 0
			broilerSlaughter1 = 0
			broilerValue1 = 0
			pigSlaughter1 = 0
			pigValue1 = 0
			sheepSlaughter1 = 0
			sheepValue1 = 0
			duckSlaughter1 = 0
			duckTray1 = 0
			duckValue1 = 0

			tray2 = 0
			trayValue2 = 0
			broilerSlaughter2 = 0
			broilerValue2 = 0
			pigSlaughter2 = 0
			pigValue2 = 0
			sheepSlaughter2 = 0
			sheepValue2 = 0
			duckSlaughter2 = 0
			duckTray2 = 0
			duckValue2 = 0

			for post in posts:
				if "Layer" in post.batch and post.action == "Tray":
					if "MS" in post.notes:
						tray1 = tray1 + post.actionNo
						trayValue1 = trayValue1 + post.value
					else:
						tray2 = tray2 + post.actionNo
						trayValue2 = trayValue2 + post.value
				if "Broiler" in post.batch and "Slaughter" in post.action:
					broilerSlaughter1 = broilerSlaughter1 + (post.actionNo * -1)
					broilerValue1 = broilerValue1 + post.value
				if "Pig" in post.batch and post.action == "Slaughter":
					pigSlaughter1 = pigSlaughter1 + (post.actionNo *-1)
					pigValue1 = pigValue1 + post.value
				if "Sheep" in post.batch and post.action == "Slaughter":
					sheepSlaughter1 = sheepSlaughter1 + (post.actionNo *-1)
					sheepValue1 = sheepValue1 + post.value
				if "Duck" in post.batch and post.action == "Slaughter":
					duckSlaughter1 = duckSlaughter1 + (post.actionNo * -1)
					duckValue1 = duckValue1 + post.value
				if "Duck" in post.batch and post.action == "Tray":
					duckTray1 =	duckTray1 + post.actionNo
					duckValue1 = duckValue1 + post.value 

			totalValue1 = trayValue1 + broilerValue1 + pigValue1 + sheepValue1 + duckValue1
			meatShop = [tray1, trayValue1, broilerSlaughter1, broilerValue1, pigSlaughter1, pigValue1, sheepSlaughter1, sheepValue1, duckSlaughter1, duckTray1, duckValue1, totalValue1]
			flash('Report betweeen ' + startDate + ' and ' + endDate)
			return render_template('report.html', form=form, posts=posts, meat_shop=meatShop)

		else:
			return render_template('report.html', form=form, error=error)
	
	if request.method == 'GET':
		startDate = (datetime.date.today() - datetime.timedelta(1*365/12)).isoformat()
		endDate = datetime.date.today()
		posts = db.session.query(Entry).filter(Entry.entryDate.between(startDate, endDate))

		# Meat Shop
		tray1 = 0
		trayValue1 = 0
		broilerSlaughter1 = 0
		broilerValue1 = 0
		pigSlaughter1 = 0
		pigValue1 = 0
		sheepSlaughter1 = 0
		sheepValue1 = 0
		duckSlaughter1 = 0
		duckTray1 = 0
		duckValue1 = 0

		tray2 = 0
		trayValue2 = 0
		broilerSlaughter2 = 0
		broilerValue2 = 0
		pigSlaughter2 = 0
		pigValue2 = 0
		sheepSlaughter2 = 0
		sheepValue2 = 0
		duckSlaughter2 = 0
		duckTray2 = 0
		duckValue2 = 0

		for post in posts:
			if "Layer" in post.batch and post.action == "Tray":
				if "MS" in post.notes:
					tray1 = tray1 + post.actionNo
					trayValue1 = trayValue1 + post.value
				else:
					tray2 = tray2 + post.actionNo
					trayValue2 = trayValue2 + post.value
			if "Broiler" in post.batch and "Slaughter" in post.action:
				broilerSlaughter1 = broilerSlaughter1 + (post.actionNo * -1)
				broilerValue1 = broilerValue1 + post.value
			if "Pig" in post.batch and post.action == "Slaughter":
				pigSlaughter1 = pigSlaughter1 + (post.actionNo *-1)
				pigValue1 = pigValue1 + post.value
			if "Sheep" in post.batch and post.action == "Slaughter":
				sheepSlaughter1 = sheepSlaughter1 + (post.actionNo *-1)
				sheepValue1 = sheepValue1 + post.value
			if "Duck" in post.batch and post.action == "Slaughter":
				duckSlaughter1 = duckSlaughter1 + (post.actionNo * -1)
				duckValue1 = duckValue1 + post.value
			if "Duck" in post.batch and post.action == "Tray":
				duckTray1 =	duckTray1 + post.actionNo
				duckValue1 = duckValue1 + post.value 

		totalValue1 = trayValue1 + broilerValue1 + pigValue1 + sheepValue1 + duckValue1
		meatShop = [tray1, trayValue1, broilerSlaughter1, broilerValue1, pigSlaughter1, pigValue1, sheepSlaughter1, sheepValue1, duckSlaughter1, duckTray1, duckValue1, totalValue1]

		return render_template('report.html', form=form, posts=posts, meat_shop=meatShop)


@app.route('/main')
@login_required
def main():
	posts = db.session.query(Entry).order_by(Entry.entryDate.desc())
	return render_template('main.html', form = AddTaskForm(request.form), posts=posts)



if __name__ == '__main__':
	app.run(debug=True)

