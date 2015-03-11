# FarmInv controller

#imports
from functools import wraps
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
import config
from forms import AddTaskForm
#debugger
import pdb

app = Flask(__name__)
#pulls configuration from file
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Entry, Broiler, Layer, Pig

####OLD CODE

#configuation
#DATABASE = 'farmInv.db'
#USERNAME = 'admin'
#PASSWORD = 'admin'
#SECRET_KEY = '90fd909a93'

#pulls in app configuation by looking for UPPERCASE variable
#app.config.from_object(__name__)

####OLD CODE




#no longer needed

#import sqlite3
#function for connection to the DATABASE
#def connect_db():
	#return sqlite3.connect(app.config['DATABASE'])

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
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
			return render_template('login.html', error=error)
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	if request.method == 'GET':
			return render_template('login.html')


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
				db.session.query(table).filter_by(batch=batch).update({"alive": newVal})

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
				db.session.query(table).filter_by(batch=batch).update({"alive": newVal})

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

@app.route('/main')
@login_required
def main():
	posts = db.session.query(Entry).order_by(Entry.entryDate.desc())
	return render_template('main.html', form = AddTaskForm(request.form), posts=posts)



if __name__ == '__main__':
	app.run(debug=True)

