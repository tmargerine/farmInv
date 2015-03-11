# FarmInv controller

#imports
from functools import wraps
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
import config
import sqlite3
from forms import AddTaskForm
#debugger
import pdb

app = Flask(__name__)
#pulls configuration from file
app.config.from_object('config')
db = SLQAlchempy(app)

from models import Entry

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
	if request.meathon == 'POST':
		if form.validate_on_submit():
			new_entry = Entry(
				form.entryDate.data,
				form.batch.data,
				form.action.data,
				form.actionNo.data,
				form.value.data,
				form.notes.data)
			db.ssession.add(new_entry)
			db.session.commit()
	flash('New entry was successfully posted.Thanks.')

	entryDate = request.form['entryDate']
	batch = request.form['batch']
	action = request.form['action']
	actionNo = int(request.form['actionNo'])
	value = float(request.form['value'])
	table = request.form['batch']
	dbTable = table[:-3]

	if not entryDate or not batch:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into animals (entryDate, batch, action, actionNo, value, notes) values (?, ?, ?, ?, ?, ?)', [request.form['entryDate'], request.form['batch'], request.form['action'], request.form['actionNo'], request.form['value'], request.form['notes']])

		#start new code
		if action == "Purchase":
			cvpb = value / actionNo
			g.db.execute("INSERT INTO " + dbTable + " (batch, purDate, alive, cvpb, special, sold, dead, feed, time, sales, exp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [batch, entryDate, actionNo, cvpb, 0, 0, 0, 0, 0, 0, value])
			g.db.commit()
			flash('New entry was successfully posted!')
			return redirect(url_for('main'))
		else:
			#get data from specific animal table so we can update
			query0 = "SELECT * FROM " + dbTable + " WHERE batch = '" + batch +"'"

			temp = g.db.execute(query0)
			ogData = temp.fetchone()
			#debug
			#pdb.set_trace()

			ogPurchDate = ogData[1]
			ogAlive = ogData[2]
			ogCVPB = ogData[3]
			ogSlaughtered = ogData[4]
			ogSold = ogData[5]
			ogDead = ogData[6]
			ogFeed = ogData[7]
			ogTime = ogData[8]
			ogSales = ogData[9]
			ogExp = ogData[10]
			flag = False					

		if action == "Dead" or action == "Lost":
			#update Dead data for batch, but data from animals table or form will be negative
			newVal = ogDead - actionNo
			col = "dead"
			alive = ogAlive + actionNo
			c.execute("UPDATE " + dbTable + " SET alive  = " + str(alive) + " WHERE batch = '" + batch + "'")

		elif "Slaughter" in str(action):
			#update slaughtered data
			newVal = ogSpecial - actionNo
			alive = ogAlive + actionNo
			c.execute("UPDATE " + dbTable + " SET alive  = " + str(alive) + " WHERE batch = '" + batch + "'")
					
			col = "special"
			newVal2 = ogSales + value
			col2= "sales"
			flag = True
			
		elif action == "Tray":
			newVal = ogSpecial + actionNo
			col = "special"
			newVal2 = ogSales + value
			col2= "sales"
			flag = True

		elif action == "Sold":
			newVal = ogSold + actionNo
			col = "sold"
			newVal2 = ogSales + value
			col2= "sales"
			flag = True
			alive = ogAlive + actionNo
			c.execute("UPDATE " + dbTable + " SET alive  = " + str(alive) + " WHERE batch = '" + batch + "'")

		elif action == "Feed":
			newVal = ogFeed + actionNo
			col = "feed"
			newVal2 = ogExp + value
			col2= "exp"
			flag = True

		elif action == "Time":
			newVal = ogTime + actionNo
			col = "Time"
			newVal2 = ogExp + value
			col2= "exp"
			flag = True

		if flag:
			query2 = "UPDATE " + dbTable + " SET " + col2 + " = " + str(newVal2) + " WHERE batch = '" + batch + "'"
			g.db.execute(query2)

		query = "UPDATE " + dbTable + " SET " + col + " = " + str(newVal) + " WHERE batch = '" + batch + "'"
		g.db.execute(query)

		#End new code
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))

@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from animals order by entryDate DESC')
	posts = [dict(entryDate=row[1], batch=row[2], action=row[3], actionNo=row[4], value=row[5], notes=row[6]) for row in cur.fetchall()]
	g.db.close()

	posts = db.session.query(Task).filter

	return render_template('main.html', form = AddTaskForm(request.form), posts=posts)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
	g.db = connect_db()

	if request.method == 'POST':
		startDate = request.form['startDate']
		endDate = request.form['endDate']
	else:
		startDate = '2000-01-01'
		endDate = request.form['endDate']

	subQuery = "SELECT * FROM animals WHERE entryDate BETWEEN '"+ startDate + "' AND  '" + endDate + "'"
	cur = g.db.execute("SELECT sum(value) FROM animals WHERE action = 'Slaughter' AND batch LIKE 'Broiler___'")
	temp = cur.fetchone()
	reportData = dict(broilerSlaughter = temp[0])
	cur = g.db.execute("SELECT sum(value) FROM animals WHERE action = 'Sold' AND batch LIKE 'Broiler___'")
	temp = cur.fetchone()
	reportData['broilerSold'] = temp[0]

	cur = g.db.execute("SELECT sum(value) FROM animals WHERE action = 'Slaughter' AND batch LIKE 'Pig___'")
	temp = cur.fetchone()
	reportData['pigSlaughter'] = temp[0]

	cur = g.db.execute("SELECT sum(value) FROM animals WHERE action = 'Slaughter' AND batch LIKE 'Drakes'")
	temp = cur.fetchone()
	reportData['drakeSlaughter'] = temp[0]

	cur = g.db.execute("SELECT sum(value) FROM animals WHERE action = 'Slaughter' AND (batch LIKE 'Lambs' OR batch ='Ewes')")
	temp = cur.fetchone()
	reportData['sheepSlaughter'] = temp[0]

	cur = g.db.execute("SELECT sum(value) FROM animals WHERE action = 'Tray' AND batch LIKE 'Layer___'")
	temp = cur.fetchone()
	reportData['layerTray'] = temp[0]

	cur = g.db.execute("select * from animals WHERE action in ('Slaughter', 'Sold','Tray') order by entryDate DESC")
	posts = [dict(entryDate=row[1], batch=row[2], action=row[3], actionNo=row[4], value=row[5], notes=row[56]) for row in cur.fetchall()]
	g.db.close()


	return render_template('report.html', posts = posts, reportData = reportData, total = sum(reportData.itervalues()) )


@app.route('/layers')
@login_required
def layers():
	g.db = connect_db()
	cur = g.db.execute('select * from animals where batch like "Layer___" order by entryDate DESC')
	posts = [dict(entryDate=row[1], batch=row[2], action=row[3], actionNo=row[4], value=row[5], notes=row[6]) for row in cur.fetchall()]
	g.db.close()
	return render_template('layers.html', posts=posts)

@app.route('/broilers')
@login_required
def broilers():
	g.db = connect_db()
	cur = g.db.execute('select * from animals where batch like "Broiler___" order by entryDate DESC')
	posts = [dict(entryDate=row[1], batch=row[2], action=row[3], actionNo=row[4], value=row[5], notes=row[6]) for row in cur.fetchall()]
	g.db.close()
	return render_template('broilers.html', posts=posts)


if __name__ == '__main__':
	app.run(debug=True)

