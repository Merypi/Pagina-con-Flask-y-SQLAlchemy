# SECRET_KEY = "GDtfDCFYjD"
# SQLALCHEMY_DATABASE_URI = 'sqlite:///datos(4)'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
import os
SECRET_KEY = "GDtfDCFYjD" 
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.abspath(os.getcwd()) +'/datoss.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False