from flask import Flask, request, jsonify
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors
from MySQLdb.constants import FIELD_TYPE
from random import choice as c
from cache import cache
import json
import os
import sys
#get current dir and set path for env dir so can import config vars
current_path = os.getcwd()
path_env = current_path + '/env'
sys.path.insert(0, path_env)
#also add parent path
parent_path = os.sep.join(os.getcwd().split(os.sep)[:-1])
parent_path_env = parent_path + '/env'
sys.path.insert(0, parent_path_env)

#initialize app
app = Flask(__name__)
app.config.from_pyfile('../env/config.py')
app.config['CACHE_TYPE'] = 'simple'

#db settings
db_sett = 'mysql://%s:%s@%s/%s' % (app.config['USER'], app.config['PW'], app.config['HOST'], app.config['DB'])
app.config['SQLALCHEMY_DATABASE_URI'] =  db_sett

from models import db
db.init_app(app)

#login settings
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

cache.init_app(app)

#MySQL conversions
my_conv = { FIELD_TYPE.LONG: int }

#Connect to MySQL
def openDB():
  db = MySQLdb.connect(host=app.config['HOST'], #hostname
                    user=app.config['USER'], # username
                    passwd=app.config['PW'], # password
                    db=app.config['DB'], # db
                    conv=my_conv,# datatype conversions
                    cursorclass=MySQLdb.cursors.DictCursor)
  cur = db.cursor()
  return db, cur


#connect to separate db
def openDB2():
  db2 = MySQLdb.connect(host=app.config['HOST2'], #hostname
                    user=app.config['USER2'], # username
                    passwd=app.config['PW2'], # password
                    db=app.config['DB2'], # db
                    conv=my_conv,# datatype conversions
                    cursorclass=MySQLdb.cursors.DictCursor)
  cur2 = db2.cursor()
  return db2, cur2

#handles quering mysql, output to json
def queryToData(cursor_obj,query,index=None,keyname=None,need_json=None):
  #print query
  if index==None and keyname==None and need_json==None:
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()
    data_f = json.dumps(data)
    return data_f

  if index!=None and keyname!=None and need_json==None:

  	cursor_obj.execute(query)
  	data = cursor_obj.fetchall()[index][keyname]
  	data_f = json.dumps(data)
  	return data_f

  if index==None and keyname==None and need_json!=None:

  	cursor_obj.execute(query)
  	data = cursor_obj.fetchall()
  	return data

  if index!=None and keyname!=None and need_json!=None:

    cursor_obj.execute(query)
    data = cursor_obj.fetchall()[index][keyname]
    return data

import views, models
if __name__ == '__main__':
  app.run()
