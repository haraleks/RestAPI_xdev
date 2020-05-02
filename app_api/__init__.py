from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://test1:Test1_2020@localhost/flask_users_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app_api import models, routes

db.create_all()