#models.py

from invController import db

class Entry(db.Model):

	__tablename__ = "entries"

	_id = db.Column(db.Integer, primary_key=True)
	entryDate = db.Column(db.Date, nullable=False)
	batch = db.Column(db.String, nullable=False)
	action = db.Column(db.String, nullable=False)
	actionNo = db.Column(db.Float)
	value = db.Column(db.Float)
	notes = db.Column(db.String)

	def __init__(self, entryDate, batch, action, actionNo, value, notes):
		self.entryDate = entryDate
		self.batch = batch
		self.action = action
		self.actionNo = actionNo
		self.value = value
		self.notes = notes

	#def __repr__(self):
		#return "<name %r>" % (self.entryDate)

class Broiler(db.Model):

	__tablename__ = "Broiler"

	_id = db.Column(db.Integer, primary_key=True)
	batch = db.Column(db.String, nullable=False)
	purDate = db.Column(db.Date, nullable=False)
	alive = db.Column(db.Integer)
	cvpb = db.Column(db.Float)
	special = db.Column(db.Integer)
	sold = db.Column(db.Integer)
	dead = db.Column(db.Integer)
	feed = db.Column(db.Float)
	time = db.Column(db.Float)
	sales = db.Column(db.Float)
	exp = db.Column(db.Float)

	def __init__(self, batch, purDate, alive, cvpb, special, sold, dead, feed, time, sales, exp):
		self.batch = batch
		self.purDate = purDate
		self.alive = alive
		self.cvpb = cvpb
		self.special = special
		self.sold = sold
		self.dead = dead
		self.feed = feed
		self.time = time
		self.sales = sales
		self.exp = exp

	#def __repr__(self):
		#return "<special %r>" % (self.special)
		#return "<record(batch='%s', purDate='%s', alive='%s', cvpb='%s', special='%s', sold='%s', dead='%s', feed='%s', time='%s', sales='%s', exp='%s')>" % ( self.batch, self.purDate, self.alive, self.cvpb, self.special, self.sold, self.dead, self.feed, self.time, self.sales, self.exp)
		#return '%s', '%s', '%s', '%s', '%s' % (self.batch, self.purDate, self.alive, self.cvpb, self.special)

class Layer(db.Model):

	__tablename__ = "Layer"

	_id = db.Column(db.Integer, primary_key=True)
	batch = db.Column(db.String, nullable=False)
	purDate = db.Column(db.Date, nullable=False)
	alive = db.Column(db.Integer)
	cvpb = db.Column(db.Float)
	special = db.Column(db.Integer)
	sold = db.Column(db.Integer)
	dead = db.Column(db.Integer)
	feed = db.Column(db.Float)
	time = db.Column(db.Float)
	sales = db.Column(db.Float)
	exp = db.Column(db.Float)

	def __init__(self, batch, purDate, alive, cvpb, special, sold, dead, feed, time, sales, exp):
		self.batch = batch
		self.purDate = purDate
		self.alive = alive
		self.cvpb = cvpb
		self.special = special
		self.sold = sold
		self.dead = dead
		self.feed = feed
		self.time = time
		self.sales = sales
		self.exp = exp

	#def __repr__(self):
		#return "<name %r>" % (self.batch)


class Pig(db.Model):

	__tablename__ = "Pig"

	_id = db.Column(db.Integer, primary_key=True)
	batch = db.Column(db.String, nullable=False)
	purDate = db.Column(db.Date, nullable=False)
	alive = db.Column(db.Integer)
	cvpb = db.Column(db.Float)
	special = db.Column(db.Integer)
	sold = db.Column(db.Integer)
	dead = db.Column(db.Integer)
	feed = db.Column(db.Float)
	time = db.Column(db.Float)
	sales = db.Column(db.Float)
	exp = db.Column(db.Float)

	def __init__(self, batch, purDate, alive, cvpb, special, sold, dead, feed, time, sales, exp):
		self.batch = batch
		self.purDate = purDate
		self.alive = alive
		self.cvpb = cvpb
		self.special = special
		self.sold = sold
		self.dead = dead
		self.feed = feed
		self.time = time
		self.sales = sales
		self.exp = exp

	#def __repr__(self):
		#return "<name %r>" % (self.batch)

class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User %r>' % (self.name)

		