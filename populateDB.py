#import from csv into table

import csv
import sqlite3

with sqlite3.connect("farmInv.db") as connection:
	c = connection.cursor()

	#open csv file
	document = csv.reader(open("pigs.csv", "rU"))

	try:
		#create a new table
		# c.execute("CREATE TABLE animals(entryDate TEXT, batch TEXT, action TEXT, actionNo INT, value INT, notes TEXT)")

		#insert data
		c.executemany("INSERT INTO animals(entryDate, batch, action, actionNo, value, notes) values (?, ?, ?, ?, ?, ?)", document)

	except sqlite3.OperationalError:
		print "Error"
		