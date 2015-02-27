##loading report to page

import sqlite3

#open db and get cursor
with sqlite3.connect("farmInv.db") as conn:
	c = conn.cursor()

	#query animals table to allocate data to specific animal tables
	rows = c.execute("SELECT * FROM animals")

	#cycle through results to allocate each entry accordingly
	for row in rows:
		entryDate = row[0]
		batch = row[1]
		action = row[2]
		actionNo = row[3]
		value = row[4]
		notes = row[5]

		#this section can be used when a single entry is submitted, using form data
		
		#check to see if batch is for sheep and set bdTable
		if ("Lambs", "Ewes", "NB", "Rams") in batch:
			dbTable = "Sheep"

		#check to see batch is ducks
		elif ("Drakes", "Ducks", "Ducklings"):
			dbTable = "Ducks"

		#if not unique batches use standard form
		else:
			dbTable = batch[:-3]
		
		if action = "Purchase":
			c.execute("INSERT INTO ? (batch,purDate, alive, cvpb, special, sold, dead, feed, time, sales, exp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", dbTable, batch, entryDate, actionNo, (value/actionNo), 0, 0, 0, 0, 0, 0, value)
			#break out of loop
		else:
			#get data from specific animal table so we can update
			ogData = c.execute("SELECT * FROM ?", dbTable)

			ogBatch = ogData[0]
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

		if action == "Dead" or action == "Lost":
			#update Dead data for batch, but data from animals table or form will be negative
			newDead == ogDead - actionNo
			c.execute("UPDATE ? SET dead = ? WHERE ogBatch = ? ", dbTable, newDead, batch)

		elif action == "Slaughter" or action == "Tray":
			#update slaughtered data
			newSlaughtered = ogSlaughtered + actionNo
			newSales = ogSales + value
			c.execute("UPDATE ? SET special = ? WHERE ogBatch = ? ", dbTable, newSlaughtered, batch)

		elif action == "Sold":
			newSold = ogSold + actionNo
			newSales = ogSales + value
			c.execute("UPDATE ? SET sold = ? WHERE ogBatch = ? ", dbTable, newSold, batch)

		elif action == "Feed":
			newFeed = ogFeed + actionNo
			newExp = ogExp + value
			c.execute("UPDATE ? SET exp = ? WHERE ogBatch = ? ", dbTable, newExp, batch)

		elif action == "Time":
			newTime = ogTime + actionNo
			newExp = ogExp + value
			c.execute("UPDATE ? SET time = ? WHERE ogBatch = ? ", dbTable, newTime, batch)
