#config.py


import os

#grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

#configuation
DATABASE = 'farmInv.db'

#USERNAME = 'admin'
#PASSWORD = 'admin'

WTF_CSRF_ENABLED = True
SECRET_KEY = '90fd909a93'

#defines the full path for the DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

# The database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
