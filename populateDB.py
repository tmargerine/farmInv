#import from csv into table

import csv
import sqlite3
import pdb

with sqlite3.connect("farmInv.db") as connection:
	c = connection.cursor()

	#open csv file
	document = csv.reader(open("updated.csv", "rU"))

	try:
		#ORIGINAL
		#create a new table
		# c.execute("CREATE TABLE animals(entryDate TEXT, batch TEXT, action TEXT, actionNo INT, value INT, notes TEXT)")

		#insert data
		#c.executemany("INSERT INTO animals(entryDate, batch, action, actionNo, value, notes) values (?, ?, ?, ?, ?, ?)", document)
		#END ORIGINAL


		c.execute("CREATE TABLE entries(_id INTEGER PRIMARY KEY AUTOINCREMENT, entryDate TEXT, batch TEXT, action TEXT, actionNo INT, value INT, notes TEXT)")
		#pdb.set_trace()

		c.execute("CREATE TABLE Broiler(_id INTEGER PRIMARY KEY AUTOINCREMENT, batch TEXT, purDate TEXT, alive TEXT, cvpb REAL, special INTEGER, sold INTEGER, dead INTEGER, feed REAL, time REAL, sales REAL, exp REAL)")
		c.execute("CREATE TABLE Layer(_id INTEGER PRIMARY KEY AUTOINCREMENT, batch TEXT, purDate TEXT, alive TEXT, cvpb REAL, special INTEGER, sold INTEGER, dead INTEGER, feed REAL, time REAL, sales REAL, exp REAL)")
		c.execute("CREATE TABLE Pig(_id INTEGER PRIMARY KEY AUTOINCREMENT, batch TEXT, purDate TEXT, alive TEXT, cvpb REAL, special INTEGER, sold INTEGER, dead INTEGER, feed REAL, time REAL, sales REAL, exp REAL)")


		for row in document:
			entryDate = row[0]
			batch = row[1]
			action = row[2]
			actionNo = int(row[3])
			if row[4] == '':
				value = 0
			else:
				value = float(row[4])
			notes = row[5]
			flag = False
			
			#pdb.set_trace()
			c.execute('insert into entries (entryDate, batch, action, actionNo, value, notes) values (?, ?, ?, ?, ?, ?)', [entryDate, batch, action, actionNo, value, notes])

			#check to see if batch is for sheep and set bdTable
			if batch in ("Lambs", "Ewes", "NB", "Rams"):
				dbTable = "Sheep"
				break

			#check to see batch is ducks
			elif batch in ("Drakes", "Ducks", "Ducklings"):
				dbTable = "Ducks"
				break

			#if not unique batches use standard form
			else:
				dbTable = batch[:-3]


			
			if action == "Purchase":
				cvpb = value / actionNo
				c.execute("INSERT INTO " + dbTable + " (batch, purDate, alive, cvpb, special, sold, dead, feed, time, sales, exp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [batch, entryDate, actionNo, cvpb, 0, 0, 0, 0, 0, 0, value])
				#connection.commit()
				continue
			else:
				#get data from specific animal table so we can update
				query0 = "SELECT * FROM " + dbTable + " WHERE batch = '" + batch +"'"

				temp = c.execute(query0)
				ogData = temp.fetchone()
				

				ogPurchDate = ogData[2]
				ogAlive = int(ogData[3])
				ogCVPB = ogData[4]
				ogSpecial = ogData[5]
				ogSold = ogData[6]
				ogDead = ogData[7]
				ogFeed = ogData[8]
				ogTime = ogData[9]
				ogSales = ogData[10]
				ogExp = ogData[11]
									

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
				newVal = ogSold - actionNo
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
				#debug
				#pdb.set_trace()

			elif action == "Time":
				newVal = ogTime + actionNo
				col = "Time"
				newVal2 = ogExp + value
				col2= "exp"
				flag = True

			if flag:
				query2 = "UPDATE " + dbTable + " SET " + col2 + " = " + str(newVal2) + " WHERE batch = '" + batch + "'"
				c.execute(query2)
				
			query = "UPDATE " + dbTable + " SET " + col + " = " + str(newVal) + " WHERE batch = '" + batch + "'"

			

			c.execute(query)

			
			#connection.commit()
			
			#g.db.close()
		connection.commit()
	except sqlite3.OperationalError:
		print "Error"
