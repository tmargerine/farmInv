# FarmInv controller

#imports
from functools import wraps
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

#configuation
DATABASE = 'farmInv.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = '90fd909a93'

app = Flask(__name__)

#pulls in app configuation by looking for UPPERCASE variable
app.config.from_object(__name__)

#function for connection to the DATABASE
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error=error)

@app.route('/add', methods=['POST'])
@login_required
def add():
	entryDate = request.form['entryDate']
	batch = request.form['batch']

	if not entryDate or not batch:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into animals (entryDate, batch, action, actionNo, value, notes) values (?, ?, ?, ?, ?, ?)', [request.form['entryDate'], request.form['batch'], request.form['action'], request.form['actionNo'], request.form['value'], request.form['notes']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))

@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from animals order by entryDate DESC')
	posts = [dict(entryDate=row[0], batch=row[1], action=row[2], actionNo=row[3], value=row[4], notes=row[5]) for row in cur.fetchall()]
	g.db.close()
	return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)

