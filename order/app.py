import os
from flask import Flask
from flask_migrate import Migrate

from routes import order_blueprint
from models import db, init_app

app = Flask(__name__)

app.config['SECRET_KEY'] = 'nBwg9uSus8m6kqApYqHUOQ'

file_path = os.path.abspath(os.getcwd())+"/database/order.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(order_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)