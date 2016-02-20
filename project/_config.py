import os

basedir = os.path.dirname(os.path.abspath(__file__))

#DATABASE = 'flasktaskr.db'
#USERNAME = 'admin'
#PASSWORD = 'admin'
CSRF_ENABLED = True
SECRET_KEY = 'my_precious'
DEBUG = False

#DATABASE_PATH = os.path.join(basedir,DATABASE)
#DATABASE_PATH.replace("\\"," ")
#SQLAlCHEMY_DATABASE_URI = 'sqlite:///'+ DATABASE
#print SQLAlCHEMY_DATABASE_URI
