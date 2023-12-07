# database.py
import pymysql.cursors
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)
