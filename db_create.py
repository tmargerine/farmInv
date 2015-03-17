#db_create.def 
from invController import db
#from models import Task
from datetime import datetime

#create the database and the db table
db.create_all()

#commit the changes
db.session.commit()