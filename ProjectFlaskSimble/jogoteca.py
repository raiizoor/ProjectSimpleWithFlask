
from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MySQL(app)

lm = LoginManager()
lm.init_app(app)

from back_end_listgames import *

if __name__ == '__main__':
    app.run()
