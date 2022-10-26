'''
******************************Please go through ReadMe.txt and main.py before run the project**********************************

This Module contains All connection (database,flask,flask_restful) component implementation code.

'''

import json
import mysql.connector
import urllib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

#Credential ==>> Please Replace Accordingly

username_value="root"
password_value="root@123"
host_value="127.0.0.1"
db_name="DBrequirmentAPI"
json_file_path_for_test="employee_and_skill_data.json" #one json file is avilable in project directory, replace path if you need
#to test with another file

    

app = Flask('requirmentAPI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


# Establising database connection & creating db

con = mysql.connector.connect(username=username_value, password=password_value, host=host_value)
c = con.cursor(buffered=True)
c.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
c.close()
con.close()


# configuring db with sqlalcheamy and app with restful api framework

# Syntax for URI: mysql://user:paswd@host name/db name
db_uri = f"mysql://{username_value}:{urllib.parse.quote(password_value)}@localhost/{db_name}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)  # Wrapping flask instance in orm and creating orm instance
api = Api(
    app
)  # Wrapping flask instance in restfulapi and creating restful api instance


# Read data from the json file

with open(f"{json_file_path_for_test}") as file:
    data = file.read()  # return string
    sample_data = json.loads(data)  # return python obj
    # print(sample_data['internal-recruitment-service'][49]['fullname'])
    # print(sample_data['internal-recruitment-service'][49]['skillsets'])